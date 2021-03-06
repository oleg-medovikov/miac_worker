from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

def neveren_vid_lechenia():
    SQL = open('zam_mz/sql/neverni_vid_lecenia.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = put_excel_for_mo(DF,'неверный вид лечения', None)
    put_svod_for_mo(DF, 'неверный вид лечения', None)

    return STAT_FILE 
