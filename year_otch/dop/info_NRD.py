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
WHERE rf.CODE = 'ИнфконтрольНРД'
and bi.CODE in ('pokdnrd_01', 'pokdnrd_02', 'pokdnrd_03', 'pokdnrd_04',
       'pokdnrd_05', 'pokdnrd_06', 'pokdnrd_07', 'pokdnrd_08',
       'pokdnrd_09', 'pokdnrd_10', 'pokdnrd_11', 'pokdnrd_12',
       'pokdnrd_13', 'pokdnrd_14', 'pokdnrd_15')
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

pokazatel = {
    "pokdnrd_01": "01. Количество коек ВСЕГО",
    "pokdnrd_02": "02. Количество хирургических коек",
    "pokdnrd_03": "03. Количество реанимационных коек",
    "pokdnrd_04": "04. Количество пациентов, поступивших в стационар в отчетном периоде",
    "pokdnrd_05": "05. Количество пациентов, выписанных / переведенных из стационара в отчетном периоде",
    "pokdnrd_06": "06. Количество пациентов, умерших в стационаре в отчетном периоде",
    "pokdnrd_07": "07. Количество пользованных пациентов ВСЕГО",
    "pokdnrd_08": "08. Количество пользованных пациентов хирургических отделений",
    "pokdnrd_09": "09. Количество пользованных пациентов реанимационных отделений",
    "pokdnrd_10": "10. Количество отделений в стационаре ВСЕГО",
    "pokdnrd_11": "11. Количество хирургических отделений  в стационаре",
    "pokdnrd_12": "12. Количество реанимационных отделений в стационаре",
    "pokdnrd_13": "13. Количество новорожденных, родившихся живыми, недоношенных",
    "pokdnrd_14": "14. Количество пользованных  пациентов отделений реанимации родильниц",
    "pokdnrd_15": "15. Количество пользованных  пациентов отделений реанимации новорожденных",
}

info_NRD = SQL_otchet(
    filename="/tmp/Инфконтроль_НРД.xlsx",
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
