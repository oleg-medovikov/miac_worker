from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

async def bez_izhoda():
    SQL = open('func/zam_mz/sql/bez_ishod.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = await put_excel_for_mo(DF,'Без исхода 30 дней', None)
    await put_svod_for_mo(DF, 'Без исхода 30 дней', None)

    return STAT_FILE
