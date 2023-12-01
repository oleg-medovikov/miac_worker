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
WHERE rf.CODE = 'ТрадицОбщ'
and bi.CODE in (
    'boldr_01', 'boldr_02', 'boldr_03', 'boldr_04', 'boldr_05', 'boldr_06',
    'boldr_07', 'boldr_08', 'boldr_09', 'boldr_10', 'boldr_11', 'boldr_12',
    'boldr_13', 'boldr_14'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "01. Малярия": ("_01", "_02"),
    "02. Сыпной тиф": ("_03", "_04"),
    "03. Болезнь Брилля": ("_05", "_06"),
    "04. Педикулез": ("_07", "_08"),
    "05. Чесотка": ("_09", "_10"),
    "06. Сифилис (заразная форма)": ("_11", "_12"),
    "07. Болезнь, вызванная ВИЧ + носители ВИЧ-инфекции (бессимптомный статус)": (
        "_13",
        "_14",
    ),
}

rows = {
    "1. заноса Инф.З.": (
        "_01",
        "_03",
        "_05",
        "_07",
        "_09",
        "_11",
        "_13",
    ),
    "2. внутрибольничных Инф.З.": (
        "_02",
        "_04",
        "_06",
        "_08",
        "_10",
        "_12",
        "_14",
    ),
}

infections_4 = SQL_otchet(
    filename="/tmp/Традиционные_инфекции.xlsx",
    sql=sql,
    columns=columns,
    cols_name="Нозологические формы",
    rows=rows,
    rows_name="Количество случаев",
    del_col=[],
    pivot={
        "index": ["ORGANIZATION", "Количество случаев"],
        "columns": ["Нозологические формы"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
