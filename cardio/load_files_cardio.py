import pandas as pd
import glob
import re
import os

from .ColumnName import ColumnName, NAMES
from clas import Dir
from base import dn122_sql, dn122_insert


class my_except(Exception):
    pass


def clear_number(STR: str) -> str:
    "Функция очищает поле телефона от лишнего мусора"
    TEL = {
        pd.isnull(STR): [''],
        ',' in STR: ''.join(re.findall(r'[\d,]', STR)).split(','),
        ';' in STR: ''.join(re.findall(r'[\d;]', STR)).split(';'),
        '()' in STR: ''.join(re.findall(r'[\d()]', STR)).split('()'),
        '.0' in STR: ''.join(re.findall(r'[\d.]', STR)).split('.0'),
        '\\' in STR: ''.join(re.findall(r'[\d\\]', STR)).split('\\'),
        '/' in STR: ''.join(re.findall(r'[\d/]', STR)).split('/'),
        ' ' in STR: ''.join(re.findall(r'[\d ]', STR)).split(' '),
    }.get(True, [''.join(re.findall(r'[\d/]', STR))])

    for i, PART in enumerate(TEL):
        TEL[i] = {
            len(PART) == 11:
                f'+7({PART[1:4]})-{PART[4:7]}-{PART[7:9]}-{PART[9:]}',
            len(PART) == 10:
                f'+7({PART[0:3]})-{PART[3:6]}-{PART[6:8]}-{PART[8:]}',
            len(PART) == 7:
                f'+7(812)-{PART[0:3]}-{PART[3:5]}-{PART[5:]}',
            len(PART) == 12 and PART[:2] == '78':
                f'+7({PART[2:5]})-{PART[5:8]}-{PART[8:10]}-{PART[10:]}',
        }.get(True, '')

    return {
                len(TEL) == 1: TEL[0],
                len(TEL) > 1: ''.join(x + ', ' for x in TEL if len(x))[:-2],
            }.get(True, '')


def clear_snils(STR: str):
    "чистим СНИЛС"
    STR = ''.join(re.findall(r'\d', str(STR)))
    return {
        len(STR) == 11:
            f'{STR[0:3]}-{STR[3:6]}-{STR[6:9]} {STR[9:]}',
        len(STR) == 10:
            f'0{STR[0:2]}-{STR[2:5]}-{STR[5:8]} {STR[8:]}',
        len(STR) == 9:
            f'00{STR[0:1]}-{STR[1:4]}-{STR[4:7]} {STR[7:]}',
        len(STR) == 8:
            f'000-{STR[0:3]}-{STR[3:6]} {STR[6:]}',
    }.get(True, '')


def clear_sex(STR):
    return {
        'м' in STR.lower(): 'Мужской',
        'ж' in STR.lower(): 'Женский',
    }.get(True, '')


def clear_pasport_ser(STR):
    STR = ''.join(re.findall(r'\d', str(STR)))
    return {
        len(STR) == 4: f'{STR[0:2]} {STR[2:]}',
    }.get(True, '')


def calculate_hash(df):
    """Считаем хеш строк федерального регистра"""
    df['string'] = df['OID'] + \
        df['Фамилия'] + \
        df['Имя'] + \
        df['Отчество'] + \
        df['Дата рождения'] + \
        df['Пол'] + \
        df['Номер СНИЛС'] + \
        df['Телефон пациента (мобильный)'] + \
        df['Телефон пациента (домашний)'] + \
        df['Адрес пациента'] + \
        df['Серия паспорта'] + \
        df['Номер паспорта'] + \
        df['Серия полиса ОМС'] + \
        df['Номер полиса ОМС']

    df['string'] = df['string'].str.replace(' ', '')

    import hashlib
    from multiprocesspandas import applyparallel

    def func(x):
        return hashlib.md5(x.encode('cp1251')).hexdigest()

    return df['string'].apply_parallel(func, num_processes=10)


Dict_columns = {
    'md5': 'md5_hash',
    'file': 'file',
    'MO': 'MO',
    'Краткое наименование юр. лица МО': 'ShortNameMO',
    'Наименования подразделения МО':  'NameDepartMO',
    'OID': 'Oid',
    'Идентификатор пациента в МИС': 'PatientMOId',
    'Принадлежность адреса пациента к участку': 'Uchastok',
    'Локальный ID участка в МИС': 'UchastokId',
    'Фамилия': 'Surname',
    'Имя': 'FirstName',
    'Отчество': 'MiddleName',
    'Дата рождения': 'Birthday',
    'Пол': 'Sex',
    'Номер СНИЛС': 'Snils',
    'Телефон пациента (мобильный)': 'PhoneMob',
    'Телефон пациента (домашний)': 'Phone',
    'Адрес пациента': 'Adress',
    'Серия паспорта': 'Pasp_S',
    'Номер паспорта': 'Pasp_N',
    'Серия полиса ОМС': 'Polis_S',
    'Номер полиса ОМС': 'Polis_S',
    'Идентификатор врача, осуществляющего ДН': 'DoctorId',
    'Наименование специальности врача, осуществляющего ДН': 'SpecialName',
    'Идентификация специальности врача, осуществляющего ДН': 'SpecialId',
    'GUID структурного подразделения врача, осуществляющего ДН': 'GUIDDepartSpecial',
    'Дата необходимой записи на приём (месяц и год)': 'DatePriem',
    }


def load_files_cardio():
    PATH = Dir.get('CARDIO')
    MASK = PATH + '/ori.cardio.*/*_122/*.xls*'

    COLUMS = ColumnName.all_names(NAMES)
    list_ = []

    STAT = pd.DataFrame()
    MO = pd.read_excel('help/MO_cardio.xlsx')

    for FILE in glob.glob(MASK):
        k = len(STAT)
        STAT.loc[k, 'file'] = FILE

        try:
            DF = pd.read_excel(FILE, usecols=COLUMS, dtype=str)
        except Exception as e:
            STAT.loc[k, 'mess'] = 'ошибка ' + str(e)
            continue
        else:
            STAT.loc[k, 'mess'] = 'файл прочитан'

        DF['file'] = FILE.split('CARDIO/')[-1]
        ACCOUNT = FILE.split('/')[5].split('.')[2]

        try:
            DF['MO'] = MO.loc[
                MO['Account'].str.contains(ACCOUNT),
                'Name'].iat[0]
            DF['OID'] = MO.loc[
                MO['Account'].str.contains(ACCOUNT),
                'Oid'].iat[0]
        except IndexError:
            pass

        list_.append(DF.drop_duplicates())

        NAME = FILE.rsplit('/', 1)[0] + '/Архив'
        try:
            os.mkdir(NAME)
        except FileExistsError:
            pass
        NAME += '/' + FILE.rsplit('/', 1)[1]

        #os.replace(FILE, NAME)

        break

    DF = pd.concat(list_, ignore_index=True)
    DF.fillna('', inplace=True)

    if len(DF) == 0:
        raise my_except('Загрузка файлов кардио - нет новых файлов')

    # чистим номера телефонов
    CON_1 = 'Телефон пациента (мобильный)'
    CON_2 = 'Телефон пациента (домашний)'

    DF[CON_1 + '_'] = DF[CON_1].apply(clear_number)
    DF[CON_2 + '_'] = DF[CON_2].apply(clear_number)

    # возвращаем МО неправильные номера телефонов
    Error_Phone = DF[(DF[CON_1 + '_'] == '') & (DF[CON_2 + '_'] == '')]
    for FILE in Error_Phone['file'].unique():
        NAME = PATH + '/' + FILE.rsplit('/', 1)[0] + '/Error_Phone'

        try:
            os.mkdir(NAME)
        except FileExistsError:
            pass

        NAME += '/' + FILE.rsplit('/', 1)[1]
        PART = Error_Phone[Error_Phone['file'] == FILE]
        del PART[CON_1 + '_']
        del PART[CON_2 + '_']

        PART.to_excel(NAME, index=False)

    # после разложения удаляем колонки
    DF[CON_1] = DF[CON_1 + '_']
    DF[CON_2] = DF[CON_2 + '_']
    del DF[CON_1 + '_']
    del DF[CON_2 + '_']

    # удаляем строчки те, где нет телефонов
    DF = DF[(DF[CON_1] != '') | (DF[CON_2] != '')]

    # Чистим день рождения
    DF['Дата рождения'] = pd.to_datetime(
        DF['Дата рождения'],
        errors='coerce'
        ).dt.strftime('%d.%m.%Y')
    DF.fillna('', inplace=True)
    # чистим пол
    try:
        DF['Пол'] = DF['Пол'].apply(clear_sex)
    except KeyError:
        DF['Пол'] = ''

    # чистим СНИЛС
    DF['Номер СНИЛС'] = DF['Номер СНИЛС'].apply(clear_snils)

    # считаем хеши строк
    DF['md5'] = calculate_hash(DF)

    OLD = dn122_sql('SELECT md5_hash from oleg.Patient')

    """
    OLD - это хеши которые есть в базе
    DF  - все хеши которые прочитал из файликов
    NEW - новые хеши, которые нужно добавить в базу
          просто ищем разность
    """

    NEW = DF[~DF['md5'].isin(OLD['md5_hash'].unique())]

    NEW.rename(columns=Dict_columns, inplace=True)
    NEW = NEW[Dict_columns.values()]

    try:
        dn122_insert(NEW, 'Patient', 'oleg', False, 'append')
    except Exception as e:
        print(str(e))
        raise my_except(str(e)[:150])

    STAT.loc[0, 'Всего прочёл строк'] = len(DF)
    STAT.loc[0, 'Из них залил в базу'] = len(NEW)

    STAT_FILE = 'temp/cardio_loads_files.xlsx'
    STAT.to_excel(STAT_FILE)

    return STAT_FILE
