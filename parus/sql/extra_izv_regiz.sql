SELECT 
    [Подведомственность],
    [MO],
    SUM(CASE 
            WHEN status IN ('1 - ЭМД отправлен на регистрацию в федеральную подсистему', 'over') THEN Total
            ELSE 0
        END) AS 'Count_wait',
    SUM(CASE 
            WHEN status IN ('2 - ЭМД не прошел ФЛК на региональном уровне',
                            '3 - Ошибка при передаче ЭМД в федеральную подсистему',
                            '5 - Ошибка при прохождении ФЛК в федеральной подсистеме') THEN Total
            ELSE 0
        END) AS 'Count_good',
    SUM(CASE 
            WHEN status = '4 - ЭМД успешно зарегистрирован в федеральной подсистеме' THEN Total
            ELSE 0
        END) AS 'Count_bad'
FROM [MIAC_DS].[rmd].[v_eventlog_remd_all_2023_light]
WHERE ShortName = 'Экстренное извещение об инфекционном заболевании'
    AND [Year] = CASE WHEN MONTH(GETDATE()) = 1 THEN YEAR(GETDATE()) - 1 ELSE YEAR(GETDATE()) END
    AND [Month] = CASE WHEN MONTH(GETDATE()) = 1 THEN 12 ELSE MONTH(GETDATE()) - 1 END
GROUP BY [Подведомственность], [MO]
ORDER BY [Подведомственность], [MO];
