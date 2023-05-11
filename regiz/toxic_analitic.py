from datetime import datetime

from system import return_mounth, write_styling_excel_file
from .toxic_get_cases import toxic_get_cases
from .toxic_checker import toxic_checker
from .toxic_columns import toxic_columns
from .toxic_no_obs import toxic_no_obs


class my_except(Exception):
    pass


def toxic_analitic(ARG):
    "сгенерировать за месяц"
    DATE = datetime.strptime(ARG.split(';')[0], '%d-%m-%Y')
    START, END = return_mounth(DATE)
    DF = toxic_get_cases(START, END)
    DF = DF.loc[DF['medical_help_name'] == ARG.split(';')[1]]

    FILENAME = f'temp/Аналитика по полноте регистра с {START} по {END}.xlsx'
    FILERROR = f'temp/Ошибки заполнения {START} по {END}.xlsx'
    FILENOBS = f'temp/Нет показателей {START} по {END}.xlsx'

    # делаем проверку на ошибки
    error = toxic_checker(DF)

    if len(error):
        DF = DF.loc[~DF['history_number'].isin(error['history_number'])]
        error = toxic_columns(error)
        error = error.fillna('ПУСТО!!!')

    # проверяем на пац без показателей
    no_obs = toxic_no_obs(START, END, ARG.split(';')[1])

    DF = toxic_columns(DF)
    DF = DF.fillna('ПУСТО!!!')

    write_styling_excel_file(FILENAME, DF, ARG.split(';')[1])
    RETURN = FILENAME

    if len(error):
        write_styling_excel_file(FILERROR, error, 'errors')
        RETURN += ';' + FILERROR

    if len(no_obs):
        write_styling_excel_file(FILENOBS, no_obs, 'errors')
        RETURN += ';' + FILENOBS

    return RETURN
