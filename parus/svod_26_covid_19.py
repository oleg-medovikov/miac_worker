import time, datetime, shutil, openpyxl
import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql
from clas import Dir


def svod_26_covid_19():
    SQL = open('parus/sql/covid_26_svod.sql', 'r').read()

    DF = parus_sql(SQL)

    DF['type'] = 'parus'

    DATE = datetime.datetime.now().strftime('%d.%m.%Y')

    OLD_FILE = Dir.get('punct_zabor') + '/' + DATE + ' Пункты отбора.xlsx'

    values = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0}

    try:
        OLD = pd.read_excel(
                OLD_FILE,
                skiprows=3,
                header=None,
                sheet_name='Соединение'
                )
    except:
        OLD = pd.DataFrame()
    else:
        OLD = OLD.loc[~(OLD[2].isnull() & OLD[3].isnull() & OLD[5].isnull())]
        OLD = OLD.fillna(value=values)
        del OLD[0]
        del OLD[14]
        OLD['type'] = 'file'

    if len(OLD.columns) == len(DF.columns):
        OLD.columns = DF.columns

    NEW_DF = pd.concat([DF, OLD], ignore_index=True)
    NEW_DF = NEW_DF.drop_duplicates(subset=[
        'LAB_UTR_MO',
        'ADDR_PZ',
        'LAB_UTR_02'])

    DATE = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%d_%m_%Y')

    NEW_NAME = 'temp/' + DATE + '_26_COVID_19_cvod.xlsx'

    shutil.copyfile('help/26_COVID_19_svod.xlsx', NEW_NAME )

    wb= openpyxl.load_workbook( NEW_NAME )

    ws = wb['Из паруса']
    rows = dataframe_to_rows(DF,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    ws = wb['Из файла']
    rows = dataframe_to_rows(OLD,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    ws = wb['Соединение']
    rows = dataframe_to_rows(NEW_DF,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save( NEW_NAME )

    return NEW_NAME
