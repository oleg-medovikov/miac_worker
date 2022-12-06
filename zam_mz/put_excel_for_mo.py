import datetime
import os
import pandas as pd
from clas import Dir


def put_excel_for_mo(DF, NAME, DATE):
    "Раскладываем файлы по папкам организаций"

    if DATE is None:
        DATE = datetime.datetime.now().strftime('%Y-%m-%d')

    STAT = pd.DataFrame()

    ROOT = Dir.get('covid')

    for ORG in DF['Медицинская организация'].unique():

        STAT.loc[len(STAT), 'Медицинская организация'] = ORG

        PART = DF.loc[DF['Медицинская организация'] == ORG]
        PART.index = range(1, len(PART) + 1)
        PART.fillna(0, inplace=True)
        PART = PART.applymap(str)

        USER = Dir.get(ORG)

        if USER:
            PATH = ROOT + USER
            try:
                os.makedirs(PATH)
            except OSError:
                pass

            FILE = PATH + '/' + DATE + ' ' + NAME + '.xlsx'

            with pd.ExcelWriter(FILE) as writer:
                PART.to_excel(writer, sheet_name='унрз')

            STAT.loc[len(STAT) - 1, 'Статус'] = 'Файл положен'
            STAT.loc[len(STAT) - 1, 'Имя файла'] = FILE
        else:
            STAT.loc[len(STAT) - 1, 'Статус'] \
                    = 'Не найдена директория для файла'

    STAT.index = range(1, len(STAT) + 1)

    STAT_FILE = 'temp/отчёт по разложению ' + NAME + '.xlsx'

    with pd.ExcelWriter(STAT_FILE) as writer:
        STAT.to_excel(writer, sheet_name='унрз')

    return STAT_FILE


def put_excel_for_mo_2(DF_1, DF_2, NAME, NAME_1, NAME_2, DATE):
    "Раскладываем файлы по папкам организаций где 2 вкладки в файле"

    if DATE is None:
        DATE = datetime.datetime.now().strftime('%Y-%m-%d')

    STAT = pd.DataFrame()

    ROOT = Dir.get('covid')
    # нужно сложить все организации из 2 таблиц
    ORGANIZATIONS = DF_1['Медицинская организация']\
        .append(DF_2['Медицинская организация'])\
        .unique()

    for ORG in ORGANIZATIONS:

        STAT.loc[len(STAT), 'Медицинская организация'] = ORG

        PART_1 = DF_1.loc[DF_1['Медицинская организация'] == ORG]
        PART_1.index = range(1, len(PART_1) + 1)
        PART_1.fillna(0, inplace=True)
        PART_1 = PART_1.applymap(str)

        PART_2 = DF_2.loc[DF_2['Медицинская организация'] == ORG]
        PART_2.index = range(1, len(PART_2) + 1)
        PART_2.fillna(0, inplace=True)
        PART_2 = PART_2.applymap(str)

        USER = Dir.get(ORG)

        if USER:
            PATH = ROOT + USER
            try:
                os.makedirs(PATH)
            except OSError:
                pass

            FILE = PATH + '/' + DATE + ' ' + NAME + '.xlsx'

            with pd.ExcelWriter(FILE) as writer:
                PART_1.to_excel(writer, sheet_name=NAME_1)
                PART_2.to_excel(writer, sheet_name=NAME_2)

            STAT.loc[len(STAT) - 1, 'Статус'] = 'Файл положен'
            STAT.loc[len(STAT) - 1, 'Имя файла'] = FILE
        else:
            STAT.loc[len(STAT) - 1, 'Статус'] \
                    = 'Не найдена директория для файла'

    STAT.index = range(1, len(STAT) + 1)

    STAT_FILE = 'temp/отчёт по разложению ' + NAME + '.xlsx'

    with pd.ExcelWriter(STAT_FILE) as writer:
        STAT.to_excel(writer, sheet_name='унрз')

    return STAT_FILE
