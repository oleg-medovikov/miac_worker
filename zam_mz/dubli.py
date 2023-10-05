from system import write_styling_excel_file
from base import covid_sql


def dubli():
    SQL = open('zam_mz/sql/dubli.sql', 'r').read()
    DF = covid_sql(SQL)
    NEW_NAME = 'temp/Замечания Дубли.xlsx'
    write_styling_excel_file(NEW_NAME, DF, 'dubli')
    return NEW_NAME
