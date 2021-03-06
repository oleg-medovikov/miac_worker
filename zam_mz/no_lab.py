from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

def no_lab():
    SQL = open('zam_mz/sql/no_lab.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = put_excel_for_mo(
            DF,
            'нет лабораторного подтверждения',
            None)
    put_svod_for_mo(
            DF,
            'нет лабораторного подтверждения',
            None)

    return STAT_FILE
