from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

def no_snils():
    SQL = open('func/zam_mz/sql/no_snils.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = put_excel_for_mo(DF,'Нет СНИЛСа', None)
    put_svod_for_mo(DF, 'Нет СНИЛСа', None)

    return STAT_FILE

