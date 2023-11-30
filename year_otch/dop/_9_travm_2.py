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
    'travm2_01', 'travm2_02', 'travm2_03',
    'travm2_04', 'travm2_05', 'travm2_06',
    'travm2_07', 'travm2_08'
)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""
pokazatel = {
    "travm2_01": "1. Число травмированных лиц, подлежащих вакцинации против гепатита В (непривитых до травматизации)",
    "travm2_02": "2. Число травмированных лиц, вакцинированных против гепатита В в связи с травмой",
    "travm2_03": "3. Число травмированных лиц, подлежащих ревакцинации против гепатита В (неревакцинированных до травмы)",
    "travm2_04": "4. Число травмированных лиц, ревакцинированных против гепатита В в связи с травмой",
    "travm2_05": "5. Число лиц, травмированных от ВИЧ-инфицированного пациента",
    "travm2_06": "6. Число лиц, травмированных от ВИЧ-инфицированного пациента, пролеченных против ВИЧ-инфекции",
    "travm2_07": "7. Число лиц, травмированных от больного с неизвестным ВИЧ-статусом (с высоким риском инфицирования)",
    "travm2_08": "8. Число лиц, травмированных от больного с неизвестным ВИЧ-статусом и пролеченных против ВИЧ-инфекции",
}


travm_2 = SQL_otchet(
    filename="/tmp/Охрана_Здоровья.xlsx",
    sql=sql,
    del_col=[],
    pivot={
        "index": [
            "ORGANIZATION",
        ],
        "columns": ["POKAZATEL"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
