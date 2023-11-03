import pandas as pd
import os
from datetime import datetime, timedelta

from clas import Dir

NAMES = [
    "п/н",
    "Дата создания РЗ",
    "УНРЗ",
    "Дата изменения РЗ",
    "СНИЛС",
    "ФИО",
    "Пол",
    "Дата рождения",
    "Диагноз",
    "Диагноз установлен",
    "Осложнение основного диагноза",
    "Субъект РФ",
    "Медицинская организация",
    "Ведомственная принадлежность",
    "Вид лечения",
    "Дата госпитализации",
    "Дата исхода заболевания",
    "Исход заболевания",
    "Степень тяжести",
    "Посмертный диагноз",
    "ИВЛ",
    "ОРИТ",
    "МО прикрепления",
    "Медицинский работник",
]


class my_except(Exception):
    pass


def copy_uach():
    if datetime.now().hour < 15:
        DATE = (datetime.today() - timedelta(days=1)).strftime("%Y_%m_%d")
        TOMORROW = datetime.today().strftime("%Y_%m_%d")
    else:
        DATE = datetime.today().strftime("%Y_%m_%d")
        TOMORROW = (datetime.today() + timedelta(days=1)).strftime("%Y_%m_%d")

    FEDREG_FILE = (
        Dir.get("path_robot")
        + "/"
        + TOMORROW
        + "/Федеральный регистр лиц, больных - "
        + DATE
        + ".csv"
    )

    IACH_FILE = (
        Dir.get("covid_iac2")
        + "/Федеральный регистр лиц, больных - "
        + DATE
        + "_ИАЦ.csv"
    )

    if not os.path.exists(FEDREG_FILE):
        raise my_except("Файл фр не найден!")

    DF = pd.read_csv(
        FEDREG_FILE,
        usecols=NAMES,
        na_filter=False,
        dtype=str,
        delimiter=";",
        engine="python",
        encoding="utf-8",
    )

    del DF["СНИЛС"]
    del DF["ФИО"]

    try:
        DF.to_csv(IACH_FILE, index=False, sep=";", encoding="cp1251")
    except Exception as e:
        return f"Ошибка!  {IACH_FILE} Не удалось скопировать!\n {str(e)}"

    return "Файл скопирован!"
