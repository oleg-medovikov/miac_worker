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
WHERE rf.CODE = 'ИнфконтрольОБЩ'
and bi.CODE in (
    'faktr_01', 'faktr_02', 'faktr_03', 'faktr_04', 
    'faktr_05', 'faktr_06', 'faktr_07', 'faktr_08',
    'faktr_09', 'faktr_10', 'faktr_11', 'faktr_12'
    )
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

pokazatel = {
    "faktr_01": "01. Количество пациентов, которым осуществлялась искусственная вентиляция легких ВСЕГО",
    "faktr_02": "02. Количество ИВЛ-дней ВСЕГО",
    "faktr_03": "03. Количество пациентов ОРИТ, которым осуществлялась искусственная вентиляция легких",
    "faktr_04": "04. Количество ИВЛ-дней в ОРИТ",
    "faktr_05": "05. Количество пациентов, которым осуществлялась постановка мочевых катетеров ВСЕГО",
    "faktr_06": "06. Количество мочевых катетеро-дней ВСЕГО",
    "faktr_07": "07. Количество пациентов ОРИТ, которым осуществлялась постановка мочевых катетеров",
    "faktr_08": "08. Количество мочевых катетеро-дней в ОРИТ",
    "faktr_09": "09. Количество пациентов, которым осуществлялась постановка центральных венозных и подключичных катетеров ВСЕГО",
    "faktr_10": "10. Количество катетеро-дней (центральные венозные и подключичные катетеры) ВСЕГО",
    "faktr_11": "11. Количество пациентов ОРИТ, которым осуществлялась постановка центральных венозных и подключичных катетеров",
    "faktr_12": "12. Количество катетеро-дней (центральные венозные и подключичные катетеры) в ОРИТ",
}

risk_factor_GEN = SQL_otchet(
    filename="/tmp/Инфконтроль_ОБЩ.xlsx",
    sql=sql,
    pokazatel=pokazatel,
    del_col=["level_1"],
    pivot={
        "index": ["ORGANIZATION"],
        "columns": ["POKAZATEL"],
        "values": ["VALUE"],
        "aggfunc": "first",
    },
)
