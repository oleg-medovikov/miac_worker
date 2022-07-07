from base import covid_sql

def check_fr():
    SQL = "select * from robo.fr_status"
    
    DF = covid_sql(SQL)

    DF = DF.loc[DF['Регистр'] != 'ФР (полный с/без даты редактирования) загрузка' ]

    MESS = '```Состояние базы COVID на данный момент:'
    MESS += '\n' + '='*len(MESS)

    for ROW in DF.to_dict('records'):
        _ = len(DF['Регистр'].max()) - len(ROW['Регистр'])

        MESS += '\n' + ROW['Регистр'] +' '*_ + ' | ' + ROW['Выгрузка/Загрузка'] + ' | ' + str(ROW['Количество строчек'])

    MESS += '```'
    return MESS
