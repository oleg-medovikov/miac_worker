import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

def svod_40_covid_19_dates():
    SQL = open('func/parus/sql/covid_40_by_date.sql', 'r').read()

    df = parus_sql(SQL)

    df = df.loc[df.TVSP.notnull()]
    df = df.loc[~df.TVSP.isin(['Пункт вакцинации'])]
    df.V_1 = pd.to_numeric(df.V_1)
    df.V_2 = pd.to_numeric(df.V_2)
    df.DAY = df.DAY.dt.date
    
    res = df.pivot_table(
            index=['DIST','TVSP'],
            columns=['DAY'],
            values=['V_1','V_2'],
            fill_value=0,
            aggfunc=np.sum )

    summ = df.pivot_table(
            index=['DIST'],
            columns=['DAY'],
            values=['V_1','V_2'],
            fill_value=0,
            aggfunc=np.sum )

    total = pd.DataFrame(summ.sum()).T

    res['Район'] = res.index.get_level_values(0)
    res['Пункт вакцинации'] = res.index.get_level_values(1)

    summ['Район'] = summ.index.get_level_values(0)
    summ['Пункт вакцинации'] = 'Всего'
    total['Район'] = 'Весь город'
    total['Пункт вакцинации'] = 'Все'

    itog = pd.concat([total,summ,res], ignore_index=True)
    itog = itog.set_index(['Район','Пункт вакцинации'])
    
    FILE = 'temp/Вакцинация по датам.xlsx'
    with pd.ExcelWriter(file) as writer:
        itog.V_1.to_excel(writer,sheet_name='Первый компонент вакцины')
        itog.V_2.to_excel(writer,sheet_name='Второй компонент вакцины')
    
    return FILE


 
