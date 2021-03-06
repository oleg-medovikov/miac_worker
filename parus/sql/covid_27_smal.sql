SELECT 
	to_char(r.BDATE, 'DD.MM.YYYY') day,
    SYSDATE time,
	a.RN ORGANIZATION_ID,
	a.AGNNAME ORGANIZATION ,
	rf.CODE  otchet,
	bi.CODE  pokazatel,
	bi.NAME pokazatel_name,
    CASE WHEN STRVAL IS NOT NULL THEN STRVAL 
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
WHERE rf.CODE = '27 COVID19' 
and r.BDATE between  to_date('2021-01-01','yyyy-mm-dd') AND  trunc(SYSDATE) - 1
and bi.CODE IN ('labCOVID_17','labCOVID_18', 'labCOVID_19', 'labCOVID_20') 
--and bi.CODE IN ('labCOVID_17','labCOVID_18','labCOVID_19','labCOVID_18_21_1','labCOVID_18_21') --заменено 09.12.2021
