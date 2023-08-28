import shutil
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql


def mp_veteran_cvo():
    SQL = open('parus/sql/mp_veteran_cvo.sql', 'r').read()

    DF = parus_sql(SQL)

    DATE = DF.at[0, 'DAY']

    del DF['DAY']

    DF.loc['Итого по городу'] = DF.loc[
            DF['POK01'] != 'Итого по организации'
            ].sum(numeric_only=True, axis=0)
    DF.loc['Итого по городу', 'ORGANIZATION'] = 'Итого:'

    NEW_NAME = 'temp/МП_ветеранам_СВО_' + DATE + '.xlsx'

    shutil.copyfile('help/mp_veteran_cvo.xlsx', NEW_NAME)

    wb = openpyxl.load_workbook(NEW_NAME)
    ws = wb['Свод']
    rows = dataframe_to_rows(DF, index=False, header=False)
    for r_idx, row in enumerate(rows, 5):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save(NEW_NAME)

    return NEW_NAME
