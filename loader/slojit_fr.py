import xlrd
from glob import glob
import shutil
import numpy
import os
from multiprocessing import Pool
import pandas as pd
from datetime import datetime, timedelta

from clas import Dir
from base import covid_sql

NAMES = [
    'п/н', 'Дата создания РЗ', 'УНРЗ', 'Дата изменения РЗ',
    'СНИЛС', 'ФИО', 'Пол', 'Дата рождения',
    'Диагноз', 'Диагноз установлен',
    'Осложнение основного диагноза', 'Субъект РФ',
    'Медицинская организация', 'Ведомственная принадлежность',
    'Вид лечения', 'Дата госпитализации',
    'Дата исхода заболевания', 'Исход заболевания',
    'Степень тяжести', 'Посмертный диагноз', 'ИВЛ', 'ОРИТ',
    'МО прикрепления', 'Медицинский работник'
    ]


class my_except(Exception):
    pass


def read_file(FILE):
    df = pd.read_excel(
                FILE,
                header=1,
                usecols=NAMES,
                engine='xlrd',
                skipfooter=1)
    return df


def slojit_fr():
    "это функция складывает выгрузки ФР в 1 файл"

    xlrd.xlsx.ensure_elementtree_imported(False, None)
    xlrd.xlsx.Element_has_iter = True

    PATH = Dir.get('path_robot') + '/_ФР_по_частям'
    DATE = datetime.now().strftime("%Y_%m_%d")
    # nameSheetShablon = "Sheet1"

    FILES = glob(PATH + '/Федеральный регистр лиц*.xlsx')
    FILES += glob(PATH + '/Static/Федеральный регистр лиц*.xlsx')

    if not len(FILES):
        raise my_except('В папке нет файлов!')

    pool = Pool()
    df_list = pool.map(read_file, FILES)
    df = pd.concat(df_list, ignore_index=True)

    df["п/н"] = range(1, len(df)+1)

    TOMORROW = (datetime.today() + timedelta(days=1)).strftime("%Y_%m_%d")

    ROOT = Dir.get('path_robot') + '/' + TOMORROW

    FEDREG_FILE = ROOT + '/Федеральный регистр лиц, больных - ' + DATE + '.csv'

    # IACH_FILE = Dir.get('covid_iac2') \
    # + '/Федеральный регистр лиц, больных - '\
    #    + DATE + '_ИАЦ.csv'

    OTCHET_9 = glob(ROOT + '/9. Отчет по пациентам COVID-центр*.xlsx')

    MESS = '``` \n'
    MESS += f'Успешно сложены {len(FILES)} файлов выгрузки ФР, \
        всего строк: {df.shape[0]}'

    if len(OTCHET_9):
        OTCHET_9_NEW = Dir.get('covid_iac2') \
            + '/' + OTCHET_9[0].rsplit('/', 1)[1]
        shutil.copyfile(OTCHET_9[0], OTCHET_9_NEW)
        MESS += '\nОтчет №9 скопирован в папку иац'
    else:
        MESS += '\nНе удалось найти отчет №9'

    # Числа для Марии Геннадьевны
    NumberForMG = df[
                    df['Диагноз'].isin(['U07.1'])
                    & df['Исход заболевания'].isnull()
                    & df['Вид лечения'].isin(['Стационарное лечение'])
                ].shape[0]

    NumberFor1 = df[df['Диагноз'].isin(['U07.1'])].shape[0]

    NumberFor2 = df[df[
            'Посмертный диагноз'].isin(['U07.1'])
            & df['Исход заболевания'].isin(['Смерть'])
            ].shape[0]

    # Дата выгрузки
    DAY = pd.to_datetime(
        df['Дата изменения РЗ'],
        format='%d.%m.%Y'
        ).max().date()
    YESTERDAY = (DAY - timedelta(days=1)).strftime('%Y-%m-%d')

    # Какое-то sql колдунство
    # берем нужное число выздоровевших с мах номером и вчерашней датой
    SQL = f"""SELECT [value_count] FROM [robo].[values]
                where id = (
                    select max(id)
                        from [robo].[values]
                            where [value_name] = 'Всего выздоровело от COVID'
                                and date_rows = '{YESTERDAY}'
                        )"""

    count_vizd_old = covid_sql(SQL).iat[0, 0]
    count_vizd_new = df[
            df['Исход заболевания'].isin(['Выздоровление'])
            & df['Диагноз'].isin(['U07.1'])
            ].shape[0]

    NumberFor3 = count_vizd_new - count_vizd_old

    # Расчитываем возраст
    df['Возраст'] = (
        pd.to_datetime(df['Диагноз установлен'], format="%d.%m.%Y")
        - pd.to_datetime(df['Дата рождения'], format="%d.%m.%Y")) \
        / numpy.timedelta64(1, 'Y')

    # расчёт людей на стационарном лечении
    ILL = df['Исход заболевания'].isnull()
    STAC = df['Вид лечения'].isin(['Стационарное лечение'])
    AMB = df['Вид лечения'].isin(['Амбулаторное лечение'])
    COVID = df['Диагноз'].isin(['U07.1', 'U07.2'])
    J1 = df['Диагноз'].str.contains('J1[2-8]')
    AGE_18 = df['Возраст'] < 18
    AGE_60 = df['Возраст'] >= 60
    AGE_70 = df['Возраст'] >= 70

    NumberFor4_1 = df.loc[ILL & STAC & (COVID | J1)].shape[0]
    NumberFor4_2 = df.loc[ILL & STAC & (COVID | J1) & AGE_18].shape[0]
    NumberFor4_3 = df.loc[ILL & STAC & (COVID | J1) & AGE_60].shape[0]
    NumberFor4_4 = df.loc[ILL & STAC & (COVID | J1) & AGE_70].shape[0]

    # расчёт людей на амбулаторном лечении
    NumberFor5_1 = df.loc[ILL & AMB & (COVID | J1)].shape[0]
    NumberFor5_2 = df.loc[ILL & AMB & (COVID | J1) & AGE_18].shape[0]
    NumberFor5_3 = df.loc[ILL & AMB & (COVID | J1) & AGE_60].shape[0]
    NumberFor5_4 = df.loc[ILL & AMB & (COVID | J1) & AGE_70].shape[0]

    # Считаем выздоровевших за последние полгода
    REC = df['Исход заболевания'].str.contains('Выздоровление')
    DATE_HALF = datetime.now() - timedelta(days=181)
    df['Дата исхода заболевания'] = pd.to_datetime(
        df['Дата исхода заболевания'],
        format='%d.%m.%Y',
        errors='ignore'
        )
    HALF = df['Дата исхода заболевания'] > DATE_HALF

    NumberFor7 = df.loc[REC & COVID & HALF].shape[0]

    MESS += f"""
Цифры для Марии Геннадьевны:
===============================
На стационарном лечении (U07.1): {format(NumberForMG,'n')}
Всего заболело: {format(NumberFor1,'n')}
Всего умерло:   {format(NumberFor2,'n')}
Всего выздоровело за {str(DAY)}: {format(NumberFor3, 'n')}
Сейчас на стационаром лечении:
    Всего:     {format(NumberFor4_1, 'n')}
    Младше 18: {format(NumberFor4_2, 'n')}
    Старше 60: {format(NumberFor4_3, 'n')}
    Старше 70: {format(NumberFor4_4, 'n')}
Сейчас на амбулаторном лечении:
    Всего:     {format(NumberFor5_1, 'n')}
    Младше 18: {format(NumberFor5_2, 'n')}
    Старше 60: {format(NumberFor5_3, 'n')}
    Старше 70: {format(NumberFor5_4, 'n')}
================================
```
"""

    # Считаем детей
    count_deti_ill = df.loc[COVID & AGE_18].shape[0]
    count_deti_rec = df.loc[COVID & AGE_18 & REC].shape[0]

    DEATH = df['Исход заболевания'].isin(['Смерть'])
    COVID_D = df['Посмертный диагноз'].isin(['U07.1', 'U07.2'])
    # тут нужно посчитать обратные значения
    DICT_REPLACE = {
        False: True,
        True: False
        }
    COVID_D_E = COVID_D.replace(DICT_REPLACE)
    LIST_ISHOD_NO = [
        'Диагноз не подтвержден',
        'Отказ пациента от лечения',
        'Перевод пациента в другую МО',
        'Перевод пациента на амбулаторное лечение',
        'Перевод пациента на стационарное лечение'
        ]
    ISHOD_NO = df['Исход заболевания'].isin(LIST_ISHOD_NO)

    count_deti_death = df.loc[COVID_D & AGE_18 & DEATH].shape[0]
    count_deti_death_else = df.loc[COVID_D_E & AGE_18 & COVID & DEATH].shape[0]
    count_deti_else = df.loc[COVID & AGE_18 & ISHOD_NO].shape[0]
    count_deti_amb = df.loc[COVID & AGE_18 & AMB & ILL].shape[0]
    count_deti_stach = df.loc[COVID & AGE_18 & STAC & ILL].shape[0]

    count_deti_ill_old = covid_sql(f"""
        SELECT [value_count] FROM [robo].[values]
            where id = (select max(id)
                from [robo].[values]
                    where [value_name] = 'Всего детей заболело от COVID'
                and date_rows = '{YESTERDAY}' )"""
                                   ).iat[0, 0]

    count_deti_rec_old = covid_sql(f"""
        SELECT [value_count] FROM [robo].[values]
            where id = (select max(id)
                from [robo].[values]
                where [value_name] = 'Всего детей выздоровело от COVID'
                and date_rows = '{YESTERDAY}' )"""
                                   ).iat[0, 0]

    count_deti_death_old = covid_sql(f"""
        SELECT [value_count] FROM [robo].[values]
            where id = (select max(id)
                from [robo].[values]
                where [value_name] = 'Всего детей умерло от COVID'
                and date_rows = '{YESTERDAY}')"""
                                     ).iat[0, 0]

    MESS += f""";mess; ```
Отдельно по детям, больным COVID-19:
   Заболело:              {format(count_deti_ill,'n')}
   Заболело за день:      {format(count_deti_ill - count_deti_ill_old,'n')}
   Выздоровело:           {format(count_deti_rec,'n')}
   Выздоровело за день:   {format(count_deti_rec - count_deti_rec_old,'n')}
   Умерло:                {format(count_deti_death,'n')}
   Умерло за день:        {format(count_deti_death - count_deti_death_old,'n')}
   Умерло не от COVID-19: {format(count_deti_death_else,'n')}
   Другой исход:          {format(count_deti_else,'n')}
   Всего на амбулаторном: {format(count_deti_amb,'n')}
   Всего на стационарном: {format(count_deti_stach,'n')}
```
"""

    # Считаем школьников
    SCHOOL = df['Возраст'] > 6

    count_deti_ill = df.loc[COVID & AGE_18 & SCHOOL].shape[0]
    count_deti_rec = df.loc[COVID & AGE_18 & SCHOOL & REC].shape[0]

    count_deti_death = df.loc[COVID_D & AGE_18 & SCHOOL & DEATH].shape[0]
    count_deti_death_else = df.loc[
        COVID_D_E & AGE_18 & SCHOOL & COVID & DEATH
        ].shape[0]
    count_deti_else = df.loc[COVID & AGE_18 & SCHOOL & ISHOD_NO].shape[0]
    count_deti_amb = df.loc[COVID & AGE_18 & SCHOOL & AMB & ILL].shape[0]
    count_deti_stach = df.loc[COVID & AGE_18 & SCHOOL & STAC & ILL].shape[0]

    count_deti_ill_old = covid_sql(f"""
        SELECT [value_count] FROM [robo].[values]
            where id = (select max(id)
            from [robo].[values]
                where [value_name] = 'Всего школьников заболело от COVID'
                and date_rows = '{YESTERDAY}' )"""
                                   ).iat[0, 0]

    count_deti_rec_old = covid_sql(f"""
        SELECT [value_count] FROM [robo].[values]
            where id = (select max(id)
                from [robo].[values]
                    where value_name = 'Всего школьников выздоровело от COVID'
                and date_rows = '{YESTERDAY}' )"""
                                   ).iat[0, 0]

    count_deti_death_old = covid_sql(f"""
        SELECT [value_count] FROM [robo].[values]
            where id = (select max(id)
                from [robo].[values]
                    where [value_name] = 'Всего школьников умерло от COVID'
                and date_rows = '{YESTERDAY}' )"""
                                     ).iat[0, 0]

    MESS +=f""" ```
Отдельно по школьникам, больным COVID-19:
   Заболело:              {format(count_deti_ill,'n')}
   Заболело за день:      {format(count_deti_ill - count_deti_ill_old,'n')}
   Выздоровело:           {format(count_deti_rec,'n')}
   Выздоровело за день:   {format(count_deti_rec - count_deti_rec_old,'n')}
   Умерло:                {format(count_deti_death,'n')}
   Умерло за день:        {format(count_deti_death - count_deti_death_old,'n')}
   Умерло не от COVID-19: {format(count_deti_death_else,'n')}
   Другой исход:          {format(count_deti_else,'n')}
   Всего на амбулаторном: {format(count_deti_amb,'n')}
   Всего на стационарном: {format(count_deti_stach,'n')}
```
"""

    # Считаю детей с 01.01.2022
    df['Диагноз установлен'] = pd.to_datetime(
        df['Диагноз установлен'],
        format='%d.%m.%Y',
        errors='ignore'
        )

    DIAGNOZ_DATE = df['Диагноз установлен'] >= '2022-01-01'

    count_deti_ill = df.loc[COVID & AGE_18 & DIAGNOZ_DATE].shape[0]
    count_deti_rec = df.loc[COVID & AGE_18 & REC & DIAGNOZ_DATE].shape[0]
    count_deti_death = df.loc[COVID_D & AGE_18 & DEATH & DIAGNOZ_DATE].shape[0]

    MESS += f""" ```
Отдельно по детям, заболевшим с 01-01-2022
   Заболевшие дети:       {format(count_deti_ill,'n')}
   Выздовевшие дети:      {format(count_deti_rec,'n')}
   Умершие дети:          {format(count_deti_death,'n')}
    """

    # Форматируем даты

    for col in ['Диагноз установлен', 'Дата исхода заболевания']:
        df[col] = df[col].dt.strftime('%d.%m.%Y')

    # Записываем файл
    try:
        df.to_csv(FEDREG_FILE, index=False, sep=";", encoding='utf-8')
    except FileNotFoundError:
        os.mkdir(FEDREG_FILE.rsplit('/', 1)[0])
        MESS += '\n================================='
        MESS += '\nНе нашёл папку для ФР и создал её'
        df.to_csv(FEDREG_FILE, index=False, sep=";", encoding='utf-8')

    MESS += '```'

    return MESS
