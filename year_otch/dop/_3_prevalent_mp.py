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
    'prev_01', 'prev_02', 'prev_03', 'prev_04', 'prev_05', 'prev_06',
    'prev_07', 'prev_08', 'prev_09', 'prev_10', 'prev_11', 'prev_12',
    'prev_13', 'prev_14', 'prev_15', 'prev_16', 'prev_17', 'prev_18',
    'prev_19', 'prev_20', 'prev_21', 'prev_22', 'prev_23', 'prev_24',
    'prev_25', 'prev_26', 'prev_27', 'prev_28', 'prev_29', 'prev_30',
    'prev_31', 'prev_32', 'prev_33', 'prev_34', 'prev_35', 'prev_36'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "1. состоящих на диспансерном учете по острому вирусному гепатиту А": (
        "_01",
        "_10",
        "_19",
        "_28",
    ),
    "2. состоящих на диспансерном учете по острому вирусному гепатиту В": (
        "_02",
        "_11",
        "_20",
        "_29",
    ),
    "3. состоящих на диспансерном учете по острому вирусному гепатиту С": (
        "_03",
        "_12",
        "_21",
        "_30",
    ),
    "4. состоящих на диспансерном учете по хроническому вирусному гепатиту В": (
        "_04",
        "_13",
        "_22",
        "_31",
    ),
    "5. состоящих на диспансерном учете по хроническому вирусному гепатиту С": (
        "_05",
        "_14",
        "_23",
        "_32",
    ),
    "6. состоящих на диспансерном учете по ХВГВ + ХВГС": ("_06", "_15", "_24", "_33"),
    '7. являющихся "носителями" Анти-HCV и находящихся на диспансерном наблюдении': (
        "_07",
        "_16",
        "_25",
        "_34",
    ),
    '8. являющихся "носителями" HBsAg  и находящихся на диспансерном наблюдении': (
        "_08",
        "_17",
        "_26",
        "_35",
    ),
    "9. состоящих на диспансерном учете по неверифицированному хроническому вирусному гепатиту": (
        "_09",
        "_18",
        "_27",
        "_36",
    ),
}
rows = {
    "1. врачи": ("_01", "_02", "_03", "_04", "_05", "_06", "_07", "_08", "_09"),
    "2. средний МП": ("_10", "_11", "_12", "_13", "_14", "_15", "_16", "_17", "_18"),
    "3. младший МП": ("_19", "_20", "_21", "_22", "_23", "_24", "_25", "_26", "_27"),
    "4. прочие": ("_28", "_29", "_30", "_31", "_32", "_33", "_34", "_35", "_36"),
}

prevalent_mp = SQL_otchet(
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
