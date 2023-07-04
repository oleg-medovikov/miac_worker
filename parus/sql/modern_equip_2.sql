SELECT
    to_char(r.BDATE, 'YYYY_MM_DD') day,
    a.AGNNAME ORGANIZATION,
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
    WHERE rf.CODE = 'МодернизацияОснащени'
        AND bi.CODE like 'ModOsnOb!_%' ESCAPE '!'
        AND r.BDATE =  (SELECT max(r.BDATE) FROM PARUS.BLINDEXVALUES  d
            INNER JOIN PARUS.BLSUBREPORTS s
            ON (d.PRN = s.RN)
            INNER JOIN PARUS.BLREPORTS r
            ON(s.PRN = r.RN)
            INNER JOIN PARUS.BLREPFORMED pf
            on(r.BLREPFORMED = pf.RN)
            INNER JOIN PARUS.BLREPFORM rf
            on(pf.PRN = rf.RN)
            WHERE rf.CODE = 'МодернизацияОснащени' AND r.BDATE <  trunc(SYSDATE + 5))
