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
    'gepmr_01', 'gepmr_02', 'gepmr_03', 'gepmr_04', 'gepmr_05', 'gepmr_06',
    'gepmr_07', 'gepmr_08', 'gepmr_09', 'gepmr_10', 'gepmr_11', 'gepmr_12',
    'gepmr_13', 'gepmr_14', 'gepmr_15', 'gepmr_16', 'gepmr_17', 'gepmr_18',
    'gepmr_19', 'gepmr_20', 'gepmr_21', 'gepmr_22', 'gepmr_23', 'gepmr_24',
    'gepmr_25', 'gepmr_26', 'gepmr_27', 'gepmr_28', 'gepmr_29', 'gepmr_30',
    'gepmr_31', 'gepmr_32', 'gepmr_33', 'gepmr_34', 'gepmr_35', 'gepmr_36'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

columns = {
    "1. заболевших острым вирусным гепатитом А в отчетном году": (
        "_01",
        "_10",
        "_19",
        "_28",
    ),
    "2. заболевших острым вирусным гепатитом В в отчетном году": (
        "_02",
        "_11",
        "_20",
        "_29",
    ),
    "3. заболевших острым вирусным гепатитом С в отчетном году": (
        "_03",
        "_12",
        "_21",
        "_30",
    ),
    "4. заболевших хронических вирусным гепатитом В в отчетном году": (
        "_04",
        "_13",
        "_22",
        "_31",
    ),
    "5. заболевших хронических вирусным гепатитом С в отчетном году": (
        "_05",
        "_14",
        "_23",
        "_32",
    ),
    "6. заболевших ХВГВ +ХВГС": ("_06", "_14", "_24", "_33"),
    '7. являющихся "носителями" Анти-HCV с отчетного года': (
        "_07",
        "_15",
        "_25",
        "_34",
    ),
    '8. являющихся "носителями" HBsAg с отчетного года': ("_08", "_16", "_26", "_35"),
    '9. являющихся "носителями" HBsAg с отчетного года': ("_09", "_17", "_27", "_36"),
}
rows = {
    "1. врачи": ("_01", "_02", "_03", "_04", "_05", "_06", "_07", "_08", "_09"),
    "2. средний МП": ("_10", "_11", "_12", "_13", "_14", "_15", "_16", "_17", "_18"),
    "3. младший МП": ("_19", "_20", "_21", "_22", "_23", "_24", "_25", "_26", "_27"),
    "4. прочие": ("_28", "_29", "_30", "_31", "_32", "_33", "_34", "_35", "_36"),
}

gepatit_mp = SQL_otchet(
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
