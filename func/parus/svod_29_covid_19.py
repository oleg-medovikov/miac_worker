import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

def svod_29_covid_19():
    if int(time.strftime("%H")) < 16:
        SQL = open('func/parus/sql/covid_29_svod1.sql','r').read()
        DATE = datetime.datetime.now() - datetime.timedelta(days=1)
    else:
        SQL = open('func/parus/sql/covid_29_svod0.sql','r').read()
        DATE = datetime.datetime.now()
    
    df = parus_sql(SQL)


    NEW_NAME = 'temp/' + DATE.strftime('%d_%m_%Y') + '_29_COVID_19_cvod.xlsx'

    shutil.copyfile('help/29_COVID_19_svod.xlsx', NEW_NAME)
    
    wb= openpyxl.load_workbook(NEW_NAME)
    ws = wb['Для заполнения']

    rows = dataframe_to_rows(df,index=False, header=False)

    for r_idx, row in enumerate(rows,3):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    wb.save(NEW_NAME)

    return NEW_NAME

