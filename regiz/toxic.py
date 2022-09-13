import pandas as pd
import requests

from conf import REGIZ_AUTH

from .dict_toxic import Dict_Aim_Poison, Dict_Boolean_Alc, \
                        Dict_Place_Incident, Dict_Place_Poison, \
                        Dict_MKB, Dict_Type_Poison, Dict_Medical_Help, \
                        Dict_Set_Diagnosis


class my_except(Exception):
    pass

def get_cases(START,END):
    """Получаем начальную выборку"""

    URL = f" https://regiz.gorzdrav.spb.ru/N3.BI/getDData?id=1078&args={START},{END}&auth={REGIZ_AUTH}"

    df = pd.DataFrame( data = requests.get(URL).json() )

    if len(df) == 0:
        raise my_except('Нет случаев отравления за этот период')

    df['date_aff_first'] = pd.to_datetime(df['date_aff_first'], format='%Y-%m-%d')
    df.sort_values(by=['date_aff_first'], inplace=True )
    df.drop_duplicates(subset=df.columns.drop('date_aff_first'), keep='last', inplace=True )
    df.index = range(len(df))
    return df


def get_address_multi(DF):
    """Получение адреса в много потоков"""
    def func(x):
        URL = f"https://regiz.gorzdrav.spb.ru/N3.BI/getDData?id=1079&args={x}&auth={REGIZ_AUTH}"
        return requests.get(URL).json()[0]['address']
    
    import hashlib
    from multiprocesspandas import applyparallel
    return DF['luid'].apply_parallel(func, num_processes=10 )


