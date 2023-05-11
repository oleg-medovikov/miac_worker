from pandas import DataFrame, concat, to_datetime
from datetime import datetime


def toxic_checker(df: 'DataFrame') -> 'DataFrame':
    """
    Проверка данныx:
    1) район принадлежит СПб
    2) не проставлена дата диагноза 303
    3) дата отравления 1104  меньше даты диагноза 303
    4) дата первичного обращения 1105 меньше даты диагноза 303
    """
    list_ = []

    # переводим даты из строк в даты
    df['303'] = to_datetime(df['303'],   format='%d.%m.%Y', errors='coerce')
    df['1104'] = to_datetime(df['1104'], format='%d.%m.%Y', errors='coerce')
    df['1105'] = to_datetime(df['1105'], format='%d.%m.%Y', errors='coerce')

    # район
    spb = df.loc[
        (df['1123'].isnull()) | ~(df['1123'].str.startswith('40', na=False))
        ]

    if len(spb):
        spb['Ошибка'] = 'район не принадлежит СПб'
        list_.append(spb)

    # нет даты диагноза 303
    r_303 = df.loc[df['303'].isnull()]

    if len(r_303):
        r_303['Ошибка'] = 'не проставлена дата диагноза 303'
        list_.append(r_303)
        df = df.loc[~df['303'].isnull()]

    # нет даты отравления 1104
    r_1104 = df.loc[df['1104'].isnull()]
    if len(r_1104):
        r_1104['Ошибка'] = 'не проставлена дата отравления 1104'
        list_.append(r_1104)
        df = df.loc[~df['1104'].isnull()]

    # нет даты первичного обращения 1105
    r_1105 = df.loc[df['1105'].isnull()]
    if len(r_1105):
        r_1105['Ошибка'] = 'не проставлена дата первичного обращения 1105'
        list_.append(r_1105)
        df = df.loc[~df['1105'].isnull()]

    # дата диагноза 303 > текущей даты
    d = df.loc[df['303'] > datetime.today()]
    if len(d):
        d['Ошибка'] = 'дата диагноза 303 > текущей даты'
        list_.append(d)

    # дата отравления 1104 > даты диагноза 303
    d = df.loc[df['1104'] > df['303']]
    if len(d):
        d['Ошибка'] = 'дата отравления 1104 позднее даты диагноза 303'
        list_.append(d)

    # дата отравления 1105 > даты диагноза 303
    d = df.loc[df['1105'] > df['303']]
    if len(d):
        d['Ошибка'] = 'первичное обращения 1105 позднее даты диагноза 303'
        list_.append(d)

    if len(list_):
        return concat(list_, ignore_index=True)

    return DataFrame()
