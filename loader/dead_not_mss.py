from base import covid_sql
from datetime import datetime
from system import write_styling_excel_file
from clas import Dir


def dead_not_mss():
    "умершие без свидетельства о смерти"
    SQL = "EXEC dbo.p_FedRegNotMss"
    DF = covid_sql(SQL)
    date = datetime.today().strftime("%Y_%m_%d_%H_%M")
    file = Dir.get('fr_not_mss') + f'/Список_без_МСС_{date}.xlsx'

    write_styling_excel_file(file, DF, 'notMSS')

    return "Список готов\n" + file.split('/')[- 1]
