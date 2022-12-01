import pandas as pd
from datetime import datetime, timedelta
import glob
from os.path import getmtime

from clas import Dir


def svod_death():
    """непонятный отчёт по умершим, непонятно кому нужен
    собираю то, что Анастасия раскладывает в 5 вечером"""

    print(1)
    PATH_OTCH = Dir.get('svod_death')
    DATE_OTCH = (datetime.now() - timedelta(days=2)).strftime("%Y.%m.%d")

    print(PATH_OTCH)
    FILES = glob.glob('/mnt/FTP/EPID/COVID/EPID.COVID.*/*/*COVID_Умершие_*.xlsx')
    FILES += glob.glob('/mnt/FTP/EPID/COVID/EPID*/EPID*/*COVID_Умершие_*.xlsx')

    DF = pd.DataFrame(FILES, columns=['files'])

    # находим файлы с нужной датой в названии
    DF['date'] = DF['files'].str.findall(DATE_OTCH)

    DF = DF.loc[DF['date'].str.len() > 0]

    DF[['path', 'name']] = DF['files'].str.rsplit('/', n=1, expand=True)

    # узнаем дату изменения файлов и выбираем последний
    def get_time_change(x):
        t = datetime.fromtimestamp(getmtime(x))
        return t.strftime('%Y-%m-%d %H:%M:%S')

    DF['time'] = DF['files'].apply(get_time_change)

    DF = DF.sort_values['time'].drop_duplicates(['name'], keep='last')

    # создаем сводный файл
    list_ = []
    for i in DF.index:
        OTCHET = pd.read_excel(DF.at[i, 'files'])
        OTCHET['Дата загрузки'] = DF.at[i, 'time']
        list_.append(OTCHET)

    SVOD = pd.concat(list_)

    del SVOD['№ п/п']

    # обновляем индексы у свода
    SVOD.index = range(len(SVOD))

    # формируем имя файла
    NAME = (PATH_OTCH + '\\' + 'Свод по умершим за ' + DATE_OTCH + '.xlsx')
    with pd.ExcelWriter(NAME) as writer:
        SVOD.to_excel(writer, sheet_name='свод')
        DF['files'].to_excel(writer, sheet_name='список файлов')

    return "Сформирован свод по умершим за день"
