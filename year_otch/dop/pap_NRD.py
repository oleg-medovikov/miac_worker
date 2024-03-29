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
WHERE rf.CODE = 'ИнфконтрольНРД' 
and i.CODE IN (
    'papnrd_01', 'papnrd_02', 'papnrd_03', 'papnrd_04', 'papnrd_05'
)
and r.BDATE between  to_date(__start__,'yyyy-mm-dd')
    AND  to_date(__stop__,'yyyy-mm-dd')
"""

pokazatel = {
    "papnrd_01": "1. Наличие протокола ПАП (да/нет)",
    "papnrd_02": "2. Торговое наименование лекарственного препарата, используемого для ПАП",
    "papnrd_03": "3. Количество операций ВСЕГО",
    "papnrd_04": "4. Количество операций, при которых показано ПАП",
    "papnrd_05": "5. Количество операций, при которых проведено ПАП ВСЕГО",
}

pap_NRD = SQL_otchet(
    filename="/tmp/Инфконтроль_НРД.xlsx",
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
