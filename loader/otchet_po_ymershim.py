import os

from clas import Dir
from system import send_mail_with_excel
from base import covid_sql


def otchet_po_ymershim():
    "отчёт по умершим почтой в понедельник"

    SQL_1 = "select * from [dbo].[View_Count_Dead_In_MO]"
    SQL_2 = "SELECT * FROM [COVID].[dbo].[v_Count_dead_Covid_Pnev_ORVI_Gripp]"

    DF_1 = covid_sql(SQL_1)
    DF_2 = covid_sql(SQL_2)

    filename_1 = 'temp/Умершие.xlsx'

    DF_1.to_excel(filename_1, index=False)

    send_mail_with_excel(
            Dir.get('svetlichnay_mail'),
            'Отчёт по умершим',
            'Добрый день! Это отчёт от Олега',
            filename_1)

    filename_2 = 'temp/Умершие для РЗН.xlsx'

    DF_2.to_excel(filename_2, index=False)

    send_mail_with_excel(
            Dir.get('svetlichnay_mail'),
            'Отчёт по умершим',
            'Добрый день! Это отчёт "умершие для РЗН" от Олега',
            filename_2)

    try:
        os.remove(filename_1)
        os.remove(filename_2)
    except FileNotFoundError:
        pass
    except FileExistsError:
        pass

    return 'Письмо с отчётом по умершим отправлено!'
