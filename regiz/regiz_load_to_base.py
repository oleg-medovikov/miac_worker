import pandas as pd
import glob
import os
from datetime import datetime

from base import ncrn_sql, ncrn_exec, ncrn_insert
from clas import Dir


def org_mis() -> 'pd.DateFrame':
    "узнать МИСы организаций"
    SQL = """
        SELECT org.ftp_user, ISNULL(ftp.NameMIS, '') AS 'NameMIS'
          FROM [nsi].[Organization] as org
            LEFT JOIN (SELECT DISTINCT [level1_key],
                      STUFF((SELECT CONCAT(',',[NameMIS])
                          FROM [nsi].[MISMO]
                          WHERE [level1_key]=t.[level1_key]
                          ORDER BY [NameMIS]
                          FOR XML PATH('')
                         ),1,1,'') AS 'NameMIS'
                    FROM [nsi].[MISMO] t) AS ftp
              ON (ftp.[level1_key] = org.level1_key)
          ORDER BY org.ftp_user
    """

    return ncrn_sql(SQL)


def update_mo_directory(DF: pd.DateFrame):
    "Если что-то изменилось в файлике - меняем в базе"
    DF.rename(columns={
        'ftp_user':   'ftp_user',
        'oid':        'OID',
        'level1_key': 'level1_key',
        'МО_краткое наименование': 'MONameSpr64',
        'MO':        'MOName',
        'MO_полное': 'MONameFull',
        'email':     'Email',
        'active':    'IsActive',
        'ИОГВ':      'IOGV',
        }, inplace=True)

    ncrn_insert(DF, 'Organization', 'nsi', False, 'replace')


NAMES = [
    'Номер истории болезни', 'Дата открытия СМО',
    'Признак амбулаторного СМО', 'СНИЛС врача'
    ]
NAMES_NEW = [
    'HistoryNumber', 'OpenDate',
    'IsAmbulant', 'SnilsDoctor'
    ]


def read_file(FILE: int, MO: 'pd.DateFrame', MIS: 'pd.DateFrame') -> dict:
    # Узнаем параметры файла
    USER = FILE.split('/')[5]

    if len(MO.loc[MO.ftp_user == USER, 'MO']):
        ORGANIZATION = MO.loc[MO.ftp_user == USER, 'MO'].values[0]
    else:
        ORGANIZATION = 'Не определена'

    # файлы рядом в той же директории
    OTHER_FILES = str(glob.glob(file.rsplit('/', 1)[0] + '/*'))

    # узнаем МИС
    if len(MIS.loc[MIS.ftp_user == USER]):
        NAME_MIS = MIS.loc[MIS.ftp_user == USER, 'NameMIS'].values[0]
    else:
        NAME_MIS = 'Не определена'

    Dict = {
        'MOName':        ORGANIZATION,
        'NameFile':      FILE,
        'CountRows':     0,
        'TextError':     '',
        'OtherFiles':    OTHER_FILES,
        'mis':           NAME_MIS,
        'DateLoadFile':  datetime.now(),
        'InOrOut':       'IN'
    }
    # размер файла
    if os.path.getsize(FILE) == 0:
        Dict['TextError'] = 'Файл пустой, нулевого размера'
        return Dict

    # да, разверзнется ад!
    try:
        DF = pd.read_excel(FILE, usecols=NAMES, dtype=str)
    except KeyError:
        Dict['TextError'] = 'Файл является листом excel, не могу прочитать'
        return Dict
    except XLRDError:  # если это html файл
        try:
            DF = pd.read_html(FILE)
        except ValueError:
            Dict['TextError'] \
                    = 'Файл является листом html, но не удалось распарсить'
            return Dict
        else:
            DF = pd.concat(DF)
            DF = DF[names].applymap(str)
            DF.columns = NAMES_NEW
            Dict['CountRows'] = len(DF)
            Dict['TextError'] = 'Файл HTMl удачно распарсен'
    except ValueError as e:  # Если не найдены колонки
        if str(e) == 'File is not a recognized excel file':
            try:
                DF = pd.read_html(file)
            except ValueError:
                Dict['TextError'] \
                    = 'Файл является листом html, но не удалось распарсить'
                return Dict
            else:
                if len(DF):
                    DF = pd.concat(DF)
                    DF = DF[names].applymap(str)
                    DF.columns = NAMES_NEW
                    Dict['CountRows'] = len(DF)
                    Dict['TextError'] = 'Файл HTMl удачно распарсен'
                else:
                    # если df пустой
                    Dict['CountRows'] = 0
                    Dict['TextError'] = 'Файл HTMl не удалось распарсить'
                    return Dict
        elif 'Excel file format cannot be determined' in str(e):
            # вообще непонятный файл
            Dict['CountRows'] = 0
            Dict['TextError'] = 'Файл HTMl не удалось распарсить'
            return Dict
        else:
            # ошибка, что не нашёл колонки таблицы
            try:
                DF = pd.read_excel(FILE, usecols=NAMES_NEW, dtype=str)
            except Exception as e:
                if len(pd.read_excel(FILE).columns) == 4:
                    # если в файле 4 колонки, то ищем шапку по строчкам
                    for i in range(10):
                        try:
                            DF = pd.read_excel(
                                    FILE,
                                    usecols=NAMES,
                                    skiprows=i,
                                    dtype=str
                                    )
                        except Exception as e:
                            if i == 9:
                                Dict['TextError'] = \
                                    'Не найдена одна из колонок'
                                return Dict
                        else:
                            DF.columns = NAMES_NEW
                            Dict['CountRows'] = len(DF)
                            Dict['TextError'] = \
                                f'Файл прочитан, но пришлось поискать шапку на строке номер {i}'
                            break
                else:
                    # если в файле не 4 колонки, то и пофигу на него
                    Dict['TextError'] = 'Файл не удалось прочитать'
                    return Dict
            else:
                # если у файла шапка NAMES_NEW - это файл что робот кладёт
                # игнорим
                Dict['TextError'] = 'Файл прочитан, но он уже был когда-то обработан'
                return Dict
    else:
        # если файл прочитан без проблем
        DF.columns = NAMES_NEW
        Dict['CountRows'] = len(DF)
        Dict['TextError'] = 'Файл прочитан без проблем'

    Dict['df'] = DF
    Dict['res'] = True
    return Dict


def regiz_load_to_base():
    "Загрузка файликов от МО в базу NCRN"

    MO = pd.read_excel(Dir.get('regiz_svod') + '/mo_directory.xlsx')
    MIS = org_mis()

    update_mo_directory(MO)
    ncrn_exec('TRUNCATE TABLE dbo.TempTableFromMO')

    MASK = Dir.get('regiz') + '/ori.regiz*/_Входящие/[!~]*.xls*'

    REMOVE_FILE = []
    STAT = pd.DateFrame()

    for FILE in glob.iglob(MASK):
        k = len(STAT)
        STAT.loc[k, 'NameFile'] = FILE
        try:
            Dict = read_file(FILE, MO, MIS)
        except Exception as e:
            STAT['TextError'] = str(e)
            continue
        else:
            STAT.loc[k, 'CountRows'] = Dict['CountRows']
            STAT.loc[k, 'DateLoadFile'] = Dict['DateLoadFile']
            STAT.loc[k, 'InOrOut'] = 'IN'
            STAT.loc[k, 'MOName'] = Dict['MOName']
            STAT.loc[k, 'OtherFiles'] = Dict['OtherFiles']
            STAT.loc[k, 'TextError'] = Dict['TextError']
            STAT.loc[k, 'mis'] = Dict['mis']

            REMOVE_FILE.append(FILE)





