SELECT DAY, ORGANIZATION,
		nvl(cast(pok01 as int),0) pok01,nvl(cast(pok02 as int),0) pok02,
	    nvl(cast(pok03 as int),0) pok03,nvl(cast(pok04 as int),0) pok04,
        nvl(cast(pok05 as int),0) pok05,nvl(cast(pok06 as int),0) pok06,
        nvl(cast(pok07 as int),0) pok07,nvl(cast(pok08 as int),0) pok08,
        nvl(cast(pok09 as int),0) pok09,nvl(cast(pok10 as int),0) pok10,
        nvl(cast(pok11 as int),0) pok11,nvl(cast(pok12 as int),0) pok12,
        nvl(cast(pok13 as int),0) pok13,nvl(cast(pok14 as int),0) pok14,
        nvl(cast(pok15 as int),0) pok15,nvl(cast(pok16 as int),0) pok16,
        nvl(cast(pok17 as int),0) pok17,nvl(cast(pok18 as int),0) pok18,
        nvl(cast(pok19 as int),0) pok19,nvl(cast(pok20 as int),0) pok20,
        nvl(cast(pok21 as int),0) pok21,nvl(cast(pok22 as int),0) pok22,
        nvl(cast(pok23 as int),0) pok23,nvl(cast(pok24 as int),0) pok24,
        nvl(cast(pok25 as int),0) pok25,nvl(cast(pok26 as int),0) pok26,
        nvl(cast(pok27 as int),0) pok27,nvl(cast(pok28 as int),0) pok28,
        nvl(cast(pok29 as int),0) pok29,nvl(cast(pok30 as int),0) pok30,
        nvl(cast(pok31 as int),0) pok31,nvl(cast(pok32 as int),0) pok32,
        nvl(cast(pok33 as int),0) pok33,nvl(cast(pok34 as int),0) pok34,
        nvl(cast(pok35 as int),0) pok35,nvl(cast(pok36 as int),0) pok36,
        nvl(cast(pok37 as int),0) pok37,nvl(cast(pok38 as int),0) pok38,
        nvl(cast(pok39 as int),0) pok39,nvl(cast(pok40 as int),0) pok40,
        nvl(cast(pok41 as int),0) pok41,nvl(cast(pok42 as int),0) pok42,
        nvl(cast(pok43 as int),0) pok43,nvl(cast(pok44 as int),0) pok44,
        nvl(cast(pok45 as int),0) pok45,nvl(cast(pok46 as int),0) pok46,
        nvl(cast(pok47 as int),0) pok47,nvl(cast(pok48 as int),0) pok48,
        nvl(cast(pok49 as int),0) pok49,nvl(cast(pok50 as int),0) pok50,
        nvl(cast(pok51 as int),0) pok51,nvl(cast(pok52 as int),0) pok52,
        nvl(cast(pok53 as int),0) pok53,nvl(cast(pok54 as int),0) pok54,
        nvl(cast(pok55 as int),0) pok55,nvl(cast(pok56 as int),0) pok56
FROM (
SELECT
    to_char(r.BDATE, 'DD.MM.YYYY') day,
    a.AGNNAME ORGANIZATION,
    rf.CODE  otchet,
    bi.CODE  pokazatel,
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
WHERE rf.CODE = 'МП ветеранам СВО'
	AND r.BDATE =  (SELECT max(r.BDATE) FROM PARUS.BLINDEXVALUES  d
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
							WHERE rf.CODE = 'МП ветеранам СВО' AND r.BDATE <  trunc(SYSDATE + 5)
							))
pivot
(
MIN(value)
FOR POKAZATEL IN ( 
	'MP_SVO_1_01' pok01, 'MP_SVO_4_01' pok02, 'MP_SVO_1_02' pok03, 'MP_SVO_4_02' pok04, 
	'MP_SVO_1_03' pok05, 'MP_SVO_4_03' pok06, 'MP_SVO_1_04' pok07, 'MP_SVO_4_04' pok08,
	'MP_SVO_1_05' pok09, 'MP_SVO_4_05' pok10, 'MP_SVO_1_06' pok11, 'MP_SVO_4_06' pok12,
	'MP_SVO_2_01' pok13, 'MP_SVO_5_01' pok14, 'MP_SVO_2_02' pok15, 'MP_SVO_5_02' pok16,
	'MP_SVO_2_03' pok17, 'MP_SVO_5_03' pok18, 'MP_SVO_2_04' pok19, 'MP_SVO_5_04' pok20,
	'MP_SVO_2_05' pok21, 'MP_SVO_5_05' pok22, 'MP_SVO_2_06' pok23, 'MP_SVO_5_06' pok24,
	'MP_SVO_1_07' pok25, 'MP_SVO_4_07' pok26, 'MP_SVO_1_08' pok27, 'MP_SVO_4_08' pok28,
	'MP_SVO_1_09' pok29, 'MP_SVO_4_09' pok30, 'MP_SVO_1_10' pok31, 'MP_SVO_4_10' pok32,
	'MP_SVO_1_11' pok33, 'MP_SVO_4_11' pok34, 'MP_SVO_2_07' pok35, 'MP_SVO_5_07' pok36,
	'MP_SVO_2_08' pok37, 'MP_SVO_5_08' pok38, 'MP_SVO_2_09' pok39, 'MP_SVO_5_09' pok40,
	'MP_SVO_2_10' pok41, 'MP_SVO_5_10' pok42, 'MP_SVO_2_11' pok43, 'MP_SVO_5_11' pok44,
	'MP_SVO_1_12' pok45, 'MP_SVO_4_12' pok46, 'MP_SVO_1_13' pok47, 'MP_SVO_4_13' pok48,
	'MP_SVO_1_14' pok49, 'MP_SVO_4_14' pok50, 'MP_SVO_2_12' pok51, 'MP_SVO_5_12' pok52,
	'MP_SVO_2_13' pok53, 'MP_SVO_5_13' pok54, 'MP_SVO_2_14' pok55, 'MP_SVO_5_14' pok56
)
)
