import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

import pandas as pd 


PART_NOMER = ['01','02','03','04','05','06','07','08','09','10']

COLUMNS = ['exp_test_01_01', 'exp_test_02_01', 'exp_test_03_01', 'exp_test_04_01',
           'exp_test_05_01','exp_test_06_01', 'exp_test_07_01', 'exp_test_08_01',
           'exp_test_09_01']


def svod_54_covid_19():
    SQL = open('parus/sql/covid_54_svod.sql', 'r').read()

    DF = parus_sql(SQL) 


    DATE = datetime.datetime.now().strftime('%d_%m_%Y')


    NEW_NAME = 'temp/54_COVID_19_'   + DATE + '.xlsx'

    shutil.copyfile('help/54_COVID_19_new.xlsx', NEW_NAME)

    wb = openpyxl.load_workbook(NEW_NAME)
    
    for NOMER in PART_NOMER:
        # Вытаскиваем кусок данных про конкретную партию
        PART = DF.loc[DF['POKAZATEL'].str.endswith( NOMER )]

        PART = PART.pivot_table(index = ['ORGANIZATION', 'DAY'], columns = ['POKAZATEL'],aggfunc='first').stack(0)

        PART.fillna(0,inplace=True)

        for COL in COLUMNS:
            COL = COL[:-2] + NOMER
            if COL not in PART.columns:
                 PART[COL] = 0
            else:
                PART[COL] = pd.to_numeric(PART[COL], errors='ignore')
        
        PART.reset_index(inplace=True)

        list_ = list(PART.columns[ 3:12 ])
        list_.append('DAY')
        PART = PART[list_]

        ws = wb['part ' + NOMER ]
        
        rows = dataframe_to_rows(PART,index=False, header=True)
        for r_idx, row in enumerate(rows,2):
            for c_idx, value in enumerate(row, 2):
                ws.cell(row=r_idx, column=c_idx, value=value)

    
    wb.save( NEW_NAME )

    return NEW_NAME


