import pandas as pd

from base import dn122_sql
from clas import Dir


class my_except(Exception):
    pass


def cardio_decomposition_files(DATE):
    "Разложение результатов обзвона 122 службы по папкам"

    PATH = Dir.get('CARDIO')
    P = DATE.split('-')
    DATE = f"{P[2]}-{P[1]}-{P[0]}"

    SQL = f"""
        SELECT * FROM oleg.patient
            where FeedBackDate = '{DATE}'
            and FeedBackId is not null
    """

    DF = dn122_sql(SQL)

    if len(DF) == 0:
        raise my_except('За данное число нечего разложить')

    DF['user'] = DF['file'].apply(lambda x: x.split('/', 1)[0])

    STAT = pd.DataFrame()

    for USER in DF['user'].unique():
        k = len(STAT)
        STAT.loc[k, 'user'] = USER

        FILE = PATH + f'/{USER}/{USER[11:]}_feedback_122_{DATE}.xlsx'

        PART = DF.loc[DF['user'] == USER]
        del PART['user']
        del PART['MO']
        del PART['Oid']
        del PART['DateCreate']

        try:
            PART.to_excel(FILE, index=False)
        except Exception as e:
            STAT.loc[k, 'status'] = f'Не смог положить файл {str(e)}'
        else:
            STAT.loc[k, 'status'] = 'Успешно положил файл'

    NAME = 'temp/decomposition_log.xlsx'
    STAT.to_excel(NAME)

    return NAME
