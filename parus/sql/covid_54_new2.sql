SELECT itog.day,
itog.organization, itog.ogrn, itog.pok_3, itog.pok_4,
itog.pok_5_itog,
otchet.pok_5,
itog.pok_6_itog,
otchet.pok_6,
otchet.pok_7
from
(SELECT  ORGANIZATION, pok_3,pok_4, ogrn,
	to_char(max(day), 'DD.MM.YYYY') day,
	sum(CAST(pok_5 AS int) )  pok_5_itog,
	sum(CAST(pok_6 AS int) )  pok_6_itog
        FROM (
                SELECT
                	r.BDATE day,
                    --to_char(r.BDATE, 'DD.MM.YYYY') day,
                    a.AGNNAME organization,
                    a.OGRN ogrn,
                    i.CODE pokazatel,
                    ro.RN TABLICHA,
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
                WHERE rf.code = '54 COVID 19 NEW2'
                and a.AGNNAME <> 'Наименование Контаргент используется для сводных отчетов'
                --and r.BDATE =  trunc(SYSDATE) 
                and i.CODE in ('etest_03', 'etest_04', 'etest_05', 'etest_06', 'etest_07')
                )
                pivot
                (
                max(value)
                FOR POKAZATEL IN (
                'etest_03' pok_3, 'etest_04' pok_4,
                'etest_05' pok_5, 'etest_06' pok_6, 'etest_07' pok_7 
                )
                )
    where pok_3 is not null
    group by ORGANIZATION, pok_3, pok_4, ogrn ) itog
    left join (
    SELECT  ORGANIZATION, pok_3,pok_4,date_otch,
	CAST(pok_5 AS int)   pok_5,
	CAST(pok_6 AS int)  pok_6,
	CAST(pok_7 AS int)  pok_7
        FROM (
                SELECT
                    to_char(r.BDATE, 'DD.MM.YYYY') date_otch,
                    a.AGNNAME organization,
                    i.CODE pokazatel,
                    ro.RN TABLICHA,
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
                WHERE rf.code = '54 COVID 19 NEW2'
                and r.BDATE = trunc(SYSDATE)
                and i.CODE in ('etest_03', 'etest_04', 'etest_05', 'etest_06', 'etest_07')
                )
                pivot
                (
                max(value)
                FOR POKAZATEL IN (
                'etest_03' pok_3, 'etest_04' pok_4,
                'etest_05' pok_5, 'etest_06' pok_6, 'etest_07' pok_7 
                )
                )
    where pok_3 is not null
    )  otchet
    on( itog.organization = otchet.organization and itog.pok_3 = otchet.pok_3 and itog.pok_4 = otchet.pok_4 )
    order by ORGANIZATION, pok_3,pok_4
