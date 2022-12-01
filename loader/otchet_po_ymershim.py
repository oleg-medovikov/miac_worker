import os

from clas import Dir
from system import send_mail_with_excel
from base import covid_sql


def otchet_po_ymershim():
    "отчёт по умершим почтой в понедельник"

    SQL = "select * from [dbo].[View_Count_Dead_In_MO]"

    DF = covid_sql(SQL)

    filename = 'temp/Умершие.xlsx'

    DF.to_excel(filename, index=False)

    send_mail_with_excel(
            Dir.get('svetlichnay_mail'),
            'Отчёт по умершим',
            'Добрый день! Это отчёт от Олега',
            filename)

    try:
        os.remove(filename)
    except FileNotFoundError:
        pass
    except FileExistsError:
        pass

    return 'Письмо с отчётом по умершим отправлено!'
