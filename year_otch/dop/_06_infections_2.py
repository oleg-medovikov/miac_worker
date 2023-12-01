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
    'infnrod2_01', 'infnrod2_02', 'infnrod2_03', 'infnrod2_04', 'infnrod2_05', 'infnrod2_06',
    'infnrod2_07', 'infnrod2_08', 'infnrod2_09', 'infnrod2_10', 'infnrod2_11', 'infnrod2_12',
    'infnrod2_13', 'infnrod2_14', 'infnrod2_15', 'infnrod2_16', 'infnrod2_17', 'infnrod2_18',
    'infnrod2_19', 'infnrod2_20', 'infnrod2_21', 'infnrod2_22', 'infnrod2_23', 'infnrod2_24',
    'infnrod2_25', 'infnrod2_26', 'infnrod2_27', 'infnrod2_28', 'infnrod2_29', 'infnrod2_30',
    'infnrod2_31', 'infnrod2_32', 'infnrod2_33', 'infnrod2_34', 'infnrod2_35', 'infnrod2_36',
    'infnrod2_37', 'infnrod2_38', 'infnrod2_39', 'infnrod2_40', 'infnrod2_41', 'infnrod2_42',
    'infnrod2_43', 'infnrod2_44', 'infnrod2_45', 'infnrod2_46', 'infnrod2_47', 'infnrod2_48',
    'infnrod2_49', 'infnrod2_50', 'infnrod2_51'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "01. Дифтерия": ("_01", "_02", "_03"),
    "02. Бактерионосительство токсигенных штаммоф дифтерии": ("_04", "_05", "_06"),
    "03. Коклюш": ("_07", "_08", "_09"),
    "04. Скарлатина": ("_10", "_11", "_12"),
    "05. Ветряная оспа": ("_13", "_14", "_15"),
    "06. Эпидемический паротит": ("_16", "_17", "_18"),
    "07. Корь": ("_19", "_20", "_21"),
    "08. Краснуха": ("_22", "_23", "_24"),
    "09. Менингококковая инфекция": ("_25", "_26", "_27"),
    "10. Менингококкцемия, гнойный менингит": ("_28", "_29", "_30"),
    "11. Инфекционный мононуклеоз": ("_31", "_32", "_33"),
    "12. Грипп": ("_34", "_35", "_36"),
    "13. ОРЗ": ("_37", "_38", "_39"),
    "14. Туберкулез (все формы)": ("_40", "_41", "_42"),
    "15. Туберкулез органов дыхания": ("_43", "_44", "_45"),
    "16. Бациллярные формы туберкулеза органов дыхания": ("_46", "_47", "_48"),
    "17. Короновирусная инфекция COVID-19": ("_49", "_50", "_51"),
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
        "_49",
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
        "_50",
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
        "_51",
    ),
}

infections_2 = SQL_otchet(
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
