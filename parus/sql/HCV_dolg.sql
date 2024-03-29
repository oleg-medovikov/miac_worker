SELECT
    to_char(r.BDATE, 'DD.MM.YYYY') day,
    a.AGNNAME ORGANIZATION,
    d.STRVAL error
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
    WHERE rf.code = 'HCV'
		AND bi.CODE = 'HCV_Error'
