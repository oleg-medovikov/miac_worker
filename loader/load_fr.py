import datetime, glob
import pandas as pd
import numpy

from clas import Dir
from base import covid_insert, covid_sql, covid_exec

NAMES = [
'п/н','Дата создания РЗ','УНРЗ','Дата изменения РЗ','СНИЛС',
'ФИО','Пол','Дата рождения','Диагноз','Диагноз установлен',
'Осложнение основного диагноза','Субъект РФ','Медицинская организация',
'Ведомственная принадлежность','Вид лечения','Дата госпитализации',
'Дата исхода заболевания','Исход заболевания','Степень тяжести',
'Посмертный диагноз','ИВЛ','ОРИТ','МО прикрепления','Медицинский работник'
    ]

class my_except(Exception):
    pass

def report_fr(df):
    """ Репорт о количестве выздоровевших """
    df ['Возраст'] = (pd.to_datetime(df['Диагноз установлен'], format='%d.%m.%Y') \
            - pd.to_datetime(df['Дата рождения'], format='%d.%m.%Y' ))/ numpy.timedelta64(1, 'Y')

    report = pd.DataFrame()
    report.loc[0,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[0,'value_name'] = 'Всего выздоровело от COVID'
    report.loc[0,'value_count'] = len(df[df['Исход заболевания'].isin(['Выздоровление']) & df['Диагноз'].isin(['U07.1'])])

    report.loc[1,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[1,'value_name'] = 'Всего на амбулаторном лечении от COVID'
    report.loc[1,'value_count'] = len(df.loc[(df['Исход заболевания'] == '' ) \
            & (df['Диагноз'].isin(['U07.1','U07.2']) | df['Диагноз'].str.contains('J1[2-8]') ) \
            & (df['Вид лечения'].isin(['Амбулаторное лечение']))] )

    report.loc[2,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[2,'value_name'] = 'Всего детей заболело от COVID'
    report.loc[2,'value_count'] = len(df.loc[ (df['Диагноз'].isin(['U07.1','U07.2'])) & ( df['Возраст'] < 18) ] )

    report.loc[3,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[3,'value_name'] = 'Всего детей выздоровело от COVID'
    report.loc[3,'value_count'] =  len(df.loc[ (df['Диагноз'].isin(['U07.1','U07.2'])) & ( df['Возраст'] < 18) \
            & (df['Исход заболевания'].str.contains('Выздоровление')) ])

    report.loc[4,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[4,'value_name'] = 'Всего детей умерло от COVID'
    report.loc[4,'value_count'] = len(df.loc[ (df['Посмертный диагноз'].isin(['U07.1','U07.2'])) & ( df['Возраст'] < 18)  \
            & (df['Исход заболевания'].isin(['Смерть']) ) ]) 

    report.loc[5,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[5,'value_name'] = 'Всего школьников заболело от COVID'
    report.loc[5,'value_count'] = len(df.loc[ (df['Диагноз'].isin(['U07.1','U07.2'])) & ( df['Возраст'] < 18) & (df['Возраст'] > 6 ) ] )

    report.loc[6,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[6,'value_name'] = 'Всего школьников выздоровело от COVID'
    report.loc[6,'value_count'] =  len(df.loc[ (df['Диагноз'].isin(['U07.1','U07.2'])) & ( df['Возраст'] < 18) & (df['Возраст'] > 6 ) \
            & (df['Исход заболевания'].str.contains('Выздоровление')) ])

    report.loc[7,'date_rows'] = pd.to_datetime(df['Дата создания РЗ'],format='%d.%m.%Y').max().date()
    report.loc[7,'value_name'] = 'Всего школьников умерло от COVID'
    report.loc[7,'value_count'] = len(df.loc[ (df['Посмертный диагноз'].isin(['U07.1','U07.2'])) & ( df['Возраст'] < 18) & (df['Возраст'] > 6) \
            & (df['Исход заболевания'].isin(['Смерть']) ) ]) 
    
    covid_insert(report, 'values', 'robo', False, 'append')


def calculate_hash(df):
    """Считаем хеш строк федерального регистра"""
    df['string']= df['СНИЛС'] + \
             df['ФИО'] + \
             df['Пол'] + \
             df['Дата рождения'] + \
             df['Диагноз'] + \
             df['Диагноз установлен'] + \
             df['Медицинская организация'] + \
             df['Дата исхода заболевания'] + \
             df['Исход заболевания'] + \
             df['Дата госпитализации'] + \
             df['Степень тяжести'] + \
             df['Посмертный диагноз'] + \
             df['ИВЛ'] + \
             df['ОРИТ'] + \
             df['Вид лечения'] + \
             df['Медицинский работник'] + \
             df['МО прикрепления']

    df['string'] = df['string'].str.replace(' ', '')

    import hashlib
    from multiprocesspandas import applyparallel

    def func(x):
        return hashlib.md5(x.encode('cp1251')).hexdigest()

    return df['string'].apply_parallel(func, num_processes=10)

def load_fr():
    """Загрузка федерального регистра"""
    PATH = Dir.get('path_robot') + '/' + datetime.datetime.now().strftime("%Y_%m_%d")

    FILE_CSV = glob.glob(PATH + '/Федеральный регистр лиц, больных *[!ИАЦ].csv')

    if len (FILE_CSV) == 0:
        raise my_except('Не найден файл Федерального регистра! Директория:\n' + PATH )

    FILE_CSV = FILE_CSV[0]

    try:
        DF = pd.read_csv(
                FILE_CSV,
                header=0,
                usecols=NAMES,
                na_filter = False,
                dtype = str,
                delimiter=';',
                engine='python',
                encoding = 'utf-8')
    except Exception as e:
        raise my_except(str(e))

    del DF ['Ведомственная принадлежность']
    del DF ['Осложнение основного диагноза']
    
    DF.drop_duplicates(subset=['УНРЗ'], keep='last', inplace=True)

    # Считаем хеш суммы строк
    DF ['md5'] = calculate_hash(DF)

    # Получаем хеш загруженного в базу регистра
    SQL = "SELECT UNRZ, hash_MD5 FROM dbo.hash_fr"
    FR = covid_sql(SQL)
    
    """
    FR_A - часть регистра, которая не изменилась
           md5 == hash_MD5

    FR_B - строки в старом регистре, которые изменились
           и которые следует удалить
           md5 is Null and hash_MD5 is not Null

    FR_C - новые строки регистра, которые нужно загрузить
           в cv_input_fr для дальнейшей обработки и 
           добавления в регистр
           md5 is not Null and hash_MD5 is Null
    """

    SVOD = DF.merge( FR, how='outer', left_on=['УНРЗ','md5'], right_on=['UNRZ','hash_MD5'])

    FR_C = SVOD.loc[ (~SVOD['md5'].isnull()) & (SVOD['hash_MD5'].isnull()) ]
    
    if len (FR_C) == 0:
        raise my_except('В базу загружен актуальный ФР!')

    del FR_C ['string']
    del FR_C ['hash_MD5']
    del FR_C ['UNRZ']
    FR_C.rename( columns={'md5': 'hash_md5'}, inplace=True )
    
    covid_exec('TRUNCATE TABLE dbo.cv_input_fr')
    covid_insert( FR_C, 'cv_input_fr', 'dbo', False, 'append' )

    FR_B = SVOD.loc[ (SVOD['md5'].isnull()) & (~SVOD['hash_MD5'].isnull()) ]
    
    FR_B = FR_B [[ 'UNRZ','hash_MD5' ]]

    covid_exec('TRUNCATE TABLE dbo.hash_fr_base')
    covid_insert( FR_B, 'hash_fr_base', 'dbo', False, 'append' )

    # Все данные загружены, запускаем процедуры обработки

    covid_exec('EXEC dbo.p_hash_md5')
    covid_exec('EXEC dbo.cv_Load_FedReg_new')

    # Отправляем числа статистики по выздоровевшим
    report_fr(DF)
    # Ещё один отчёт
    covid_exec('EXEC [mz].[p_Recalculate_for_50_Report]')

    mess = 'Регистр успешно загружен!' \
            + '\nИмя файла: '       + FILE_CSV.rsplit('/',1)[-1] \
            + '\nВсего строк: '     + str(len(DF)) \
            + '\nУдалено строк: '   + str(len(FR_B)) \
            + '\nДобавлено строк: ' + str(len(FR_C))

    return mess

