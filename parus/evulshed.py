import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

def evulshed():
    SQL = open('parus/sql/evulshed.sql', 'r').read()

    DF = parus_sql(SQL)

    DF = DF.pivot_table(
            index=['ORGANIZATION'],
            columns=['POKAZATEL', 'DAY'],
            values=['VALUE'],
            aggfunc='first').stack(0)

    DATE = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%d_%m_%Y')

    NEW_NAME = 'temp/' + DATE + '_Эвушелд.xlsx'

    shutil.copyfile('help/evulshed.xlsx', NEW_NAME)

    wb= openpyxl.load_workbook( NEW_NAME )
    ws = wb['Свод']
    rows = dataframe_to_rows(DF,index=True, header=True)
    for r_idx, row in enumerate(rows,2):  
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    wb.save( NEW_NAME )

    return  NEW_NAME

