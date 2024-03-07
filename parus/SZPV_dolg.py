from base import parus_sql
from .SZPV_MO_list import SZPV_MO_list

from system import write_styling_excel_file


def SZPV_dolg():
    SQL = open("parus/sql/SZPV_dolg.sql", "r").read()

    DF = parus_sql(SQL)

    # добавляем должников
    DELTA = set(SZPV_MO_list) - set(DF["ORGANIZATION"])
    for ORG in DELTA:
        DF = DF.append({"ORGANIZATION": ORG}, ignore_index=True)

    DF = DF.fillna("Нет отчета!")
    # записываем файл
    NEW_NAME = "temp/СЗПВ_должники.xlsx"
    write_styling_excel_file(NEW_NAME, DF, "СЗПВ_долг")

    return NEW_NAME
