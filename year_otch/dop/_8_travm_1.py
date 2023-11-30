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
    'travm_01', 'travm_02', 'travm_03', 'travm_04', 'travm_05', 'travm_06',
    'travm_07', 'travm_08', 'travm_09', 'travm_10', 'travm_11', 'travm_12',
    'travm_13', 'travm_14', 'travm_15', 'travm_16', 'travm_18', 'travm_19',
    'travm_20', 'travm_21', 'travm_22', 'travm_23', 'travm_24'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "1. укола иглой": (
        "_01",
        "_07",
        "_13",
        "_19",
    ),
    "2. пореза скальпелем": (
        "_02",
        "_08",
        "_14",
        "_20",
    ),
    "3. попадания жидких биологических сред (кровь, ликвор и пр.) на слизистую": (
        "_03",
        "_09",
        "_15",
        "_21",
    ),
    "4. попадания жидких биологических сред (кровь, ликвор и пр.) на кожу": (
        "_04",
        "_10",
        "_16",
        "_22",
    ),
    "5.  травм при обращении с медицинскими отходами": (
        "_05",
        "_11",
        "_17",
        "_23",
    ),
    "6. прочих травм": (
        "_06",
        "_12",
        "_18",
        "_24",
    ),
}
rows = {
    "1. врачи": ("_01", "_02", "_03", "_04", "_05", "_06"),
    "2. средний МП": ("_07", "_08", "_09", "_10", "_11", "_12"),
    "3. младший МП": ("_13", "_14", "_15", "_16", "_17", "_18"),
    "4. прочие": ("_19", "_20", "_21", "_22", "_23", "_24"),
}

travm_1 = SQL_otchet(
    filename="/tmp/Охрана_Здоровья.xlsx",
    sql=sql,
    columns=columns,
    cols_name="Количество случаев",
    rows=rows,
    rows_name="Категории медицинских работников",
    del_col=[],
    pivot={
        "index": ["ORGANIZATION", "Категории медицинских работников"],
        "columns": ["Количество случаев"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
