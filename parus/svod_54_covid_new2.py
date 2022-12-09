import shutil
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

from base import parus_sql


def svod_54_covid_new2():
    SQL = open('parus/sql/covid_54_new2.sql', 'r').read()

    DF = parus_sql(SQL)

    DATE = DF.at[0, 'DAY']

    del DF['DAY']

    NEW_NAME = f'temp/{DATE}_54_COVID_19_new2.xlsx'

    shutil.copyfile('help/54_COVID_19_new2.xlsx', NEW_NAME)

    wb = load_workbook(NEW_NAME)

    ws = wb['свод']
    rows = dataframe_to_rows(DF, index=False, header=False)
    for r_idx, row in enumerate(rows, 5):
        for c_idx, value in enumerate(row, 2):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save(NEW_NAME)

    return NEW_NAME
