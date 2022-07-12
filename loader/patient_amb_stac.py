from datetime import datetime
import openpyxl, shutil
from openpyxl.utils.dataframe import dataframe_to_rows

from base import covid_sql

SQL = """
SELECT
         [Вид лечения]
         ,count(distinct [УНРЗ]) As 'Всего'
         ,count(distinct case when  (age >=60 ) then [УНРЗ] end) As 'Заболевшие в возрасте 60+'
         ,count(distinct case when  (age >=70 ) then [УНРЗ] end) As 'Заболевшие в возрасте 70+'
  FROM (SELECT [Диагноз]
                           ,[Вид лечения]
                           ,[УНРЗ]
                           , CASE 
                                        when [Диагноз] = 'U07.1'
                                               then 'U1'
                                        when [Диагноз] = 'U07.2'
                                               then 'U2'
                                        when [Диагноз] like '%J1[2-8]%'
                                               then 'J'
                             end 'Diagn'
                           ,dbo.f_calculation_age([Дата рождения],[Диагноз установлен]) As 'age'
                    FROM [COVID].[dbo].[cv_fedreg]
                    where ([Диагноз] like '%U07%'
                                  OR [Диагноз] like '%J1[2-8]%')
                                  and Isnull([Дата исхода заболевания],'') ='') As dan
             GROUP BY [Вид лечения]
"""

def patient_amb_stac():
    
    df = covid_sql(SQL)

    date_otch = datetime.now().strftime('%d_%m_%Y')
    
    new_name  = 'temp/' + date_otch + '_Пациенты на амб и стац лечении.xlsx'

    shutil.copyfile('help/patient_amb_stac.xlsx' , new_name)
    
    wb= openpyxl.load_workbook( new_name)
    ws = wb['Лист1']
    rows = dataframe_to_rows(df,index=False, header=False)
    for r_idx, row in enumerate(rows,2):  
        for c_idx, value in enumerate(row,1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    wb.save( new_name )
    
    return new_name
