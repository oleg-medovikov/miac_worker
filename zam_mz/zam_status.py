import pandas as pd
import glob
from datetime import datetime


from clas import Dir

def zamechania_stat():
    PATH = Dir.get('zam_status')
    
    df = pd.DataFrame()

    for FILE in glob.glob(PATH):
        NAME = FILE.rsplit('/',1)[-1]

        try:
            DATE = datetime.strptime(NAME[0:10], '%Y-%m-%d')
        except:
            continue

        df.loc[len(df)  , 'file'] = FILE
        df.loc[len(df)-1, 'date'] = DATE
        df.loc[len(df)-1, 'type'] = NAME[11:-5]


    DATE_MAX = df['date'].max()

    df = df.loc[df['date'] == DATE_MAX ]

    _1 = df.loc[df['type'] == 'Без исхода 30 дней' ].size
    _2 = df.loc[df['type'] == 'Нет амбулаторного этапа' ].size
    _3 = df.loc[df['type'] == 'Нет амбулаторного этапа, умер от COVID' ].size
    _4 = df.loc[df['type'] == 'Нет данных ОМС' ].size
    _5 = df.loc[df['type'] == 'нет дневниковых записей' ].size
    _6 = df.loc[df['type'] == 'Нет СНИЛСа' ].size
    _7 = df.loc[df['type'] == 'зависшие статусы' ].size
    _8 = df.loc[df['type'] == 'зависшие статусы без МО прикрепления' ].size
    _9 = df.loc[df['type'] == 'неверный вид лечения' ].size
    _A = df.loc[df['type'] == 'нет ПАЗ' ].size
    _B = df.loc[df['type'] == 'Сверка ФР и ежедневного отчёта' ].size

    mess = f"``` Последние замечания разложены за {DATE_MAX.strftime('%Y-%m-%d')}"
    mess += '\n' + '='*len(mess)

    mess +=f"""
Без исхода 30 дней:        {_1}{' '*(3 - len(str(_1)))} файлов
Нет амбулаторного этапа:   {_2}{' '*(3 - len(str(_2)))} файлов
Нет амб. этапа умер U07.1: {_3}{' '*(3 - len(str(_3)))} файлов
Нет данных ОМС:            {_4}{' '*(3 - len(str(_4)))} файлов
Нет дневниковых записей:   {_5}{' '*(3 - len(str(_5)))} файлов
Нет СНИЛСа:                {_6}{' '*(3 - len(str(_6)))} файлов
Зависшие статусы:          {_7}{' '*(3 - len(str(_7)))} файлов
Зависшие статусы без МО:   {_8}{' '*(3 - len(str(_8)))} файлов
Неверный вид лечения:      {_9}{' '*(3 - len(str(_9)))} файлов
Нет ПАЗ:                   {_A}{' '*(3 - len(str(_A)))} файлов
Сверка ФР и ежед. отчёта:  {_B}{' '*(3 - len(str(_B)))} файлов
"""
    mess += '```'

    return mess
