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
WHERE rf.CODE = 'РодовспоможениеРДДет'
and bi.CODE in (
    'rddet_01', 'rddet_02', 'rddet_03', 'rddet_04', 'rddet_05', 'rddet_06',
    'rddet_07', 'rddet_08', 'rddet_09', 'rddet_10', 'rddet_11', 'rddet_12',
    'rddet_13', 'rddet_14', 'rddet_15', 'rddet_16', 'rddet_17', 'rddet_18'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "1. Генерализованные формы ГСИ у новорожденных": ("_01", "_02"),
    "2. Локализованные формы ГСИ у новорожденных ВСЕГО": ("_03", "_04"),
    "3. Инфекция кожи": ("_05", "_06"),
    "4. Инфекция подкожной клетчатки": ("_07", "_08"),
    "5. Инфекция в области пупка (омфалит)": ("_09", "_10"),
    "6. Инфекция слизистых оболочек глаза (конъюнктивит, дакриоцистит)": ("_11", "_12"),
    "7. Другие локализованные формы ГСИ у новорожденных ": ("_13", "_14"),
    "8. Всего новорожденных с генерализованными формами ГСИ": ("_15", "_16"),
    "9. Всего новорожденных с локализованными формами ГСИ": ("_17", "_18"),
}
rows = {
    "1. у новорожденных (до 28 суток)": (
        "_01",
        "_03",
        "_05",
        "_07",
        "_09",
        "_11",
        "_13",
        "_15",
        "_17",
    ),
    "1.  внутрибольничные случаи": (
        "_02",
        "_04",
        "_06",
        "_08",
        "_10",
        "_12",
        "_14",
        "_16",
        "_18",
    ),
}

obstetrics_3 = SQL_otchet(
    filename="/tmp/Родовспоможение.xlsx",
    sql=sql,
    columns=columns,
    cols_name="Нозологические формы",
    rows=rows,
    rows_name="Количество случаев ГСИ",
    del_col=[],
    pivot={
        "index": ["ORGANIZATION", "Количество случаев ГСИ"],
        "columns": ["Нозологические формы"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
