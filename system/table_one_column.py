from pandas import DataFrame


def table_one_column(df: 'DataFrame') -> str:
    "Из колонки датафрейма создать сообщение"

    STRING = '\u2757\u2757\u2757'
    STRING += '<b>' + df.columns[0] + '</b> \n'
    STRING += '————————————\n'

    for i in df.index:
        STRING += '<b>' + df.iat[i, 0] + '</b>\n'

    return STRING
