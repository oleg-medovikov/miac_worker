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
    'obslgepb_01', 'obslgepb_02', 'obslgepb_03', 'obslgepb_04', 'obslgepb_05', 'obslgepb_06',
    'obslgepb_07', 'obslgepb_08', 'obslgepb_09', 'obslgepb_10', 'obslgepb_11', 'obslgepb_12',
    'obslgepb_13', 'obslgepb_14', 'obslgepb_15', 'obslgepb_16'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "1. подлежащих обследованию на маркеры вирусного гепатита В": (
        "_01",
        "_05",
        "_09",
        "_13",
    ),
    "2. обследованных на маркеры вирусного гепатита В": (
        "_02",
        "_06",
        "_10",
        "_14",
    ),
    "3. у которых маркеры вирусного гепатита В выявлены впервые": (
        "_03",
        "_07",
        "_11",
        "_15",
    ),
    "4. у которых маркеры вирусного гепатита В выявлены при поступлении на работу": (
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

inspection_gepB = SQL_otchet(
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
