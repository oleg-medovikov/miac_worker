from base import covid_sql
from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

async def zavishie_statusy():
    SQL_1 = open('func/zam_mz/sql/bez_ambulat_level_amb.sql','r').read()
    SQL_2 = open('func/zam_mz/sql/bez_ambulat_level_noMO.sql','r').read()

    DF_1 = covid_sql( SQL_1 )
    DF_2 = covid_sql( SQL_2 )

    STAT_1 = await put_excel_for_mo(
            DF_1,
            'зависшие статусы',
            None)
    await put_svod_for_mo(
            DF_1,
            'зависшие статусы',
            None)

    STAT_2 = await put_excel_for_mo(
            DF_2,
            'зависшие статусы без МО прикрепления',
            None)
    await put_svod_for_mo(
            DF_2,
            'зависшие статусы без МО прикрепления',
            None)

    return STAT_1 + ';' + STAT_2

