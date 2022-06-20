from base import parus_sql, miac_ds_insert

def svod_27_covid_small():
    SQL = open('func/parus/sql/covid_36_svod.sql', 'r').read()

    DF = parus_sql(SQL)

    if len(df):
        miac_ds_insert(DF, 'covid_27', 'Pds', False, 'replace' )

    return 1


