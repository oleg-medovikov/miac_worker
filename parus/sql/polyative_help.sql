SELECT DAY, organization,
		    nvl(pok01, 'Итого по организации') pok01, nvl(cast(pok02 as int),0) pok02,
	      nvl(cast(pok03 as int),0) pok03, nvl(cast(pok04 as int),0) pok04,
        nvl(cast(pok05 as int),0) pok05, nvl(cast(pok06 as int),0) pok06,
        nvl(cast(pok07 as int),0) pok07, nvl(cast(pok08 as int),0) pok08,
        nvl(cast(pok09 as int),0) pok09, nvl(cast(pok10 as int),0) pok10,
        nvl(cast(pok11 as int),0) pok11, nvl(cast(pok12 as int),0) pok12,
        nvl(cast(pok13 as int),0) pok13, nvl(cast(pok14 as int),0) pok14,
        nvl(cast(pok15 as int),0) pok15, nvl(cast(pok16 as int),0) pok16,
        nvl(cast(pok17 as int),0) pok17, nvl(cast(pok18 as int),0) pok18,
        nvl(cast(pok19 as int),0) pok19, nvl(cast(pok20 as int),0) pok20
FROM 
	(SELECT
		to_char(r.BDATE, 'DD.MM.YYYY') day,
		a.AGNNAME organization,
	    i.CODE pokazatel,
	    ro.NUMB row_index ,
	CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
	         WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
	         WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
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
	    	WHERE rf.code = 'Паллиативнаяпом'
	    	AND r.BDATE = (SELECT max(r.BDATE) 
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
	            WHERE rf.CODE = 'Паллиативнаяпом' AND r.BDATE <  trunc(SYSDATE + 5)
	    		)
	)
pivot
(
	MIN(value)
FOR POKAZATEL IN (
		'palpm_01' pok01, 'palpm_02' pok02, 'palpm_03' pok03, 'palpm_04' pok04, 'palpm_05' pok05,
		'palpm_06' pok06, 'palpm_07' pok07, 'palpm_08' pok08, 'palpm_09' pok09, 'palpm_10' pok10,
		'palpm_11' pok11, 'palpm_12' pok12, 'palpm_13' pok13, 'palpm_14' pok14, 'palpm_15' pok15,
		'palpm_16' pok16, 'palpm_17' pok17, 'palpm_18' pok18, 'palpm_19' pok19, 'palpm_20' pok20
		)
)
