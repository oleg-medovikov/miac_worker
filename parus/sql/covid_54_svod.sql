SELECT
  r.BDATE day,
  a.AGNNAME organization,
  i.CODE pokazatel,
  CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
    WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
    WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
    ELSE NULL END value
  FROM PARUS.BLTBLVALUES v
    INNER JOIN PARUS.BLTABLESIND si
    on(v.BLTABLESIND = si.RN)
    INNER JOIN (SELECT * FROM PARUS.BALANCEINDEXES
            WHERE CODE LIKE 'exp_test_%' ) i
    on(si.BALANCEINDEXES = i.RN)
    INNER JOIN (SELECT PRN, RN, NUMB  FROM  PARUS.BLTBLROWS  ) ro
    on(v.PRN = ro.RN)
    INNER JOIN PARUS.BLSUBREPORTS s
    on(ro.PRN = s.RN)
    INNER JOIN PARUS.BLREPORTS  r
    on(s.PRN = r.RN)
    INNER JOIN PARUS.AGNLIST a
    on(r.AGENT = a.RN)
    INNER JOIN PARUS.BLREPFORMED rd
    on(r.BLREPFORMED = rd.RN)
    INNER JOIN (SELECT * FROM PARUS.BLREPFORM
            WHERE CODE = '54 COVID 19 NEW' ) rf
    on(rd.PRN = rf.RN)
    INNER JOIN (SELECT to_char(MAX(DAY), 'DD.MM.YYYY')  DAY
                  ,RN
            FROM (   SELECT r.BDATE DAY
                  ,a.RN
                FROM PARUS.BLSUBREPORTS s
                  INNER JOIN PARUS.BLREPORTS r
                    ON (s.PRN = r.RN)
                  INNER JOIN PARUS.AGNLIST a
                    ON (r.AGENT = a.rn)
                  INNER JOIN PARUS.BLREPFORMED pf
                    ON (r.BLREPFORMED = pf.RN)
                  INNER JOIN PARUS.BLREPFORM rf
                    ON (pf.PRN = rf.RN)
                WHERE rf.code = '54 COVID 19 NEW'
                    AND r.BDATE <= trunc(SYSDATE)) dan1
            GROUP BY RN) maxDate
      ON (maxDate.DAY = r.BDATE
        AND maxDate.RN = a.RN)
      ORDER BY  day, organization, pokazatel
