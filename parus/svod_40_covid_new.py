from datetime import datetime, timedelta
from pandas import concat
import shutil
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql


MNEMOKOD = '40 COVID 19'
DATE_NEW = 'trunc(SYSDATE + 2 )'
DATE_OLD = 'trunc(SYSDATE + 1 )'
POKAZATELS = ['KOVIVAC', 'KONVASEL', 'CPUTNIKL', 'CPUTNIKV', 'EPIVAK']
LIST_POK_1 = [
    'distr', 'org', 'type', '_03', '_04', '_05', '_06', '_07', '_08', '_09',
    '_10', '_11', '_12', '_13', '_14', '_15', '_16', '_17', '_18', '_19',
    '_20', '_21', '_22', '_23', '_24', '_25', '_26', '_27', '_28', '_29',
    '_30', '_31', '_32',
]
LIST_POK_2 = [
    '_01', '_02', 'type', '_03', '_04', '_05', '_06', '_07', '_08', '_09',
    '_10', '_11', '_12', '_13', '_14', '_15', '_16', '_17', '_18', '_19',
    '_20', '_21', '_22', '_23', '_24', '_25', '_26', '_27', '_28', '_29',
    '_30', '_31', '_32',
]


SQL_VACHIN = f"""SELECT
    to_char(r.BDATE, 'DD.MM.YYYY') day,
    bi.CODE  pokazatel,
    a.AGNNAME ORGANIZATION,
        CASE WHEN STRVAL IS NOT NULL THEN STRVAL
         WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
         WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
    ELSE NULL END value
    FROM PARUS.BLINDEXVALUES  d
       INNER JOIN PARUS.BLSUBREPORTS s
       ON (d.PRN = s.RN)
       INNER JOIN PARUS.BLREPORTS r
       ON(s.PRN = r.RN)
       INNER JOIN PARUS.AGNLIST a
       on(r.AGENT = a.rn)
       INNER JOIN PARUS.BLREPFORMED pf
       on(r.BLREPFORMED = pf.RN)
       INNER JOIN PARUS.BLREPFORM rf
       on(pf.PRN = rf.RN)
       INNER JOIN PARUS.BALANCEINDEXES bi
       on(d.BALANCEINDEX = bi.RN)
    WHERE rf.code = '{MNEMOKOD}'
        AND r.BDATE in ({DATE_OLD}, {DATE_NEW})
        AND (
        (bi.CODE like '!POKAZATEL!%'
        and bi.CODE not like '%_O')
        or bi.CODE in ('distr', 'org'))
"""
SQL_VACHIN_TVSP = f"""SELECT
            to_char(r.BDATE, 'DD.MM.YYYY') day,
            a.AGNNAME organization,
            i.CODE pokazatel,
            ro.NUMB row_index ,
            CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
                WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
                WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
                ELSE NULL END value
        FROM PARUS.BLTBLVALUES v
        INNER JOIN PARUS.BLTABLESIND si
            on(v.BLTABLESIND = si.RN)
        INNER JOIN PARUS.BALANCEINDEXES i
            on(si.BALANCEINDEXES = i.RN)
        INNER JOIN PARUS.BLTBLROWS ro
            on(v.PRN = ro.RN)
        INNER JOIN PARUS.BLSUBREPORTS s
            on(ro.PRN = s.RN)
        INNER JOIN PARUS.BLREPORTS r
            on(s.PRN = r.RN)
        INNER JOIN PARUS.AGNLIST a
            on(r.AGENT = a.RN)
        INNER JOIN PARUS.BLREPFORMED rd
            on(r.BLREPFORMED = rd.RN)
        INNER JOIN PARUS.BLREPFORM rf
            on(rd.PRN = rf.RN)
            WHERE rf.code =  '{MNEMOKOD}'
                and r.BDATE  in ({DATE_OLD}, {DATE_NEW})
                and (
                    (i.CODE like '!POKAZATEL!%'
                    and i.CODE not like '%_O')
                    )
"""
SQL_REVAC_MO = f"""SELECT
        to_char(r.BDATE, 'DD.MM.YYYY') day,
        a.AGNNAME ORGANIZATION,
        'индекс' indx,
        rf.CODE  otchet,
        bi.CODE  pokazatel,
        CASE WHEN STRVAL IS NOT NULL THEN STRVAL
            WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
            WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
            ELSE NULL END value
        FROM PARUS.BLINDEXVALUES  d
            INNER JOIN PARUS.BLSUBREPORTS s
                ON (d.PRN = s.RN)
            INNER JOIN PARUS.BLREPORTS r
                ON(s.PRN = r.RN)
            INNER JOIN PARUS.AGNLIST a
                on(r.AGENT = a.rn)
            INNER JOIN PARUS.BLREPFORMED pf
                on(r.BLREPFORMED = pf.RN)
            INNER JOIN PARUS.BLREPFORM rf
                on(pf.PRN = rf.RN)
            INNER JOIN PARUS.BALANCEINDEXES bi
                on(d.BALANCEINDEX = bi.RN)
        WHERE rf.code = '{MNEMOKOD}'
            and  r.BDATE in ({DATE_OLD}, {DATE_NEW})
            and bi.CODE in (
            'revac_02_0индекс_s', 'revac_0индекс_03_s', 'revac_04_0индекс_s',
            'revac_05_0индекс_s', 'revac_06_0индекс_s', 'revac_07_0индекс_s',
            'revac_08_0индекс_s', 'revac_09_0индекс_s', 'revac_10_0индекс_s',
            'revac_11_0индекс_s', 'revac_12_0индекс_s', 'revac_13_0индекс_s',
            'revac_14_0индекс_s', 'revac_15_0индекс_s', 'revac_16_0индекс_s',
            'revac_17_0индекс_s', 'revac_18_0индекс_s', 'revac_19_0индекс_s'
                )
"""


def svod_40_covid_new():
    "Новый свод 40 ковида"
    DICT = {}

    # Вытаскиваем верхнюю строчку организации
    for POKAZATEL in POKAZATELS:
        SQL_VACHIN_ = SQL_VACHIN.replace('!POKAZATEL!', POKAZATEL)

        DF = parus_sql(SQL_VACHIN_)

        DF = DF.pivot_table(
            index=['DAY', 'ORGANIZATION'],
            columns=['POKAZATEL'],
            values='VALUE',
            aggfunc='first'
        )

        COLUMNS = [x.replace('_', POKAZATEL + '_') for x in LIST_POK_1]
        for COL in COLUMNS:
            if COL not in DF.columns:
                DF[COL] = 0
        DF['type'] = 'Медицинская организация'
        DF = DF.reset_index()
        OLD = DF.loc[DF['DAY'] == DF['DAY'].min()]
        NEW = DF.loc[DF['DAY'] == DF['DAY'].max()]
        OLD.index = range(len(OLD))
        NEW.index = range(len(NEW))

        DICT[POKAZATEL] = NEW[[COLUMNS]]
        DICT[POKAZATEL + '_OLD'] = OLD[[COLUMNS]]

    # Вытаскиваем таблицу ТВСП снизу
    for POKAZATEL in POKAZATELS:
        SQL_VACHIN_ = SQL_VACHIN_TVSP.replace('!POKAZATEL!', POKAZATEL)

        DF = parus_sql(SQL_VACHIN_)

        DF = DF.pivot_table(
            index=['DAY', 'ORGANIZATION'],
            columns=['POKAZATEL'],
            values='VALUE',
            aggfunc='first'
        )

        COLUMNS = [x.replace('_', POKAZATEL + '_') for x in LIST_POK_2]
        for COL in COLUMNS:
            if COL not in DF.columns:
                DF[COL] = 0
        DF['type'] = 'Пункт вакцинации'
        DF['CPUTNIKL_01'] = DF['CPUTNIKL_02'].str.split().str[0] + ' район'
        OLD = DF.loc[DF['DAY'] == DF['DAY'].min()]
        NEW = DF.loc[DF['DAY'] == DF['DAY'].max()]
        OLD.index = range(len(OLD))
        NEW.index = range(len(NEW))

        DICT[POKAZATEL] = NEW[[COLUMNS]]
        DICT[POKAZATEL + '_OLD'] = OLD[[COLUMNS]]

    # Вытаскиваем ревакцинацию за МО
    list_ = []
    for i in range(1, 7):
        SQL_ = SQL_REVAC_MO.replace('индекс', str(i))
        DF = parus_sql(SQL_)
        DF = DF.pivot_table(
            index=['DAY', 'ORGANIZATION', 'INDX'],
            columns=['POKAZATEL'],
            values='VALUE',
            aggfunc='first'
        )
        list_.append(DF.reset_index())

    DF = concat(list_, ignore_index=True)
    OLD = DF.loc[DF['DAY'] == DF['DAY'].min()]
    NEW = DF.loc[DF['DAY'] == DF['DAY'].max()]





