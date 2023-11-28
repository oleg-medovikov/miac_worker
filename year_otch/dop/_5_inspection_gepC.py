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
WHERE rf.CODE = 'ОхранаЗОбщ'
and bi.CODE in (
    'obslgepc_01', 'obslgepc_02', 'obslgepc_03', 'obslgepc_04', 'obslgepc_05', 'obslgepc_06',
    'obslgepc_07', 'obslgepc_08', 'obslgepc_09', 'obslgepc_10', 'obslgepc_11', 'obslgepc_12',
    'obslgepc_13', 'obslgepc_14', 'obslgepc_15', 'obslgepc_16'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "1. подлежащих обследованию на маркеры вирусного гепатита С": (
        "_01",
        "_05",
        "_09",
        "_13",
    ),
    "2. обследованных на маркеры вирусного гепатита С": (
        "_02",
        "_06",
        "_10",
        "_14",
    ),
    "3. у которых маркеры вирусного гепатита С выявлены впервые": (
        "_03",
        "_07",
        "_11",
        "_15",
    ),
    "4. у которых маркеры вирусного гепатита С выявлены при поступлении на работу": (
        "_04",
        "_08",
        "_12",
        "_16",
    ),
}
rows = {
    "1. врачи": ("_01", "_02", "_03", "_04"),
    "2. средний МП": ("_05", "_06", "_07", "_08"),
    "3. младший МП": ("_09", "_10", "_11", "_12"),
    "4. прочие": ("_13", "_14", "_15", "_16"),
}

inspection_gepC = SQL_otchet(
    filename="/tmp/Охрана_Здоровья.xlsx",
    sql=sql,
    columns=columns,
    cols_name="Численность медицинских работников",
    rows=rows,
    rows_name="Категории медицинских работников",
    del_col=[],
    pivot={
        "index": ["ORGANIZATION", "Категории медицинских работников"],
        "columns": ["Численность медицинских работников"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
