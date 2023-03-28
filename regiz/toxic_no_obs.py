from pandas import DataFrame
import requests

from conf import REGIZ_AUTH

DICT = {
    'case_open_date': 'Дата заведения',
    'history_number': 'Номер истории болезни',
    'diagnosis': 'Диагноз',
    'medical_help_name': 'Организация',
    'cancelled_obs': 'Есть ли отменённые показатели',
    }


class my_except(Exception):
    pass


def toxic_no_obs(START: str, END: str, ORG=None) -> 'DataFrame':
    """токсикологические пациенты без показателей"""
    URL = " https://regiz.gorzdrav.spb.ru/N3.BI/getDData" \
        + f"?id=1177&args={START},{END}&auth={REGIZ_AUTH}"

    try:
        df = DataFrame(data=requests.get(URL).json())
    except requests.Timeout:
        return DataFrame()
    except requests.ConnectionError:
        return DataFrame()
    else:
        if not len(df):
            return DataFrame()

    if ORG is not None:
        df = df.loc[df['medical_help_name'].isin([ORG])]

    DF = DataFrame()
    for key, value in DICT.items():
        try:
            DF[value] = df[key]
        except KeyError:
            continue

    return DF
