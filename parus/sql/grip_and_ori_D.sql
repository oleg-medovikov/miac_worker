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
    WHERE rf.code = 'ДиагнГриппаОРИ'
        AND  r.BDATE = TO_DATE('__DAY__','DD.MM.YYYY')
        AND  bi.CODE in (
            'table_34', 'table_35', 'table_36', 'table_37',
            'table_38', 'table_39'
            )
