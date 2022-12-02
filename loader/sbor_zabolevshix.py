import glob
import pandas as pd
import os
from datetime import datetime, timedelta

from base import covid_insert
from clas import Dir

columnsTitles = [
    'Медицинская организация', 'использованный файл',
    'Фамилия, имя, отчество', 'Дата рождения', 'СНИЛС', 'Должность',
    'Дата постановки диагноза (COVID-19)',
    'место нахождения в настоящее время',
    'Домашний адрес, телефон',
    'Связь заболевания с выполнением обязанностей в медицинской организации (да / нет)',
    'Признан комиссией учреждения, что мед.работник пострадавший (да / нет)'
    ]
new_name = [
    'mo', 'file', 'fio', 'birthday', 'snils', 'doljnost',
    'date_diagnoz', 'place', 'adress', 'connection', 'commission'
    ]

MASK = '/mnt/FTP/EPID/COVID/EPID*/EPID*/Медработники_заболевшие/*.xlsx'


def sbor_zabolevshix():
    "заболевшие медицинские работники"
    list_ = []
    delta = datetime.now() - timedelta(days=1)

    for file in glob.glob(MASK):
        time = datetime.utcfromtimestamp(os.stat(file).st_ctime)
        if time > delta:
            df = pd.read_excel(file).dropna(how='all')
            df['Медицинская организация'] = file.rsplit('/', 1)[-1]\
                .replace('готово.xlsx', '')\
                .replace('новый_шаблон', '')\
                .replace('_', ' ')
            df['использованный файл'] = file
            list_.append(df)

    df = pd.concat(list_)
    df = df[columnsTitles]
    df.columns = new_name
    covid_insert(df, 'svod_sotrudniki', 'robo', False, 'append')
    date = str(datetime.now().date())
    name_file = Dir.get('med_sin') + date + ' сводный файл.xlsx'
    df.to_excel(name_file, index=False)

    return "Собраны заболевшие медработники"
