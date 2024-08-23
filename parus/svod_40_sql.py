MNEMOKOD = "40 COVID 19"
# DATE_NEW = "trunc(SYSDATE - 1)"
# DATE_OLD = "trunc(SYSDATE - 2)"

START = "trunc(SYSDATE - 30)"
STOP = "trunc(SYSDATE + 5)"

SQL_VACHIN = f"""
SELECT
    to_char(r.BDATE, 'YYYY.MM.DD') day,
    bi.CODE pokazatel,
    a.AGNNAME ORGANIZATION,
    1 row_index,
        CASE WHEN STRVAL IS NOT NULL THEN STRVAL
         WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
         WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
    ELSE NULL END value,
    'Медицинская организация' type
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
    WHERE rf.code = '{MNEMOKOD}'
        AND  (bi.CODE not like '%_O' and
                    (bi.CODE like 'KOVIVAC%'
                    or bi.CODE like 'KONVASEL%'
                    or bi.CODE like 'CPUTNIKL%'
                    or bi.CODE like 'CPUTNIKV%'
                    or bi.CODE like 'EPIVAK%'
                    or bi.CODE in ('distr', 'org')
                    ))
        AND r.BDATE IN (
            SELECT dates
            FROM (
                SELECT DISTINCT r.BDATE AS dates
                FROM PARUS.BLINDEXVALUES d
                INNER JOIN PARUS.BLSUBREPORTS s ON (d.PRN = s.RN)
                INNER JOIN PARUS.BLREPORTS r ON (s.PRN = r.RN)
                INNER JOIN PARUS.BLREPFORMED pf ON (r.BLREPFORMED = pf.RN)
                INNER JOIN PARUS.BLREPFORM rf ON (pf.PRN = rf.RN)
                WHERE rf.CODE = '40 COVID 19'
                  AND r.BDATE BETWEEN {START} AND {STOP}
                ORDER BY r.BDATE DESC
            )
            WHERE ROWNUM <= 2
        )
UNION
SELECT
            to_char(r.BDATE, 'YYYY.MM.DD') day,
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
            WHERE rf.code =  '{MNEMOKOD}'
                and (i.CODE not like '%_O' and
                    (i.CODE like 'KOVIVAC%'
                    or i.CODE like 'KONVASEL%'
                    or i.CODE like 'CPUTNIKL%'
                    or i.CODE like 'CPUTNIKV%'
                    or i.CODE like 'EPIVAK%'
                    ))
                AND r.BDATE IN (
                    SELECT dates
                    FROM (
                        SELECT DISTINCT r.BDATE AS dates
                        FROM PARUS.BLINDEXVALUES d
                        INNER JOIN PARUS.BLSUBREPORTS s ON (d.PRN = s.RN)
                        INNER JOIN PARUS.BLREPORTS r ON (s.PRN = r.RN)
                        INNER JOIN PARUS.BLREPFORMED pf ON (r.BLREPFORMED = pf.RN)
                        INNER JOIN PARUS.BLREPFORM rf ON (pf.PRN = rf.RN)
                        WHERE rf.CODE = '40 COVID 19'
                          AND r.BDATE BETWEEN {START} AND {STOP}
                        ORDER BY r.BDATE DESC
                    )
                    WHERE ROWNUM <= 2
                )
"""

SQL_REVAC_MO = f"""
select DAY, 'Медицинская организация' AS tip, indx, ORGANIZATION, typevacine, scep,
    nvl(cast(pok_02 as int),0) pok_02, nvl(cast(pok_03 as int),0) pok_03,
    nvl(cast(pok_04 as int),0) pok_04, nvl(cast(pok_05 as int),0) pok_05,
    nvl(cast(pok_06 as int),0) pok_06, nvl(cast(pok_07 as int),0) pok_07,
    nvl(cast(pok_08 as int),0) pok_08, nvl(cast(pok_09 as int),0) pok_09,
    nvl(cast(pok_10 as int),0) pok_10, nvl(cast(pok_11 as int),0) pok_11,
    nvl(cast(pok_12 as int),0) pok_12, nvl(cast(pok_13 as int),0) pok_13,
    nvl(cast(pok_14 as int),0) pok_14, nvl(cast(pok_15 as int),0) pok_15,
    nvl(cast(pok_16 as int),0) pok_16, nvl(cast(pok_17 as int),0) pok_17,
    nvl(cast(pok_18 as int),0) pok_18, nvl(cast(pok_19 as int),0) pok_19
    from (
    SELECT
            to_char(r.BDATE, 'YYYY.MM.DD') day,
            a.AGNNAME ORGANIZATION,
            'индекс' indx,
            '' typevacine,
            '' scep,
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
        WHERE rf.code = '{MNEMOKOD}'
            and bi.CODE in (
                'revac_02_0индекс_s', 'revac_03_0индекс_s', 'revac_04_0индекс_s',
                'revac_05_0индекс_s', 'revac_06_0индекс_s', 'revac_07_0индекс_s',
                'revac_08_0индекс_s', 'revac_09_0индекс_s', 'revac_10_0индекс_s',
                'revac_11_0индекс_s', 'revac_12_0индекс_s', 'revac_13_0индекс_s',
                'revac_14_0индекс_s', 'revac_15_0индекс_s', 'revac_16_0индекс_s',
                'revac_17_0индекс_s', 'revac_18_0индекс_s', 'revac_19_0индекс_s'
                )
            AND r.BDATE IN (
                            SELECT dates
                            FROM (
                                SELECT DISTINCT r.BDATE AS dates
                                FROM PARUS.BLINDEXVALUES d
                                INNER JOIN PARUS.BLSUBREPORTS s ON (d.PRN = s.RN)
                                INNER JOIN PARUS.BLREPORTS r ON (s.PRN = r.RN)
                                INNER JOIN PARUS.BLREPFORMED pf ON (r.BLREPFORMED = pf.RN)
                                INNER JOIN PARUS.BLREPFORM rf ON (pf.PRN = rf.RN)
                                WHERE rf.CODE = '40 COVID 19'
                                  AND r.BDATE BETWEEN {START} AND {STOP}
                                ORDER BY r.BDATE DESC
                            )
                            WHERE ROWNUM <= 2
                        )
            )
        pivot
            (
            max(value)
                FOR POKAZATEL IN (
                'revac_02_0индекс_s' pok_02, 'revac_03_0индекс_s' pok_03, 'revac_04_0индекс_s' pok_04,
                'revac_05_0индекс_s' pok_05, 'revac_06_0индекс_s' pok_06, 'revac_07_0индекс_s' pok_07,
                'revac_08_0индекс_s' pok_08, 'revac_09_0индекс_s' pok_09, 'revac_10_0индекс_s' pok_10,
                'revac_11_0индекс_s' pok_11, 'revac_12_0индекс_s' pok_12, 'revac_13_0индекс_s' pok_13,
                'revac_14_0индекс_s' pok_14, 'revac_15_0индекс_s' pok_15, 'revac_16_0индекс_s' pok_16,
                'revac_17_0индекс_s' pok_17, 'revac_18_0индекс_s' pok_18, 'revac_19_0индекс_s' pok_19
                )
            )
"""

SQL_REVAC_TVSP = f"""SELECT  DAY, 'Пункт вакцинации' AS tip, 7 AS INDX, ORGANIZATION, revac as typevacine
		,REPLACE(substr(tvsp ,INSTR(tvsp , ' ')+1, length(tvsp)),'район ','') AS scep
		,nvl(cast(pok_02 as int),0) pok_02
		,nvl(cast(pok_03 as int),0) pok_03,nvl(cast(pok_04 as int),0) pok_04
		,nvl(cast(pok_05 as int),0) pok_05,nvl(cast(pok_06 as int),0) pok_06
		,nvl(cast(pok_07 as int),0) pok_07,nvl(cast(pok_08 as int),0) pok_08
		,nvl(cast(pok_09 as int),0) pok_09,nvl(cast(pok_10 as int),0) pok_10
		,nvl(cast(pok_11 as int),0) pok_11,nvl(cast(pok_12 as int),0) pok_12
		,nvl(cast(pok_13 as int),0) pok_13,nvl(cast(pok_14 as int),0) pok_14
		,nvl(cast(pok_15 as int),0) pok_15,nvl(cast(pok_16 as int),0) pok_16
		,nvl(cast(pok_17 as int),0) pok_17,nvl(cast(pok_18 as int),0) pok_18
		,nvl(cast(pok_19 as int),0) pok_19
		FROM (
        SELECT
            r.BDATE day,
            --to_char(r.BDATE, 'YYYY.MM.DD') day,
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
        WHERE rf.code = '{MNEMOKOD}'
			and i.CODE in ( 
            'tvsp_revac','vak_revac','revac_02_01','revac_03_01','revac_04_01',
			'revac_05_01','revac_06_01','revac_07_01','revac_08_01','revac_09_01',
			'revac_10_01','revac_11_01','revac_12_01','revac_13_01','revac_14_01',
			'revac_15_01','revac_16_01','revac_17_01','revac_18_01','revac_19_01'
			)
            AND r.BDATE IN (
                SELECT dates
                FROM (
                    SELECT DISTINCT r.BDATE AS dates
                    FROM PARUS.BLINDEXVALUES d
                    INNER JOIN PARUS.BLSUBREPORTS s ON (d.PRN = s.RN)
                    INNER JOIN PARUS.BLREPORTS r ON (s.PRN = r.RN)
                    INNER JOIN PARUS.BLREPFORMED pf ON (r.BLREPFORMED = pf.RN)
                    INNER JOIN PARUS.BLREPFORM rf ON (pf.PRN = rf.RN)
                    WHERE rf.CODE = '40 COVID 19'
                      AND r.BDATE BETWEEN {START} AND {STOP}
                    ORDER BY r.BDATE DESC
                )
                WHERE ROWNUM <= 2
            )
		)
	pivot
		(
	max(value)
	FOR POKAZATEL IN (
		'tvsp_revac' tvsp,'vak_revac' revac, 'revac_02_01' pok_02,'revac_03_01' pok_03,'revac_04_01'pok_04,
		'revac_05_01' pok_05,'revac_06_01' pok_06,'revac_07_01' pok_07,'revac_08_01' pok_08,'revac_09_01' pok_09,
		'revac_10_01' pok_10,'revac_11_01' pok_11,'revac_12_01' pok_12,'revac_13_01' pok_13,'revac_14_01' pok_14,
		'revac_15_01' pok_15,'revac_16_01' pok_16,'revac_17_01' pok_17,'revac_18_01' pok_18,'revac_19_01' pok_19
		))
	WHERE tvsp IS NOT null"""
