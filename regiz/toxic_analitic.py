from datetime import datetime

from system import return_mounth, write_styling_excel_file
from .toxic_get_cases import toxic_get_cases
from .toxic_checker import toxic_checker
from .toxic_columns import toxic_columns


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

    # делаем проверку на ошибки
    error = toxic_checker(DF)
    if len(error):
        DF = DF.loc[~DF['history_number'].isin(error['history_number'])]
        error = toxic_columns(error)
        error = error.fillna('ПУСТО!!!')

    DF = toxic_columns(DF)
    DF = DF.fillna('ПУСТО!!!')

    write_styling_excel_file(FILENAME, DF, ARG.split(';')[1])
    if len(error):
        write_styling_excel_file(FILERROR, error, 'errors')
        return FILENAME + ';' + FILERROR

    return FILENAME
