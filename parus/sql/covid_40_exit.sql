SELECT org, day
    FROM(
    SELECT
      i.CODE pokazatel,
      ro.NUMB row_index,
      CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
           WHEN DATEVAL IS NOT NULL THEN to_char(DATEVAL, 'DD.MM.YYYY')
      ELSE NULL END value
    FROM PARUS.BLTBLVALUES v
        INNER JOIN PARUS.BLTABLESIND si
            on(v.BLTABLESIND = si.RN)
        INNER JOIN PARUS.BALANCEINDEXES i
            on(si.BALANCEINDEXES = i.RN)
        INNER JOIN PARUS.BLTBLROWS ro
            on(v.PRN = ro.RN)
        INNER JOIN PARUS.BLSUBREPORTS s
            on(ro.PRN = s.RN)
        INNER JOIN PARUS.BLREPORTS r
            on(s.PRN = r.RN)
        INNER JOIN PARUS.AGNLIST a
            on(r.AGENT = a.RN)
        INNER JOIN PARUS.BLREPFORMED rd
            on(r.BLREPFORMED = rd.RN)
        INNER JOIN PARUS.BLREPFORM rf
            on(rd.PRN = rf.RN)
    WHERE rf.code = '40 COVID вышли'
        and r.BDATE = to_date('13.09.2022','dd.mm.yyyy' )
        and a.AGNNAME = 'СПб ГБУЗ "Медицинский информационно-аналитический центр"'
    )
        pivot(
            max(value)
            FOR POKAZATEL IN ('40 COVID org' org, '40 COVID org date' day))
