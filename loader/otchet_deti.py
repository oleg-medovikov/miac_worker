import os

from clas import Dir
from system import send_mail_with_excel
from base import covid_sql


def send_otchet_deti():
    "отчёт по детям почтой в четверг"

    SQL = "exec [dbo].[Proc_Report_Children_with_Covid]"

    DF = covid_sql(SQL)

    filename = 'temp/Дети.xlsx'

    DF.to_excel(filename, index=False)

    send_mail_with_excel(
            Dir.get('svetlichnay_mail'),
            'Отчёт по детям',
            'Добрый день! Это отчёт от Олега',
            filename)

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    except FileExistsError:
        pass

    return 'Письмо отправлено!'
