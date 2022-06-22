import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

def svod_28_covid_19():
    SQL = open('parus/sql/covid_28_svod.sql', 'r').read()

    DF = parus_sql(SQL)

    DATE = DF.at[0,'DAY']
    del DF['DAY']

    NEW_NAME = 'temp/' + DATE + '_28_COVID_19.xlsx'

    shutil.copyfile('help/28_COVID_19_svod.xlsx', NEW_NAME)

    wb= openpyxl.load_workbook( NEW_NAME )
    ws = wb['Свод']
    rows = dataframe_to_rows(DF,index=False, header=False)
    for r_idx, row in enumerate(rows,4):  
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    wb.save( NEW_NAME )

    return  NEW_NAME

