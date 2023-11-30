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
    'rddop2_01', 'rddop2_02', 'rddop2_03', 'rddop2_04', 'rddop2_05', 'rddop2_06',
    'rddop2_07', 'rddop2_08', 'rddop2_09', 'rddop2_10', 'rddop2_11', 'rddop2_12',
    'rddop2_13', 'rddop2_14', 'rddop2_15', 'rddop2_16', 'rddop2_17', 'rddop2_18',
    'rddop2_19', 'rddop2_20', 'rddop2_21', 'rddop2_22', 'rddop2_23', 'rddop2_24',
    'rddop2_25', 'rddop2_26', 'rddop2_27', 'rddop2_28', 'rddop2_29', 'rddop2_30',
    'rddop2_31', 'rddop2_32', 'rddop2_33', 'rddop2_34', 'rddop2_35', 'rddop2_36',
    'rddop2_37', 'rddop2_38', 'rddop2_39', 'rddop2_40', 'rddop2_41', 'rddop2_42',
    'rddop2_43', 'rddop2_44', 'rddop2_45', 'rddop2_46', 'rddop2_47', 'rddop2_48',
    'rddop2_49', 'rddop2_50', 'rddop2_51', 'rddop2_52'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "01. Генерализованные формы ГСИ у родильниц": ("_01", "_02", "_03", "_04"),
    "02. Локализованные формы ГСИ у родильниц ВСЕГО": ("_05", "_06", "_07", "_08"),
    "03. Эндометриты ВСЕГО": ("_09", "_10", "_11", "_12"),
    "04. Эндометриты после Кесарева сечения": ("_13", "_14", "_15", "_16"),
    "05. Маститы гнойные": ("_17", "_18", "_19", "_20"),
    "06. Маститы серозные": ("_21", "_22", "_23", "_24"),
    "07. Расхождение швов после Кесарева сечения": ("_25", "_26", "_27", "_28"),
    "08. Гематома акушерской хирургической раны": ("_29", "_30", "_31", "_32"),
    "09. Расхождение швов промежности": ("_33", "_34", "_35", "_36"),
    "10. Абсцессы": ("_37", "_38", "_39", "_40"),
    "11. Флегмоны": ("_41", "_42", "_43", "_44"),
    "12. Флебиты": ("_45", "_46", "_47", "_48"),
    "13. Другие ГСИ": ("_49", "_50", "_51", "_52"),
}
rows = {
    "1. Всего": (
        "_01",
        "_05",
        "_09",
        "_13",
        "_17",
        "_21",
        "_25",
        "_29",
        "_33",
        "_37",
        "_41",
        "_45",
        "_49",
    ),
    "2. в стационаре": (
        "_02",
        "_06",
        "_10",
        "_14",
        "_18",
        "_22",
        "_26",
        "_30",
        "_34",
        "_38",
        "_42",
        "_46",
        "_50",
    ),
    "3. после выписки первые 10 суток": (
        "_03",
        "_07",
        "_11",
        "_15",
        "_19",
        "_23",
        "_27",
        "_31",
        "_35",
        "_39",
        "_43",
        "_47",
        "_51",
    ),
    "4. после выписки более 10 суток": (
        "_04",
        "_08",
        "_12",
        "_16",
        "_20",
        "_24",
        "_28",
        "_32",
        "_36",
        "_40",
        "_44",
        "_48",
        "_52",
    ),
}

obstetrics_2 = SQL_otchet(
    filename="/tmp/Родовспоможение.xlsx",
    sql=sql,
    columns=columns,
    cols_name="Нозологические формы",
    rows=rows,
    rows_name="Количество случаев  ВБИ, выявленных у родильниц",
    del_col=[],
    pivot={
        "index": ["ORGANIZATION", "Количество случаев  ВБИ, выявленных у родильниц"],
        "columns": ["Нозологические формы"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
