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
WHERE rf.CODE = 'ИнфконтрольРД' 
and i.CODE IN (
    'pap_01', 'pap_02', 'pap_03', 'pap_04', 'pap_05',
    'pap_06', 'pap_07', 'pap_08', 'pap_09', 'pap_10'
)
and r.BDATE between  to_date(__start__,'yyyy-mm-dd')
    AND  to_date(__stop__,'yyyy-mm-dd')
"""

pokazatel = {
    "pap_01": "01. Наличие протокола ПАП (да/нет)",
    "pap_02": "02. Торговое наименование лекарственного препарата, используемого для ПАП",
    "pap_03": "03. Количество операций Кесарево сечение Всего",
    "pap_04": "04. Количество операций Кесарево сечение, при которых показано ПАП",
    "pap_05": "05. Количество операций Кесарево сечение, при которых проведено ПАП ВСЕГО",
    "pap_06": "06. Наличие протокола ПАП при других оперативных вмешательствах",
    "pap_07": "07. Торговое наименование лекарственного препарата, используемого для ПАП при других оперативных вмешательствах",
    "pap_08": "08. Количество других оперативных вмешательств",
    "pap_09": "09. Количество других оперативных вмешательств, при которых показано ПАП",
    "pap_10": "10. Количество других оперативных вмешательств, при которых проведено ПАП",
}

pap_RD = SQL_otchet(
    filename="/tmp/Инфконтроль_РД.xlsx",
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
