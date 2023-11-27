from clas import SQL_otchet

sql = """
SELECT
    a.AGNNAME ORGANIZATION ,
    bi.CODE  pokazatel,
    NUMVAL value
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
WHERE rf.CODE = 'ИнфконтрольОБЩ'
and bi.CODE in ('kolop_01', 'kolop_02', 'kolop_03', 'kolop_04', 'kolop_05', 'kolop_06')
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

pokazatel = {
    "kolop_01": "01. Количество прооперированных пациентов",
    "kolop_02": "02. Количество операций ВСЕГО",
    "kolop_03": "03. Количество операций с I-м классом операционной раны",
    "kolop_04": "04. Количество операций с II-м классом операционной раны",
    "kolop_05": "05. Количество операций с III-м классом операционной раны",
    "kolop_06": "06. Количество операций с IV-м классом операционной раны",
}

operation_count_GEN = SQL_otchet(
    filename="/tmp/Инфконтроль_ОБЩ.xlsx",
    sql=sql,
    pokazatel=pokazatel,
    del_col=["level_1"],
    pivot={
        "index": ["ORGANIZATION"],
        "columns": ["POKAZATEL"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
