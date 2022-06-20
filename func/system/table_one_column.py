

def table_one_column(df):

    STRING = '\u2757\u2757\u2757'
    STRING +='<b>' + df.columns[0] + '</b> \n'
    STRING += '————————————\n'

    for i in df.index:
        STRING += '<b>' + df.iat[i,0] + '</b>\n'


    return STRING
