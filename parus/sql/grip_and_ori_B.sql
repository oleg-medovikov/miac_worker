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
        AND  r.BDATE =  TO_DATE('__DAY__','DD.MM.YYYY')
        AND  bi.CODE in (
            'table_sum_02', 'table_sum_03', 'table_06', 'table_07', 
            'table_08', 'table_09', 'table_10', 'table_11', 'table_12',
            'table_13', 'table_14', 'table_15', 'table_16', 'table_17',
            'table_18', 'table_19', 'table_20', 'table_21', 'table_22',
            'table_23', 'table_24', 'table_25', 'table_26', 'table_27', 
            'table_28', 'table_29', 'table_30', 'table_31', 'table_31.1',
            'table_31.2', 'table_32', 'table_33'
                )
