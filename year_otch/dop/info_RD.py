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
WHERE rf.CODE = 'ИнфконтрольРД'
and bi.CODE in ('pokd_01', 'pokd_02', 'pokd_03', 'pokd_04',
       'pokd_05', 'pokd_06', 'pokd_07', 'pokd_08',
       'pokd_09', 'pokd_10', 'pokd_11', 'pokd_12',
       'pokd_13', 'pokd_14', 'pokd_15')
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""

pokazatel = {
    "pokd_01": "01. Количество коек ВСЕГО",
    "pokd_02": "02. Количество хирургических коек",
    "pokd_03": "03. Количество реанимационных коек",
    "pokd_04": "04. Количество пациентов, поступивших в стационар в отчетном периоде",
    "pokd_05": "05. Количество пациентов, выписанных / переведенных из стационара в отчетном периоде",
    "pokd_06": "06. Количество пациентов, умерших в стационаре в отчетном периоде",
    "pokd_07": "07. Количество пользованных пациентов ВСЕГО",
    "pokd_08": "08. Количество пользованных пациентов хирургических отделений",
    "pokd_09": "09. Количество пользованных пациентов реанимационных отделений",
    "pokd_10": "10. Количество отделений в стационаре ВСЕГО",
    "pokd_11": "11. Количество хирургических отделений  в стационаре",
    "pokd_12": "12. Количество реанимационных отделений в стационаре",
    "pokd_13": "13. Количество новорожденных, родившихся живыми, недоношенных",
    "pokd_14": "14. Количество пользованных пациентов отделений реанимации родильниц",
    "pokd_15": "15. Количество пользованных пациентов отделений реанимации новорожденных",
}

info_RD = SQL_otchet(
    filename="/tmp/Инфконтроль_РД.xlsx",
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
