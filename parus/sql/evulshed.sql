SELECT
	 to_char(r.BDATE, 'DD.MM.YYYY') day,
     a.AGNNAME organization,
     i.CODE pokazatel,
	 NUMVAL AS value
     FROM PARUS.BLTBLVALUES v
          INNER JOIN PARUS.BLTABLESIND si
                on(v.BLTABLESIND = si.RN)
          INNER JOIN (SELECT * FROM PARUS.BALANCEINDEXES
                				WHERE CODE IN ('mol_04_e', 'mol_06') 
                			) i
                on(si.BALANCEINDEXES = i.RN)
          INNER JOIN (SELECT PRN, RN, NUMB  FROM  PARUS.BLTBLROWS  ) ro
                on(v.PRN = ro.RN)
          INNER JOIN PARUS.BLSUBREPORTS s
                on(ro.PRN = s.RN)
          INNER JOIN (SELECT * FROM PARUS.BLREPORTS 
          				WHERE BDATE <= trunc(SYSDATE) AND BDATE > trunc(SYSDATE) - 14 
                )  r
                on(s.PRN = r.RN)
          INNER JOIN (SELECT * FROM PARUS.AGNLIST
          				WHERE AGNNAME != 'Наименование Контаргент используется для сводных отчетов'
          			) a
                on(r.AGENT = a.RN)
          INNER JOIN PARUS.BLREPFORMED rd
                on(r.BLREPFORMED = rd.RN)
          INNER JOIN (SELECT * FROM PARUS.BLREPFORM WHERE CODE = 'Эвушелд' ) rf
                on(rd.PRN = rf.RN)
