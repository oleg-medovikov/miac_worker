import pandas as pd
from glob import glob
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


def regiz_load_to_base():
    "Загрузка файликов от МО в базу NCRN"

    MO = pd.read_excel(Dir.get('regiz_svod') + '/mo_directory.xlsx')
    update_mo_directory(MO)
    ncrn_exec('TRUNCATE TABLE dbo.TempTableFromMO')

    MASK = Dir.get('regiz') + '/ori.regiz*/_Входящие/[!~]*.xls'

    FILES = glob(MASK) + glob(MASK + 'x')

    list_ = []
    REMOVE_FILE = []
    STAT = pd.DateFrame()
    DF = pd.DateFrame()
    MIS = org_mis

    for FILE in FILES:
        # Узнаем параметры файла
        USER = FILE.split('/')[5]

        # организация
        if len(MO.loc[MO.ftp_user == USER, 'MO']):
            ORGANIZATION = MO.loc[MO.ftp_user == USER, 'MO'].values[0]
        else:
            ORGANIZATION = 'Не определена'

        # файлы рядом в той же директории
        OTHER_FILES = str(glob(file.rsplit('/',1)[0] + '/*'))

        # узнаем МИС
        if len(MIS.loc[MIS.ftp_user == USER]):
            NAME_MIS = MIS.loc[MIS.ftp_user == USER, 'NameMIS'].values[0]
        else:
            NAME_MIS = 'Не определена'

        # размер файла
        if os.path.getsize(FILE) == 0:
            STAT = STAT.append({
                'MOName':        ORGANIZATION,
                'NameFile':      FILE,
                'CountRows':     0,
                'TextError':     'Файл пустой, нулевого размера',
                'OtherFiles':    OTHER_FILES,
                'mis':           NAME_MIS,
                'DateLoadFile':  datetime.now(),
                'InOrOut':       'IN'
                }, ignore_index=True)
            continue





