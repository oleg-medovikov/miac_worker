from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import os
import shutil
import glob

from clas import Dir
from base import covid_sql, covid_insert

from .svod_death_colums import svod_death_columns


def sbor_death_week_svod():
    """ Из собранных вы кучу файлов умерших за неделю
    собираем сводный файл с кучей цифр"""

    DATE_END = (datetime.today() + relativedelta(weeks=-1, weekday=2)).date()
    DATE_START = DATE_END - timedelta(days=6)

    MASK = Dir.get('death_week') \
        + f'/с {DATE_START} по {DATE_END}/[!~]*[!вод]*.xlsx'

    list_ = []

    for EXCEL in glob.iglob(MASK):
        PART = pd.read_excel(EXCEL)
        PART['file'] = EXCEL.rsplit('/', 1)[1]
        list_.append(PART)

    DF = pd.concat(list_)

    DF_FILE = 'temp/df_file.xlsx'
    DF.to_excel(DF_FILE)

    # Убираем пустые строки
    DF = DF.loc[~DF['Медицинская организация'].isnull()]
    DF = DF.loc[~DF['ФИО'].isnull()]
    DF.index = range(len(DF))

    # считаем количество дней до госпитализации
    DF['Ndays'] = (
        pd.to_datetime(DF['Дата госпитализации'], errors='coerce')
        - pd.to_datetime(DF['Дата начала заболевания'], errors='coerce')
        ).dt.days

    # проверяем изменился ли диагноз за неделю
    CHEAK = DF[['ФИО', 'Дата рождения', 'Посмертный диагноз']]

    covid_insert(CHEAK, 'cheak_diagnoz', 'tmp', True, 'replace')

    SQL = """
    select
        c.*, fr.[Посмертный диагноз] as 'Посмертный диагноз новый'
            from (
                select * from tmp.cheak_diagnoz ) as c
            left join (
            select * from robo.v_FedReg
            where [Исход заболевания] = 'Смерть'
                ) as fr
            on (c.[ФИО] = fr.[ФИО] and c.[Дата рождения] = fr.[Дата рождения])
        where  c.[Посмертный диагноз] <> fr.[Посмертный диагноз]
        order by [index]
    """

    CHEAK = covid_sql(SQL)

    # меняем диагнозы, которые изменились
    for i in range(len(CHEAK)):
        index = int(CHEAK.at[i, 'index'])
        diagnoz = CHEAK.at[i, 'Посмертный диагноз новый']
        DF.loc[index, 'Посмертный диагноз'] = diagnoz

    SVOD = covid_sql(f"exec robo.death_week_value'{DATE_START}','{DATE_END}'")

    SVOD.fillna(0, inplace=True)
    YES = ['да', 'Да']

    for i in range(len(SVOD)):
        # определяем мед организацию
        MO = SVOD.at[i, 'Медицинская организация']

        # различные поиски
        MO = DF['Медицинская организация'].isin([MO])
        AMB = DF['Факт обращения за медицинской помощью на амбулаторном этапе (да/нет)'].isin(YES)
        BLT = DF['Факт получения бесплатной лекарственной терапии (БЛТ) на амбулаторном этапе (да/нет)'].isin(YES)
        NDAY = DF['Ndays'] > 5
        ORIT = DF['Поступление в ОРИТ  при госпитализации (да/нет)'].isin(YES)
        KT = DF['Факт выполнения КТ на амбулаторном этапе (да/нет)'].isin(YES)
        PCR = DF['Факт выполнения ПЦР-SARS-CoV-2  на амбулаторном этапе (да/нет)'].isin(YES)
        ACT = DF['Факт получения антицитокиновой терапии в стационаре (да/нет)'].isin(YES)

        U071 = DF['Посмертный диагноз'].isin(['U07.1'])
        U072 = DF['Посмертный диагноз'].isin(['U07.2'])
        J189 = DF['Посмертный диагноз'].isin(['J18.9'])

        HEAVY = DF['Степень тяжести состояния при госпитализации (легкая, ср.тяжести, тяжелая)'].str.contains('яжел')

        SVOD.loc[i, 'J'] = DF[MO & AMB & U071].shape[0]
        SVOD.loc[i, 'K'] = DF[MO & AMB & U072].shape[0]
        SVOD.loc[i, 'L'] = DF[MO & AMB & J189].shape[0]

        SVOD.loc[i, 'N'] = DF[MO & BLT & U071].shape[0]
        SVOD.loc[i, 'M'] = DF[MO & BLT & U072].shape[0]

        SVOD.loc[i, 'O'] = DF[MO & NDAY & U071].shape[0]
        SVOD.loc[i, 'P'] = DF[MO & NDAY & U072].shape[0]
        SVOD.loc[i, 'Q'] = DF[MO & NDAY & J189].shape[0]

        SVOD.loc[i, 'R'] = DF[MO & HEAVY & U071].shape[0]
        SVOD.loc[i, 'S'] = DF[MO & HEAVY & U072].shape[0]
        SVOD.loc[i, 'T'] = DF[MO & HEAVY & J189].shape[0]

        SVOD.loc[i, 'U'] = DF[MO & ORIT & HEAVY & U071].shape[0]
        SVOD.loc[i, 'V'] = DF[MO & ORIT & HEAVY & U072].shape[0]
        SVOD.loc[i, 'W'] = DF[MO & ORIT & HEAVY & J189].shape[0]

        SVOD.loc[i, 'X'] = DF[MO & KT & U071].shape[0]
        SVOD.loc[i, 'Y'] = DF[MO & KT & U072].shape[0]
        SVOD.loc[i, 'Z'] = DF[MO & KT & J189].shape[0]

        SVOD.loc[i, 'AA'] = DF[MO & PCR & U071].shape[0]
        SVOD.loc[i, 'AB'] = DF[MO & PCR & U072].shape[0]
        SVOD.loc[i, 'AC'] = DF[MO & PCR & J189].shape[0]

        SVOD.loc[i, 'AP'] = DF[MO & ACT & U071].shape[0]
        SVOD.loc[i, 'AQ'] = DF[MO & ACT & U072].shape[0]
        SVOD.loc[i, 'AR'] = DF[MO & ACT & J189].shape[0]

    # в готовом своде переименовываем колонки
    SVOD.rename(columns=svod_death_columns, inplace=True)

    # считаем какую-то сумму
    summ = SVOD['Из них (по данным ПАЗ или по данным Посмертного клинического диагноза): основная причина смерти - COVID-19  U07.1'].sum() \
        + SVOD['Из них, U07.2'].sum() \
        + SVOD['Из них, Внебольничные пневмонии'].sum()

    sp = pd.DataFrame()

    def add_stroka_one(name, u071, u072, vpb):
        DICT = {
            'Столбец': name,
            'Всего': u071 + u072 + vpb,
            'U07.1':  u071,
            'U07.1 (процент)': round(100 * u071 / summ, 1),
            'U07.2':  u072,
            'U07.2 (процент)': round(100 * u072 / summ, 1),
            'Пневмонии':  vpb,
            'Пневмонии (процент)': round(100 * vpb / summ, 1),
            }
        sp.append(DICT, ignore_index=True)

    def add_stroka(name, u071, u072, vpb):
        DICT = {
            'Столбец': name,
            'Всего': u071 + u072 + vpb,
            'U07.1': u071,
            'U07.1 (процент)': round(100 * u071 / sp.at[0, 'U07.1'], 1),
            'U07.2':  u072,
            'U07.2 (процент)': round(100 * u072 / sp.at[0, 'U07.2'], 1),
            'Пневмонии': vpb,
            'Пневмонии (процент)': round(100 * vpb / sp.at[0, 'Пневмонии'], 1),
            }
        sp.append(DICT, ignore_index=True)

    def add_stroka_free(name, u071, u072):
        DICT = {
            'Столбец':  name,
            'Всего': u071 + u072,
            'U07.1': u071,
            'U07.1 (процент)':  round(100 * u071 / sp.at[2, 'U07.1'], 1),
            'U07.2': u072,
            'U07.2 (процент)':  round(100 * u072 / sp.at[2, 'U07.2'], 1),
            'Пневмонии': 0,
            'Пневмонии (процент)': 0,
            }
        sp.append(DICT, ignore_index=True)

    add_stroka_one(
        'Умерли U07.1, U07.2, пневмонии за неделю',
        SVOD['Из них (по данным ПАЗ или по данным Посмертного клинического диагноза): основная причина смерти - COVID-19  U07.1'].sum(),
        SVOD['Из них, U07.2'].sum(),
        SVOD['Из них, Внебольничные пневмонии'].sum()

    )

    add_stroka(
        'Умерших в возрасте до 60 лет',
        SVOD['Количество умерших в возрасте до 60 лет (U07.1)'].sum(),
        SVOD['Количество умерших в возрасте до 60 лет (U07.2)'].sum(),
        SVOD['Количество умерших в возрасте до 60 лет (пневмонии)'].sum()
    )

    add_stroka(
        'Обращались за медицинской помощью на догоспитальном этапе',
        SVOD['Количество пациентов, умерших от U07.1, обращавшихся за медицинской помощью на амбулаторном этапе'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, обращавшихся за медицинской помощью на амбулаторном этапе'].sum(),
        SVOD['Количество пациентов, умерших от внебольничной пневмонии, обращавшихся за медицинской помощью на амбулаторном этапе'].sum()
    )

    add_stroka_free(
        'Получавшие бесплатную лекарственную терапию',
        SVOD['Количество пациентов, умерших от U07.1, получавших бесплатное лекарственное лечение амбулаторно'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, получавших бесплатное лекарственное лечение амбулаторно'].sum()
    )

    add_stroka(
        'Поступили через 5 дней и более от начала заболевания',
        SVOD['Количество пациентов, умерших от U07.1, поступивших в стационар после 5  дней после начала заболевания'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, поступивших в стационар после 5 дней после начала заболевания'].sum(),
        SVOD['Количество пациентов, умерших от внебольничной пневмонии, поступивших в стационар после 5  дней после начала заболевания'].sum()
    )

    add_stroka(
        'Поступили в тяжелом состоянии',
        SVOD['Количество пациентов, умерших от U07.1, поступивших в стационар в тяжелом состоянии'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, поступивших в стационар в тяжелом состоянии'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, поступивших в стационар в тяжелом состоянии'].sum()
    )


    add_stroka(
        'Поступили в тяжелом состоянии (поступили в ОРИТ)',
        SVOD['Количество пациентов, умерших от U07.1, поступивших в стационар в тяжелом состоянии в ОРИТ'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, поступивших в стационар в тяжелом состоянии в ОРИТ'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, поступивших в стационар в тяжелом состоянии в ОРИТ'].sum()
    )

    add_stroka(
        'Выполнялась КТ на амбулаторном этапе',
        SVOD['Количество пациентов, умерших от U07.1, которым на амбулаторном этапе выполнялась КТ'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, которым на амбулаторном этапе выполнялась КТ'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, которым на амбулаторном этапе выполнялась КТ'].sum()
    )
    add_stroka(
        'Выполнялась ПЦР на амбулаторном этапе',
        SVOD['Количество пациентов, умерших от U07.1, которым на амбулаторном этапе выполнялась ПЦР-SARS-CoV-2'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, которым на амбулаторном этапе выполнялась ПЦР-SARS-CoV-2'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, которым на амбулаторном этапе выполнялась ПЦР-SARS-CoV-2'].sum()
    )

    add_stroka(
        'Получали антицитокиновую терапию',
        SVOD['Количество пациентов, умерших от U07.1, получавших в стационаре антицитокиновую терапию (АЦТ)'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, получавших в стационаре АЦТ'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, получавших в стационаре АЦТ'].sum()
    )

    add_stroka(
        'Сопутствующая ИБС',
        SVOD['Количество пациентов, умерших от U07.1, имеющих ИБС'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, имеющих ИБС'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, имеющих ИБС'].sum()
    )

    add_stroka(
        'Сопутствующий СД',
        SVOD['Количество пациентов, умерших от U07.1, имеющих СД'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, имеющих СД'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, имеющих СД'].sum()
    )

    add_stroka(
        'Сопутствующий артериальная гипертония',
        SVOD['Количество пациентов, умерших от U07.1, имеющих АГ'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, имеющих АГ'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, имеющих АГ'].sum()
    )

    add_stroka(
        'Сопутствующий ожирение',
        SVOD['Количество пациентов, умерших от U07.1, имеющих ожирение'].sum(),
        SVOD['Количество пациентов, умерших от U07.2, имеющих ожирение'].sum(),
        SVOD['Количество пациентов, умерших от ВБП, имеющих ожирение'].sum()
    )

    #  ========== Расчёт районов ==================

    DF['Район проживания'].fillna('Пустое значение', inplace=True)
    DF['Район проживания'] = ['Район проживания'].str.lower()

    DF['Возраст'] = pd.to_numeric(DF['Возраст'], errors='coerce')

    ZONE = pd.DataFrame()

    for Area in DF['Район проживания'].unique():

        AREA = DF['Район проживания'].isin([Area])
        DDAY = DF['Смерть наступила в первые сутки с момента госпитализации (да/нет)'].isin(['да'])
        AGE = DF['Возраст'] >= 60

        DICT = {
            'Район проживания': Area,
            'Количество умерших': DF.loc[AREA].shape[0],
            'из них: в первые сутки': DF.loc[AREA & DDAY].shape[0],
            'из них: возраст старше 60': DF.loc[AREA & DDAY & AGE].shape[0],
            }
        ZONE.append(DICT, ignore_index=True)

    FILE_SVOD = f'temp/Умершие за неделю с {DATE_START} по {DATE_END} свод.xlsx'

    with pd.ExcelWriter(FILE_SVOD) as writer:
        SVOD.to_excel(writer, sheet_name='Свод по МО', index=False)
        sp.to_excel(writer, sheet_name='Проценты', index=False)
        ZONE.to_excel(writer, sheet_name='Умершие по районам', index=False)
        CHEAK.to_excel(writer, sheet_name='Изменившиеся диагнозы', index=False)

    return FILE_SVOD
