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
WHERE rf.CODE = 'ТрадицРД'
and bi.CODE in (
    'infrod_01', 'infrod_02', 'infrod_03', 'infrod_04', 'infrod_05', 'infrod_06',
    'infrod_07', 'infrod_08', 'infrod_09', 'infrod_10', 'infrod_11', 'infrod_12',
    'infrod_13', 'infrod_14', 'infrod_15', 'infrod_16', 'infrod_17', 'infrod_18',
    'infrod_19', 'infrod_20', 'infrod_21', 'infrod_22', 'infrod_23', 'infrod_24',
    'infrod_25', 'infrod_26', 'infrod_27', 'infrod_28', 'infrod_29', 'infrod_30',
    'infrod_31', 'infrod_32', 'infrod_33', 'infrod_34', 'infrod_35', 'infrod_36',
    'infrod_37', 'infrod_38', 'infrod_39', 'infrod_40', 'infrod_41', 'infrod_42',
    'infrod_43', 'infrod_44', 'infrod_45', 'infrod_46', 'infrod_47', 'infrod_48',
    'infrod_49', 'infrod_50', 'infrod_51', 'infrod_52', 'infrod_53', 'infrod_54',
    'infrod_55', 'infrod_56', 'infrod_57', 'infrod_58', 'infrod_59', 'infrod_60',
    'infrod_61', 'infrod_62', 'infrod_63', 'infrod_64', 'infrod_65', 'infrod_66',
    'infrod_67', 'infrod_68', 'infrod_69', 'infrod_70', 'infrod_71', 'infrod_72',
    'infrod_73', 'infrod_74', 'infrod_75', 'infrod_76', 'infrod_77', 'infrod_78',
    'infrod_79', 'infrod_80', 'infrod_81', 'infrod_82', 'infrod_83', 'infrod_84',
    'infrod_85'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "01. Брюшной тиф": ("_01", "_02", "_03", "_04", "_05"),
    "02. Паратиф А, В, С": ("_06", "_07", "_08", "_09", "_10"),
    "03. Бактерионосительство брюшного тифа, паратифов": (
        "_11",
        "_12",
        "_13",
        "_14",
        "_15",
    ),
    "04. Сальмонеллез": ("_16", "_17", "_18", "_19", "_20"),
    "05. Бактерионосительство сальмонеллеза": ("_21", "_22", "_23", "_24", "_25"),
    "06. Холера": ("_26", "_27", "_28", "_29", "_30"),
    "07. Вибрионосительство холеры": ("_31", "_32", "_33", "_34", "_35"),
    "08. Бактериальная дизентерия ВСЕГО": ("_36", "_37", "_38", "_39", "_40"),
    "09. Бактериальная дизентерия, вызванная шигеллами Зонне": (
        "_41",
        "_42",
        "_43",
        "_44",
        "_45",
    ),
    "10. Бактериальная дизентерия, вызванная шигеллами Флекснер": (
        "_46",
        "_47",
        "_48",
        "_49",
        "_50",
    ),
    "11. Бактерионосительство дизентерии": ("_51", "_52", "_53", "_54", "_55"),
    "12. ОКИ, вызванные установленными возбудителями ВСЕГО": (
        "_56",
        "_57",
        "_58",
        "_59",
        "_60",
    ),
    "13. ОКИ, вызванные энтеропатогенными кишечными палочками": (
        "_61",
        "_62",
        "_63",
        "_64",
        "_65",
    ),
    "14. Бактерионосительство энтеропатогенной кишечной палочки": (
        "_66",
        "_67",
        "_68",
        "_69",
        "_70",
    ),
    "15. Энтеровирусная инфекция ВСЕГО": ("_71", "_72", "_73", "_74", "_75"),
    "16. Энтеровирусный менингит": ("_76", "_77", "_78", "_79", "_80"),
    "17. ОКИ, вызванные неустановленными возбудителями": (
        "_81",
        "_82",
        "_83",
        "_84",
        "_85",
    ),
}

rows = {
    "1. ВСЕГО (до 28 суток)": (
        "_01",
        "_06",
        "_11",
        "_16",
        "_21",
        "_26",
        "_31",
        "_36",
        "_41",
        "_46",
        "_51",
        "_56",
        "_61",
        "_66",
        "_71",
        "_76",
        "_81",
    ),
    "2. занос (родильницы)": (
        "_02",
        "_07",
        "_12",
        "_17",
        "_22",
        "_27",
        "_32",
        "_37",
        "_42",
        "_47",
        "_52",
        "_57",
        "_62",
        "_67",
        "_72",
        "_77",
        "_82",
    ),
    "3. внутрибольничных у родильниц": (
        "_03",
        "_08",
        "_13",
        "_18",
        "_23",
        "_28",
        "_33",
        "_38",
        "_43",
        "_48",
        "_53",
        "_58",
        "_63",
        "_68",
        "_73",
        "_78",
        "_83",
    ),
    "4. внутрибольничных у новорожденных": (
        "_04",
        "_09",
        "_14",
        "_19",
        "_24",
        "_29",
        "_34",
        "_39",
        "_44",
        "_49",
        "_54",
        "_59",
        "_64",
        "_69",
        "_74",
        "_79",
        "_84",
    ),
    "5. с 2 или более очагов": (
        "_05",
        "_10",
        "_15",
        "_20",
        "_25",
        "_30",
        "_35",
        "_40",
        "_45",
        "_50",
        "_55",
        "_60",
        "_65",
        "_70",
        "_75",
        "_80",
        "_85",
    ),
}

infections_5 = SQL_otchet(
    filename="/tmp/Традиционные_инфекции.xlsx",
    sql=sql,
    columns=columns,
    cols_name="Нозологические формы",
    rows=rows,
    rows_name="Количество случаев инфекционных заболеваний",
    del_col=[],
    pivot={
        "index": ["ORGANIZATION", "Количество случаев инфекционных заболеваний"],
        "columns": ["Нозологические формы"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)