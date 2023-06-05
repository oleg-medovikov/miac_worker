from datetime import datetime, timedelta
from pandas import concat, to_numeric
import shutil
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

from .svod_40_sql import SQL_VACHIN, SQL_REVAC_MO, SQL_REVAC_TVSP

LIST_POK = [
    'DAY', 'TYPE', 'distr', 'org',
    '_01', '_02', '_03', '_04', '_05', '_06', '_07', '_08', '_09',
    '_10', '_11', '_12', '_13', '_14', '_15', '_16', '_17', '_18', '_19',
    '_20', '_21', '_22', '_23', '_24', '_25', '_26', '_27', '_28', '_29',
    '_30', '_31', '_32',
]

POKAZATELS = ['KOVIVAC', 'KONVASEL', 'CPUTNIKL', 'CPUTNIKV', 'EPIVAK']


def svod_40_covid_new():
    "Новый свод 40 ковида"
    DICT = {}

    # Вытаскиваем вакцины всем скопом и разбиваем на таблички
    DF = parus_sql(SQL_VACHIN)
    DF = DF.pivot_table(
        index=['DAY', 'ORGANIZATION', 'TYPE', 'ROW_INDEX'],
        columns=['POKAZATEL'],
        values='VALUE',
        aggfunc='first'
    )
    DF = DF.reset_index()

    for col in DF.columns:
        try:
            DF[col] = to_numeric(DF[col])
        except ValueError:
            continue

    for POKAZATEL in POKAZATELS:
        # Формируем список колонок
        COLUMNS = [x.replace('_', POKAZATEL + '_') for x in LIST_POK]
        # Добавляем недостающие
        for COL in COLUMNS:
            if COL not in DF.columns:
                DF[COL] = ''

        PART = DF[COLUMNS].copy()
        # проставляем назхвания организаций

        PART.loc[
            (PART['TYPE'] == 'Медицинская организация'),
            POKAZATEL + '_02'
        ] = PART['org']
        PART.loc[
            (PART['TYPE'] == 'Медицинская организация'),
            POKAZATEL + '_01'
        ] = PART['distr']

        del PART['org']
        del PART['distr']

        PART.loc[
            (PART[POKAZATEL + '_01'].isnull())
            & (PART['TYPE'] == 'Пункт вакцинации'),
            POKAZATEL + '_01'] = DF[
                POKAZATEL + '_02'
                ].str.split().str[0] + ' район'

        PART = PART.loc[~PART[POKAZATEL + '_02'].isnull()]

        DICT[POKAZATEL] = PART.loc[PART['DAY'] == PART['DAY'].max()]
        DICT[POKAZATEL + '_OLD'] = PART.loc[PART['DAY'] == PART['DAY'].min()]

    # Вытаскиваем ревакцинацию за МО
    list_ = []
    D_VAC = {
        '1': ' Всего',
        '2': 'Гам-КОВИД-Вак (Спутник-V)',
        '3': 'КовиВак',
        '4': 'ЭпиВакКорона',
        '5': 'Спутник Лайт',
        '6': 'Конвасэл',
    }
    for i in range(1, 7):
        SQL_ = SQL_REVAC_MO.replace('индекс', str(i))
        DF = parus_sql(SQL_)
        list_.append(DF)

    DF = concat(list_, ignore_index=True)
    DF['TYPEVACINE'] = DF['INDX'].map(D_VAC)
    DF['SCEP'] = DF['ORGANIZATION'] + DF['TYPEVACINE']

    TVSP = parus_sql(SQL_REVAC_TVSP)
    DF = concat([DF, TVSP], ignore_index=True)
    DF = DF.sort_values(['INDX', 'ORGANIZATION'])

    DICT['REVAC'] = DF.loc[DF['DAY'] == DF['DAY'].max()]
    DICT['REVAC_OLD'] = DF.loc[DF['DAY'] == DF['DAY'].min()]

    new_name_pred = 'temp/40_COVID_19_БОТКИНА_' + DF['DAY'].max() + '_предварительный.xlsx'
    new_name_osn = 'temp/40_COVID_19_БОТКИНА_' + DF['DAY'].max() + '_основной.xlsx'

    shutil.copyfile('help/40_COVID_19_pred_new.xlsx', new_name_pred)
    shutil.copyfile('help/40_COVID_19_osn.xlsx', new_name_osn)

    # Записываем данные в предварительный файл
    wb = openpyxl.load_workbook(new_name_pred)
    # 'KOVIVAC', 'KONVASEL', 'CPUTNIKL', 'CPUTNIKV', 'EPIVAK'
    D_PRINT = {
        'Спутник-V':          ('CPUTNIKV',        5, 1),
        'Вчера_Спутник':      ('CPUTNIKV_OLD',    5, 1),
        'ЭпиВакКорона':       ('EPIVAK',      5, 1),
        'Вчера_ЭпиВак':       ('EPIVAK_OLD',  5, 1),
        'КовиВак':            ('KOVIVAC',     5, 1),
        'Конвасэл':           ('KONVASEL', 5, 1),
        'Вчера_КовиВак':      ('KOVIVAC_OLD', 5, 1),
        'Спутник Лайт':       ('CPUTNIKL',       5, 1),
        'Вчера_Спутник Лайт': ('CPUTNIKL_OLD',   5, 1),
        'Ревакцинация':       ('REVAC',       10, 1),
        'Вчера_ревакцин':     ('REVAC_OLD',   10, 1),
        'Вчера_Конвасэл':     ('KONVASEL_OLD', 5, 1),
            }

    for key, value in D_PRINT.items():
        ws = wb[key]
        DATA = DICT[value[0]]
        del DATA['DAY']
        rows = dataframe_to_rows(DATA, index=False, header=False)
        for r_idx, row in enumerate(rows, value[1]):
            for c_idx, val in enumerate(row, value[2]):
                ws.cell(row=r_idx, column=c_idx, value=val)

    wb.save(new_name_pred)

    return new_name_pred
