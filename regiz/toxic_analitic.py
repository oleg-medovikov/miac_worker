import pandas as pd
from datetime import datetime

from system import return_mounth, write_styling_excel_file
from .toxic_get_cases import toxic_get_cases
from .toxic_checker import toxic_checker


class my_except(Exception):
    pass


def toxic_analitic(ARG):
    "сгенерировать за месяц"
    DATE = datetime.strptime(ARG.split(';')[0], '%d-%m-%Y')
    START, END = return_mounth(DATE)
    DF = toxic_get_cases(START, END)
    DF = DF.loc[DF['medical_help_name'] == ARG.split(';')[1]]

    FILENAME = f'temp/Аналитика по полноте регистра с {START} по {END}.xlsx'
    FILERROR = f'temp/Ошибки заполнения {START} по {END}.xlsx'

    # делаем проверку на ошибки
    error = toxic_checker(DF)
    if len(error):
        DF = DF.loc[~DF['history_number'].isin(error['history_number'])]

    D = pd.DataFrame()
    E = pd.DataFrame()

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
        '1123': '1123 - Район',
        'Ошибка': 'Ошибка',
    }

    for key, value in DICT.items():
        try:
            E[value] = error[key]
            D[value] = DF[key]
        except KeyError:
            continue

    D = D.fillna('ПУСТО!!!')
    write_styling_excel_file(FILENAME, D, ARG.split(';')[1])
    if len(error):
        write_styling_excel_file(FILERROR, E, 'errors')
        return FILENAME + ';' + FILERROR

    return FILENAME
