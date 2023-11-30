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
    'gepcmr_01', 'gepcmr_02', 'gepcmr_03', 'gepcmr_04', 'gepcmr_05',
    'gepcmr_06', 'gepcmr_07', 'gepcmr_08', 'gepcmr_09', 'gepcmr_10'
)
and r.BDATE between  to_date(__start__,'yyyy-mm-dd')
    AND  to_date(__stop__,'yyyy-mm-dd')
"""

pokazatel = {
    "gepcmr_01": "01. Эпидномер",
    "gepcmr_02": "02. Дата заболевания",
    "gepcmr_03": "03. Дата регистрации заболевания",
    "gepcmr_04": "04. Возраст",
    "gepcmr_05": "05. Должность",
    "gepcmr_06": "06. Отделение",
    "gepcmr_07": "07. Стаж работы в отделении (в годах)",
    "gepcmr_08": "08. Результаты лабораторных исследований",
    "gepcmr_09": "09. Окончательный диагноз",
    "gepcmr_10": "10. Предполагаемый путь инфекцирования",
}

gepC_mr = SQL_otchet(
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
