from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

def net_diagnoz_covid():
    SQL = open('func/zam_mz/sql/net_diagnoz_covid.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = put_excel_for_mo(DF,'нет диагноза COVID', None)
    put_svod_for_mo(DF,'нет диагноза COVID' , None)

    return STAT_FILE

