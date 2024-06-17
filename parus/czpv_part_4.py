from datetime import datetime, timedelta
from base import parus_sql


def czpv_part_4():
    SQL = open("parus/sql/szpv_part_4.sql", "r").read()

    DF = parus_sql(SQL)
    DF = DF.pivot_table(index=["ORGANIZATION"], columns=["POKAZATEL"], values=["VALUE"])
    DATE = (datetime.now() - timedelta(days=1)).strftime("%d_%m_%Y")

    NEW_NAME = "/tmp/" + DATE + "_СЗПВ_часть_4.xlsx"
    DF.to_excel(NEW_NAME)

    return NEW_NAME
