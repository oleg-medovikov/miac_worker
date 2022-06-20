import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

def svod_37_covid_19():
    SQL = open('func/parus/sql/covid_37_svod.sql', 'r').read()

    DF = parus_sql(SQL)

    DATE = DF.at[0,'DAY']
    del DF['DAY']

    NEW_NAME = 'temp/' + DATE + '_37_COVID_19_cvod.xlsx'

    shutil.copyfile('help/37_COVID_19_svod.xlsx', NEW_NAME)

    wb= openpyxl.load_workbook( NEW_NAME )
    ws = wb['Свод']
    rows = dataframe_to_rows(DF,index=False, header=False)
    for r_idx, row in enumerate(rows,6):  
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    wb.save( NEW_NAME )

    return  NEW_NAME

