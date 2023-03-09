from pandas import DataFrame, to_datetime
import requests

from conf import REGIZ_AUTH


class my_except(Exception):
    pass


def toxic_get_cases(START: str, END: str) -> 'DataFrame':
    """чаем начальную выборку"""
    URL = " https://regiz.gorzdrav.spb.ru/N3.BI/getDData" \
        + f"?id=1127&args={START},{END}&auth={REGIZ_AUTH}"

    try:
        df = DataFrame(data=requests.get(URL).json())
    except requests.Timeout:
        raise my_except('Недоступен сервер нетрики, попробуйте позже')
    except requests.ConnectionError:
        raise my_except('Недоступен сервер нетрики, попробуйте позже')

    if len(df) == 0:
        raise my_except('нет случаев!')

    # Распознаем автоматические даты создания МК и показателей
    df['date_aff_first'] = to_datetime(
        df['date_aff_first'],
        format='%Y-%m-%d %H:%M:%S'
        )
    df['meddoc_creation_date'] = to_datetime(
        df['meddoc_creation_date'],
        format='%Y-%m-%d %H:%M:%S'
        )

    # Сортируем по датам и удаляем дублирующиеся строки,
    # оставляя последнее изменение
    df.sort_values(by=['date_aff_first', 'meddoc_creation_date'], inplace=True)
    df.drop_duplicates(
        subset=df.columns.drop('date_aff_first', 'meddoc_creation_date'),
        keep='last',
        inplace=True
        )
    # исправляем индексы
    df.index = range(len(df))

    # делаем разворот таблицы для показателей
    obs = df.pivot_table(
        index=['history_number'],
        columns=['observation_code'],
        values=['observation_value'],
        aggfunc='first'
        ).stack(0)

    # уникальные строки по номеру истории болезни
    DF = df.copy()

    del DF['observation_code']
    del DF['observation_value']

    DF.drop_duplicates(
        subset='history_number',
        keep='last',
        inplace=True
    )

    # соединяем уникальные истории с показателями
    DF = DF.merge(obs, how='left', on=['history_number'])
    # обновляем индексы
    DF.index = range(len(DF))

    # добавляем поля, если каких-то обсервов не хватает
    CASE_CODES = [
        '303', '1101', '1102', '1103',
        '1104', '1105', '1108', '1109',
        '1110', '1113', '1115', '1117',
        '1119', '1123'
        ]

    for CASE in CASE_CODES:
        if CASE not in DF.columns:
            DF[CASE] = ''

    return DF
