from clas import Dir
from system import send_mail_with_excel
from base import covid_sql

EMAILS = [
    "svetlichnay_mail",
    "darina_mail",
    "zahvatova_mail",
]


def otchet_po_ymershim(chat: str = "false"):
    "отчёт по умершим почтой в понедельник"

    SQL_1 = "select * from [dbo].[View_Count_Dead_In_MO]"
    SQL_2 = "SELECT * FROM [COVID].[dbo].[v_Count_dead_Covid_Pnev_ORVI_Gripp]"

    DF_1 = covid_sql(SQL_1)
    DF_2 = covid_sql(SQL_2)

    filename_1 = "/tmp/Умершие.xlsx"
    filename_2 = "/tmp/Умершие для РЗН.xlsx"

    DF_1.to_excel(filename_1, index=False)
    DF_2.to_excel(filename_2, index=False)

    if chat == "true":
        return filename_1 + ";" + filename_2

    for mail in EMAILS:
        send_mail_with_excel(
            Dir.get(mail),
            "Отчёт по умершим",
            "Добрый день! Это отчёт от Олега",
            filename_1,
        )

    for mail in EMAILS:
        send_mail_with_excel(
            Dir.get(mail),
            "Отчёт по умершим",
            'Добрый день! Это отчёт "умершие для РЗН" от Олега',
            filename_2,
        )

    return "Письмо с отчётом по умершим отправлено!"
