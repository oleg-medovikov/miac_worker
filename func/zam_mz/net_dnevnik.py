from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

async def net_dnevnik():
    SQL = open('func/zam_mz/sql/net_dnevnik.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = await put_excel_for_mo(DF,'нет дневниковых записей', None)
    await put_svod_for_mo(DF, 'нет дневниковых записей', None)

    return STAT_FILE

