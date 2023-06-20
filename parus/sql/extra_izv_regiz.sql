SELECT 
     [Подведомственность]
    ,[MO]
    , ISNULL((SELECT SUM(Total)
          FROM [MIAC_DS].[rmd].[v_eventlog_remd_all_2023_light] 
          WHERE ShortName = m.ShortName
              AND [Year] = m.[Year]
              AND [Month] = m.[Month]
              AND [Подведомственность] = m.[Подведомственность] 
              AND [MO] = m.[MO]
              AND status IN ('2 - ЭМД не прошел ФЛК на региональном уровне'
                    ,'3 - Ошибка при передаче ЭМД в федеральную подсистему'
                    ,'5 - Ошибка при прохождении ФЛК в федеральной подсистеме')), 0)
      AS 'Count_good'
    ,ISNULL((SELECT Total
          FROM [MIAC_DS].[rmd].[v_eventlog_remd_all_2023_light] 
          WHERE ShortName = m.ShortName
              AND [Year] = m.[Year]
              AND [Month] = m.[Month]
              AND [Подведомственность] = m.[Подведомственность] 
              AND [MO] = m.[MO]
              AND status = '4 - ЭМД успешно зарегистрирован в федеральной подсистеме'), 0)
      AS 'Count_bad'
  FROM (SELECT DISTINCT [Подведомственность], [MO], ShortName, [Year], [Month]  
      FROM [MIAC_DS].[rmd].[v_eventlog_remd_all_2023_light]) AS m
  WHERE m.ShortName = 'Экстренное извещение об инфекционном заболевании'
      AND m.[Year] = CASE WHEN MONTH(GETDATE()) = 1 THEN YEAR(GETDATE())-1 ELSE YEAR(GETDATE()) END
      AND m.[Month] = CASE WHEN MONTH(GETDATE()) = 1 THEN 12 ELSE MONTH(GETDATE())-1 END
  ORDER BY m.[Подведомственность], m.[MO]
