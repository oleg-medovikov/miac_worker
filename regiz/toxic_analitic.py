import pandas as pd
import requests
from datetime import datetime

from conf import REGIZ_AUTH
from system import return_mounth, write_styling_excel_file


class my_except(Exception):
    pass


def get_cases(START: str, END: str) -> 'pd.DataFrame':
    """Получаем начальную выборку"""
    URL = " https://regiz.gorzdrav.spb.ru/N3.BI/getDData" \
        + f"?id=1127&args={START},{END}&auth={REGIZ_AUTH}"

    df = pd.DataFrame(data=requests.get(URL).json())

    if len(df) == 0:
        raise my_except('нет случаев!')

    df['date_aff_first'] = pd.to_datetime(
        df['date_aff_first'],
        format='%Y-%m-%d'
        )

    df.sort_values(by=['date_aff_first'], inplace=True)
    df.drop_duplicates(
        subset=df.columns.drop('date_aff_first'),
        keep='last',
        inplace=True
        )
    df.index = range(len(df))

    obs = df.pivot_table(
        index=['luid'],
        columns=['observation_code'],
        values=['observation_value'],
        aggfunc='first'
        ).stack(0)
    DF = df.copy()

    del DF['observation_code']
    del DF['observation_value']

    DF = DF.drop_duplicates()
    DF = DF.merge(obs, how='left', on=['luid'])
    DF.index = range(len(DF))

    return DF


def toxic_analitic(ARG):
    "сгенерировать за месяц"
    DATE = datetime.strptime(ARG.split(';')[0], '%d-%m-%Y')
    START, END = return_mounth(DATE)
    DF = get_cases(START, END)
    DF = DF.loc[DF['medical_help_name'] == ARG.split(';')[1]]

    FILENAME = f'temp/Аналитика по полноте регистра с {START} по {END}.xlsx'
    D = pd.DataFrame()

    DICT = {
        'history_number': 'Номер истории болезни',
        'date_aff_first': 'Дата открытия СМО',
        'age': 'Возраст',
        'gender': 'Пол',
        'diagnosis': 'Диагноз',
        'smo_fio': 'ФИО врача СМО',
        'meddoc_fio': 'ФИО врача МД',
        '303':  '303 - Дата установления диагноза',
        '1101': '1101 - Место происшествия',
        '1102': '1102 - Адрес места происшествия',
        '1103': '1103 - Наименование места происшествия',
        '1104': '1104 - Дата отравления',
        '1105': '1105 - Дата первичного обращения',
        '1106': '1106 - Токсичные вещества, часто встречающиеся',
        '1107': '1107 - Токсичные вещества',
        '1108': '1108 - Сочетание с алкоголем',
        '1109': '1109 - Лицо, установившее диагноз',
        '1110': '1110 - Оказана медицинская помощь',
        '1111': '1111 - Место наступления смерти',
        '1113': '1113 - Характер отравления',
        '1114': '1114 - Количество отравившихся',
        '1115': '1115 - Обстоятельства отравления',
        '1116': '1116 - Обстоятельства отравления текст',
        '1117': '1117 - Место приобретения яда',
        '1118': '1118 - Место приобретения яда текст',
        '1119': '1119 - Социальное положение',
    }

    for key, value in DICT.items():
        try:
            D[value] = DF[key]
        except KeyError:
            continue

    D = D.fillna('ПУСТО!!!')
    write_styling_excel_file(FILENAME, D, ARG.split(';')[1])

    return FILENAME
