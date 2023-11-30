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
WHERE rf.CODE = 'РодовспоможениеРод'
and bi.CODE in (
    'rddop_01', 'rddop_02', 'rddop_03',
    'rddop_04', 'rddop_05', 'rddop_06',
    'rddop_07', 'rddop_08'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""
pokazatel = {
    "rddop_01": "1. Всего родов",
    "rddop_02": "2. Акушерские щипцы",
    "rddop_03": "3. Преждевременные роды",
    "rddop_04": "4. Кесарево сечение",
    "rddop_05": "5. Перинеотомия",
    "rddop_06": "6. Ручное отделение последа",
    "rddop_07": "7. Ручное обследование матки",
    "rddop_08": "8. Плодоразрушительные операции",
}

obstetrics_1 = SQL_otchet(
    filename="/tmp/Родовспоможение.xlsx",
    sql=sql,
    pokazatel=pokazatel,
    del_col=["level_1"],
    pivot={
        "index": [
            "ORGANIZATION",
        ],
        "columns": ["POKAZATEL"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
