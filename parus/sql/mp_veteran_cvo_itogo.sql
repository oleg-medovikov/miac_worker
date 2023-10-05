SELECT
    bi.CODE  pokazatel,
    sum(NUMVAL) as value
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
WHERE rf.CODE = 'МП ветеранам СВО'
    and NUMVAL is not null
    and  REGEXP_LIKE(bi.code, 'MP_SVO_(1|2|4|5)_*')
    AND r.BDATE = (SELECT max(r.BDATE)
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
                WHERE rf.CODE = 'МП ветеранам СВО' AND r.BDATE <  trunc(SYSDATE + 5))
    group by bi.CODE
