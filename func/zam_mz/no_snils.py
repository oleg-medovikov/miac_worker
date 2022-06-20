from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

async def no_snils():
    SQL = open('func/zam_mz/sql/no_snils.sql', 'r').read()

    DF = covid_sql( SQL )

    STAT_FILE = await put_excel_for_mo(DF,'Нет СНИЛСа', None)
    await put_svod_for_mo(DF, 'Нет СНИЛСа', None)

    return STAT_FILE

