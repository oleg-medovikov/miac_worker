SELECT  day, pok01,
    nvl(cast(pok02 as int),0)  pok02,nvl(cast(pok03 as int),0)  pok03
FROM (
        SELECT
            to_char(r.BDATE, 'YYYY_MM_DD') day,
            i.CODE pokazatel,
            a.AGNNAME organization,
            ro.NUMB row_index,
            CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
                WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
                WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
                ELSE NULL END value,
            'Пункт вакцинации' type
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
            WHERE rf.code  = 'ЭкстренныеИзвещ'
        and r.BDATE =  (SELECT max(r.BDATE) FROM PARUS.BLTBLVALUES v
                                INNER JOIN PARUS.BLTBLROWS ro
                                on(v.PRN = ro.RN)
                                INNER JOIN PARUS.BLSUBREPORTS s
                                on(ro.PRN = s.RN)
                                INNER JOIN PARUS.BLREPORTS r
                                on(s.PRN = r.RN)
                                INNER JOIN PARUS.BLREPFORMED rd
                                on(r.BLREPFORMED = rd.RN)
                                INNER JOIN PARUS.BLREPFORM rf
                                on(rd.PRN = rf.RN)
                                WHERE rf.code = 'ЭкстренныеИзвещ' AND r.BDATE < trunc(SYSDATE) + 4  )
        and i.CODE in  ('ext_izv_01', 'ext_izv_02','ext_izv_03')
                )
        pivot
        (
        max(value)
        FOR POKAZATEL IN ('ext_izv_01' pok01, 'ext_izv_02' pok02, 'ext_izv_03' pok03)
        )
WHERE pok01 IS NOT NULL 
ORDER by DAY, organization
