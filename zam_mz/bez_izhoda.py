from base import covid_sql
from .put_svod_for_mo import put_svod_for_mo
from .put_excel_for_mo import put_excel_for_mo


def bez_izhoda():
    SQL = open("zam_mz/sql/bez_ishod.sql", "r").read()

    DF = covid_sql(SQL)

    STAT_FILE = put_excel_for_mo(DF, "Без исхода 25 дней", None)
    put_svod_for_mo(DF, "Без исхода 25 дней", None)

    return STAT_FILE
