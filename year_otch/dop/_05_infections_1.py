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
WHERE rf.CODE = 'ТрадицНРД'
and bi.CODE in (
    'infnrod_01', 'infnrod_02', 'infnrod_03', 'infnrod_04', 'infnrod_05', 'infnrod_06',
    'infnrod_07', 'infnrod_08', 'infnrod_09', 'infnrod_10', 'infnrod_11', 'infnrod_12',
    'infnrod_13', 'infnrod_14', 'infnrod_15', 'infnrod_16', 'infnrod_17', 'infnrod_18',
    'infnrod_19', 'infnrod_20', 'infnrod_21', 'infnrod_22', 'infnrod_23', 'infnrod_24',
    'infnrod_25', 'infnrod_26', 'infnrod_27', 'infnrod_28', 'infnrod_29', 'infnrod_30',
    'infnrod_31', 'infnrod_32', 'infnrod_33', 'infnrod_34', 'infnrod_35', 'infnrod_36',
    'infnrod_37', 'infnrod_38', 'infnrod_39', 'infnrod_40', 'infnrod_41', 'infnrod_42',
    'infnrod_43', 'infnrod_44', 'infnrod_45', 'infnrod_46', 'infnrod_47', 'infnrod_48'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "01. Брюшной тиф": ("_01", "_02", "_03"),
    "02. Паратиф А, Б, С": ("_04", "_05", "_06"),
    "03. Бактерионосительство возбудителя брюшного тифа, паратифов": (
        "_07",
        "_08",
        "_09",
    ),
    "04. Сальмонеллез": ("_10", "_11", "_12"),
    "05. Бактерионосительство возбудителя сальмонеллеза": ("_13", "_14", "_15"),
    "06. Холера": ("_16", "_17", "_18"),
    "07. Вибрионосительство возбудителя холеры": ("_19", "_20", "_21"),
    "08. Бактериальная дизентерия ВСЕГО": ("_22", "_23", "_24"),
    "09. Бактериальная дизентерия, вызванная шигеллами Зонне": ("_25", "_26", "_27"),
    "10. Бактериальная дизентерия, вызванная шигеллами Флекснер": ("_28", "_29", "_30"),
    "11. Бактериальная дизентерия": ("_31", "_32", "_33"),
    "12. ОКИ, вызванные установленными  возбудителями  ВСЕГО": ("_34", "_35", "_36"),
    "13. ОКИ, вызванные энтеропатогенными кишечными палочками": ("_37", "_38", "_39"),
    "14. Энтеровирусная инфекция  ВСЕГО": ("_40", "_41", "_42"),
    "15. Энтеровирусный менингит": ("_43", "_44", "_45"),
    "16. ОКИ, вызванные неустановленными  возбудителями": ("_46", "_47", "_48"),
}

rows = {
    "1. заноса Инф.З.": (
        "_01",
        "_04",
        "_07",
        "_10",
        "_13",
        "_16",
        "_19",
        "_22",
        "_25",
        "_28",
        "_31",
        "_34",
        "_37",
        "_40",
        "_43",
        "_46",
    ),
    "2. внутрибольничных Инф.З.": (
        "_02",
        "_05",
        "_08",
        "_11",
        "_14",
        "_17",
        "_20",
        "_23",
        "_26",
        "_29",
        "_32",
        "_35",
        "_38",
        "_41",
        "_44",
        "_47",
    ),
    "3. очагов с 2 и более Инф.З.": (
        "_03",
        "_06",
        "_09",
        "_12",
        "_15",
        "_18",
        "_21",
        "_24",
        "_27",
        "_30",
        "_33",
        "_36",
        "_39",
        "_42",
        "_45",
        "_48",
    ),
}

infections_1 = SQL_otchet(
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
