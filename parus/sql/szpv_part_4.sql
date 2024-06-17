SELECT
        a.AGNNAME ORGANIZATION,
        rf.CODE  otchet,
        bi.CODE  pokazatel,
        d.NUMVAL value
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
WHERE rf.code = 'СЗПВ'
 and  r.BDATE = ( SELECT max(r.BDATE) FROM PARUS.BLTBLVALUES v
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
				WHERE rf.code = 'СЗПВ'
                AND r.BDATE < trunc(SYSDATE) + 1 
                )
 AND  bi.CODE IN ('pos_01', 'pos_02', 'pos_03', 'pos_04','pos_06', 'pos_25', 'pos_26')
