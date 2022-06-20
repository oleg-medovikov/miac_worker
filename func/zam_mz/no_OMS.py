from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

async def no_OMS():
    SQL = open('func/zam_mz/sql/no_OMS.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = await put_excel_for_mo(DF,'Нет данных ОМС', None)
    await put_svod_for_mo(DF, 'Нет данных ОМС', None)

    return STAT_FILE
