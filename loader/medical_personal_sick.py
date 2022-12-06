from datetime import datetime
from pandas import ExcelWriter

from base import covid_sql
from clas import Dir


def medical_personal_sick():
    DF = covid_sql('EXEC  med.p_StartMedicalPersonalSick')
    DATE = datetime.now().strftime("%Y_%m_%d_%H_%M")
    FILE = Dir.get('med_sick') + f'/Заболевшие медики {DATE}.xlsx'

    with ExcelWriter(FILE) as writer:
        DF.to_excel(writer, sheet_name='meducal', index=False)

    return f'Создан файл по заболевшим сотрудникам за {DATE}'
