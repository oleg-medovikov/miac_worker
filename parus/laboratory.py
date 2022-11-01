import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
import pandas as pd
from base import parus_sql

def laboratory():
    SQL = open('parus/sql/laboratory.sql', 'r').read()

    DF   = parus_sql( SQL )

    DATE = DF.at[ 0, 'DAY' ]

    del DF ['DAY']

    DF = DF.pivot_table(index=['ORGANIZATION'], columns=['POKAZATEL'],values=['VALUE'], aggfunc='first').stack(0)
    
    DF.index = range(len(DF))

    for col in DF.columns:
        try:
            DF[col] = pd.to_numeric(DF[col])
        except:
            pass
    

    NEW_NAME = 'Мониторинг_деятельности_лабораторий_' + DATE + '.xlsx'

    shutil.copyfile( 'help/laboratory.xlsx', NEW_NAME )

    wb = openpyxl.load_workbook ( NEW_NAME )
    
    ws = wb['svod']
    rows = dataframe_to_rows(DF,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save( NEW_NAME )

    return NEW_NAME


