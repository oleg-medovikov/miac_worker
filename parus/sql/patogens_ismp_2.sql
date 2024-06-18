SELECT r.BDATE,
        a.AGNNAME ORGANIZATION,
        a.AGN_COMMENT,
        rf.CODE  otchet,
        bi.CODE  pokazatel,
        CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
           WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
           WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
           ELSE NULL END value
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
WHERE rf.code = 'Ф2 Всп. ИнфЗаб ИСМП'
        and  r.BDATE = (SELECT max(r.BDATE)
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
                            WHERE rf.code = 'Ф2 Всп. ИнфЗаб ИСМП')
