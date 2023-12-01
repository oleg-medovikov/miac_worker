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
    'gep_01', 'gep_02', 'gep_03', 'gep_04', 'gep_05', 'gep_06',
    'gep_07', 'gep_08', 'gep_09', 'gep_10', 'gep_11', 'gep_12',
    'gep_13', 'gep_14', 'gep_15', 'gep_16', 'gep_17', 'gep_18',
    'gep_19'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "01. Острые вирусные гепатиты ВСЕГО": ("_01", "_14"),
    "02. Острый гепатит А": ("_02", "_15"),
    "03. Острый вирусный гепатит В": ("_03", "_16"),
    "04. Острый вирусный гепатит С": ("_04", "_17"),
    "05. Сочетанные формы (острый вирусный гепатит В+острый вирусный гепатит С)": (
        "_05",
        "_18",
    ),
    "06. Острый неверифицированный (неуточненный) вирусный гепатит": ("_06", "_19"),
    "07. Хронические вирусные гепатиты ВСЕГО": ("_07",),
    "08. Хронический вирусный гепатит В": ("_08",),
    "09. Хронический вирусный гепатит С": ("_09",),
    "10. Сочетанные формы (хронический вирусный гепатит В+хронический вирусный гепатит С)": (
        "_10",
    ),
    "11. Хронический неверифицированный (неуточненный) вирусный гепатит": ("_11",),
    "12. Носительство HBsAg": ("_12",),
    "13. Носительство анти-HCV": ("_13",),
}

rows = {
    "1. заноса Инф.З.": (
        "_01",
        "_02",
        "_03",
        "_04",
        "_05",
        "_06",
        "_07",
        "_08",
        "_09",
        "_10",
        "_11",
        "_12",
        "_13",
    ),
    "2. внутрибольничных Инф.З.": (
        "_14",
        "_15",
        "_16",
        "_17",
        "_18",
        "_19",
    ),
}

infections_3 = SQL_otchet(
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
