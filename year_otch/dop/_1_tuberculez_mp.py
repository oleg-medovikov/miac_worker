from clas import SQL_otchet

sql = """
SELECT
    a.AGNNAME ORGANIZATION,
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
WHERE rf.CODE = 'ОхранаЗОбщ' 
and i.CODE IN (
    'tub_01', 'tub_02', 'tub_03', 'tub_04', 'tub_05',
    'tub_06', 'tub_07', 'tub_08', 'tub_09', 'tub_10',
    'tub_11'
)
and r.BDATE between  to_date(__start__,'yyyy-mm-dd')
    AND  to_date(__stop__,'yyyy-mm-dd')
"""

pokazatel = {
    "tub_01": "01. Эпидномер",
    "tub_02": "02. Дата заболевания",
    "tub_03": "03. Дата регистрации заболевания",
    "tub_04": "04. Возраст",
    "tub_05": "05. Должность",
    "tub_06": "06. Отделение",
    "tub_07": "07. Стаж работы в отделении (в годах)",
    "tub_08": "08. Дата последнего флюрографического исследования",
    "tub_09": "09. Выявлен активно",
    "tub_10": "10. Результаты лабораторных исследований",
    "tub_11": "11. Окончательный диагноз (форма туберкулеза)",
}

tuberculez_mp = SQL_otchet(
    filename="/tmp/Охрана_Здоровья.xlsx",
    sql=sql,
    pokazatel=pokazatel,
    del_col=["level_2", "ROW_INDEX"],
    pivot={
        "index": ["ORGANIZATION", "ROW_INDEX"],
        "columns": ["POKAZATEL"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
