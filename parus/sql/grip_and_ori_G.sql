SELECT
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
    WHERE rf.code = 'ДиагнГриппаОРИ'
        AND  r.BDATE = TO_DATE('__DAY__','DD.MM.YYYY')
        AND  bi.CODE in ('table_43', 'table_44', 'table_45', 'table_46', 'table_47', 'table_48', 'table_49', 'table_50', 'table_51', 'table_52', 'table_53', 'table_54', 'table_55', 'table_56', 'table_57', 'table_58', 'table_59', 'table_60', 'table_61', 'table_62')
