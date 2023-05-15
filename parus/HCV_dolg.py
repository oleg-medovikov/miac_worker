from base import parus_sql
from .HCV_MO_list import HCV_MO_list

from system import write_styling_excel_file


def HCV_dolg():
    SQL = open('parus/sql/HCV_dolg.sql', 'r').read()

    DF = parus_sql(SQL)

    DF = DF.pivot_table(
            index=['ORGANIZATION'],
            columns=['DAY'],
            values=['ERROR'],
            aggfunc='first'
        ).stack(0)
    DF.reset_index(inplace=True)
    del DF['level_1']

    # добавляем должников
    DELTA = set(HCV_MO_list) - set(DF['ORGANIZATION'])
    for ORG in DELTA:
        DF = DF.append({'ORGANIZATION': ORG}, ignore_index=True)

    DF = DF.fillna('Нет отчета!')
    # записываем файл
    NEW_NAME = 'temp/ХВГС_должники.xlsx'
    write_styling_excel_file(NEW_NAME, DF, 'ХГВС_долг')

    return NEW_NAME
