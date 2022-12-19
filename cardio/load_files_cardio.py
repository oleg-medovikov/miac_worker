import pandas as pd
import glob
import re
import os

from .ColumnName import ColumnName, NAMES
from clas import Dir
from base import dn122_sql, dn122_insert


PATH = Dir.get('CARDIO')
COLUMS = ColumnName.all_names(NAMES)


class my_except(Exception):
    pass


def clear_number(STR: str) -> str:
    "Функция очищает поле телефона от лишнего мусора"
    TEL = {
        pd.isnull(STR): [''],
        ',' in STR: ''.join(re.findall(r'[\d,]', STR)).split(','),
        ';' in STR: ''.join(re.findall(r'[\d;]', STR)).split(';'),
        '()' in STR: ''.join(re.findall(r'[\d\(\)]', STR)).split('()'),
        '.0' in STR: ''.join(re.findall(r'[\d.]', STR)).split('.0'),
        '\\' in STR: ''.join(re.findall(r'[\d\\]', STR)).split('\\'),
        '/' in STR: ''.join(re.findall(r'[\d/]', STR)).split('/'),
        ' ' in STR and len(re.findall(r'[\d]', STR)) > 11:
            ''.join(re.findall(r'[\d ]', STR)).split(' '),
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


def clear_df(DF: 'pd.DataFrame') -> 'pd.DataFrame':
    "очистка от пустых колонок, лишних пробелов и подобного"

    DF.fillna('', inplace=True)

    for COL in DF.columns:
        DF[COL] = DF[COL].astype(str)
        DF[COL] = DF[COL].str.replace('\n', '')
        DF[COL] = DF[COL].str.replace('\t', ' ')
        DF[COL] = DF[COL].str.replace(' {2,}', ' ', regex=True)
        DF[COL] = DF[COL].str.strip()
        DF[COL] = DF[COL].str.replace('nan', '')
        DF[COL] = DF[COL].str.replace('None', '')

    return DF.drop_duplicates()


def check_phones(DF: 'pd.DataFrame') -> tuple['pd.DataFrame', int]:
    "Переделываем номера и отправляем ошибки обратно"
    CON_1 = 'Телефон пациента (мобильный)'
    CON_2 = 'Телефон пациента (домашний)'

    DF[CON_1 + '_'] = DF[CON_1].apply(clear_number)
    DF[CON_2 + '_'] = DF[CON_2].apply(clear_number)
    Error_Phone = DF[(DF[CON_1 + '_'] == '') & (DF[CON_2 + '_'] == '')]

    FILE = DF['file'].unique()[0]

    if len(Error_Phone):
        NAME = PATH + '/' \
                + FILE.rsplit('/', 1)[0] + '/Error_Phone'
        try:
            os.mkdir(NAME)
        except FileExistsError:
            pass

        NAME += '/' + FILE.rsplit('/', 1)[1]
        Error_Phone.to_excel(NAME, index=False)

    DF[CON_1] = DF[CON_1 + '_']
    DF[CON_2] = DF[CON_2 + '_']
    del DF[CON_1 + '_']
    del DF[CON_2 + '_']

    DF = DF[(DF[CON_1] != '') | (DF[CON_2] != '')]

    return DF, len(Error_Phone)


def clear_birthday(DF: 'pd.DataFrame') -> 'pd.DataFrame':
    DF['Дата рождения'] = pd.to_datetime(
        DF['Дата рождения'],
        errors='coerce'
        ).dt.strftime('%d.%m.%Y')
    DF.fillna('', inplace=True)
    return DF


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
    'GUID структурного подразделения врача, осуществляющего ДН':
        'GUIDDepartSpecial',
    'Дата необходимой записи на приём (месяц и год)': 'DatePriem',
    }


def load_file(FILE: str, MO: 'pd.DataFrame') -> dict:
    "функция обработки и загрузки файла"
    Dict = {
        'mess': 'файл прочитан',  # сообщение
        'res': False,  # удалось ли загрузить
        'all': 0,  # сколько строк в файле
        'error_phone': 0,  # сколько строк без телефонов
        'clear': 0,  # сколько хороших строк
        'load': 0,  # сколько загрузилось
        }

    # читаем файл
    try:
        DF = pd.read_excel(FILE, usecols=COLUMS, dtype=str)
    except Exception as e:
        Dict['mess'] = 'ошибка прочтения \n' + str(e)
        Dict['mess'].replace(
            'Usecols do not match columns, columns expected but not found',
            'Не найдены колонки: '
                )
        return Dict
    else:
        Dict['all'] = len(DF)

    # записываем путь файла и узнаем юзера организации
    DF['file'] = FILE.split('CARDIO/')[-1]
    ACCOUNT = FILE.split('/')[5].split('.')[2]

    try:
        DF['MO'] = MO.loc[
            MO['Account'].str.contains(ACCOUNT),
            'Name'
            ].iat[0]
        DF['OID'] = MO.loc[
            MO['Account'].str.contains(ACCOUNT),
            'Oid'
            ].iat[0]
    except IndexError:
        Dict['mess'] = 'директория не найдена в списке МО'
        return Dict
    # очистка данных
    try:
        DF = clear_df(DF)
    except Exception as e:
        Dict['mess'] = 'ошибка при обработке данных \n' + str(e)
        return Dict
    # переделываем телефоны
    try:
        DF, Error_count = check_phones(DF)
    except Exception as e:
        Dict['mess'] = 'ошибка при проверке телефонов \n' + str(e)
        return Dict
    else:
        Dict['error_phone'] = Error_count
    # Чистим день рождения
    try:
        DF = clear_birthday(DF)
    except Exception as e:
        Dict['mess'] = 'ошибка при очистке дня рождения \n' + str(e)
        return Dict
    # чистим пол
    try:
        DF['Пол'] = DF['Пол'].apply(clear_sex)
    except Exception as e:
        Dict['mess'] = 'ошибка при очистке пола \n' + str(e) + str(DF.columns)
        return Dict
    # чистим СНИЛС
    try:
        DF['Номер СНИЛС'] = DF['Номер СНИЛС'].apply(clear_snils)
    except Exception as e:
        Dict['mess'] = 'ошибка при очистке СНИЛС \n' + str(e)
        return Dict
    # считаем хеши строк
    try:
        DF['md5'] = calculate_hash(DF)
    except Exception as e:
        Dict['mess'] = 'ошибка при расчете хеша \n' + str(e)
        return Dict

    # считаем количество оставшихся строк
    Dict['clear'] = len(DF)
    if Dict['clear'] == 0:
        Dict['mess'] = 'Нет строк для загрузки'
        return Dict

    """
    Поехали сравнивать хеши файла с базой
    просто ищем разность

    OLD - это хеши которые есть в базе
    DF  - все хеши из файла
    NEW - новые хеши - разность, которую нужно добавить в базу
    """

    OLD = dn122_sql('SELECT md5_hash from oleg.Patient')
    NEW = DF[~DF['md5'].isin(OLD['md5_hash'].unique())]

    NEW.rename(columns=Dict_columns, inplace=True)
    NEW = NEW[Dict_columns.values()]

    NEW['DatePriem'] = NEW['DatePriem'].astype(str)

    NEW.fillna('', inplace=True)
    NEW.drop_duplicates(subset=['md5_hash'], inplace=True)

    try:
        dn122_insert(NEW, 'Patient', 'oleg', False, 'append')
    except Exception as e:
        Dict['mess'] = 'ошибка загрузки в базу \n' + str(e)[:200]
        return Dict
    else:
        Dict['mess'] = 'файл загружен'
        Dict['res'] = True
        Dict['load'] = len(NEW)
        return Dict


def replace_file(FILE: str) -> str:
    "Переносим файл в архив после удачной загрузки"

    NAME = FILE.rsplit('/', 1)[0] + '/Архив'
    try:
        os.mkdir(NAME)
    except FileExistsError:
        pass
    NAME += '/' + FILE.rsplit('/', 1)[1]

    try:
        os.replace(FILE, NAME)
    except Exception as e:
        return f'прочитал файл, но не смог перенести в архив \n{str(e)}'
    else:
        return 'файл перенесён в архив'


def load_files_cardio():
    MASK = PATH + '/ori.cardio.[!1]*/*_122/[!~]*.xls*'

    STAT = pd.DataFrame()
    MO = pd.read_excel('help/MO_cardio.xlsx')

    for FILE in glob.iglob(MASK):
        k = len(STAT)
        STAT.loc[k, 'file'] = FILE
        try:
            DICT = load_file(FILE, MO)
        except Exception as e:
            RES = False
            STAT.loc[k, 'mess2'] = str(e)
            continue
        else:
            RES = DICT['res']
            STAT.loc[k, 'mess'] = DICT['mess']
            STAT.loc[k, 'all'] = DICT['all']
            STAT.loc[k, 'error_phone'] = DICT['error_phone']
            STAT.loc[k, 'clear'] = DICT['clear']
            STAT.loc[k, 'load'] = DICT['load']

        if RES:
            STAT.loc[k, 'mess2'] = replace_file(FILE)
        else:
            STAT.loc[k, 'mess2'] = 'файл оставлен на месте'

    # приведём в порядок файл статистики
    STAT = STAT[[
        'file', 'all', 'error_phone',
        'clear', 'load', 'mess', 'mess2'
        ]]

    STAT.rename(columns={
        'file': 'Файл',
        'all': 'Всего строк в файле',
        'error_phone': 'строк без телефонов',
        'clear': 'строк после проверки',
        'load': 'строк загружено',
        'mess': 'статус загрузки',
        'mess2': 'статус файла',
        }, inplace=True)

    STAT_FILE = 'temp/cardio_loads_files.xlsx'
    STAT.to_excel(STAT_FILE)

    return STAT_FILE
