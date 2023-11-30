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
    'gepbmr_01', 'gepbmr_02', 'gepbmr_03', 'gepbmr_04', 'gepbmr_05',
    'gepbmr_06', 'gepbmr_07', 'gepbmr_08', 'gepbmr_09', 'gepbmr_10',
    'gepbmr_11'
)
and r.BDATE between  to_date(__start__,'yyyy-mm-dd')
    AND  to_date(__stop__,'yyyy-mm-dd')
"""

pokazatel = {
    "gepbmr_01": "01. Эпидномер",
    "gepbmr_02": "02. Дата заболевания",
    "gepbmr_03": "03. Дата регистрации заболевания",
    "gepbmr_04": "04. Возраст",
    "gepbmr_05": "05. Должность",
    "gepbmr_06": "06. Отделение",
    "gepbmr_07": "07. Стаж работы в отделении (в годах)",
    "gepbmr_08": "08. Наличие трёхкратной вакцинации",
    "gepbmr_09": "09. Результаты лабораторных исследований",
    "gepbmr_10": "10. Окончательный диагноз",
    "gepbmr_11": "11. Предполагаемый путь инфекцирования",
}

gepB_mr = SQL_otchet(
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
