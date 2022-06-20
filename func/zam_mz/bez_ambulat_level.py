from base import covid_sql

from .put_svod_for_mo  import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo

async def bez_ambulat_level():
    ROOT = 'func/zam_mz/sql/'
    SQL_1 = open(ROOT + 'bez_ambulat_level.sql', 'r').read()
    SQL_2 = open(ROOT + 'bez_ambulat_level_death_covid.sql', 'r').read()
    SQL_3 = open(ROOT + 'bez_ambulat_level_death_nocovid.sql', 'r').read()

    DF_1 = covid_sql( SQL_1 )
    DF_2 = covid_sql( SQL_2 )
    DF_3 = covid_sql( SQL_3 )
    
    STAT_1 = await put_excel_for_mo(
            DF_1,
            'Нет амбулаторного этапа',
            None)
    STAT_2 = await put_excel_for_mo(
            DF_2,
            'Нет амбулаторного этапа, умер от COVID',
            None)
    STAT_3 = await put_excel_for_mo(
            DF_3,
            'Нет амбулаторного этапа, умер не от COVID',
            None)
    await put_svod_for_mo(
            DF_1,
            'Нет амбулаторного этапа',
            None)
    await put_svod_for_mo(
            DF_2,
            'Нет амбулаторного этапа, умер от COVID',
            None)
    await put_svod_for_mo(
            DF_3,
            'Нет амбулаторного этапа, умер не от COVID',
            None)

    return STAT_1 + ';' + STAT_2 + ';' + STAT_3
