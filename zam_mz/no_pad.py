from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

def no_pad():
    SQL = open('zam_mz/sql/net_pad.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = put_excel_for_mo(DF,'нет ПАЗ', None)
    put_svod_for_mo(DF, 'нет ПАЗ', None)

    return STAT_FILE

