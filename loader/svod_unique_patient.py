from datetime import datetime, timedelta
import pandas as pd

from clas import Dir


class my_except(Exception):
    pass


# NAMES_RPN = ['фио', 'м/ж','Дата рождения', 'ЭПИДНОМЕР']


def svod_unique_patient(DATE_GLOBAL):
    DATE_SVOD = (
        datetime.strptime(DATE_GLOBAL, "%d-%m-%Y") - timedelta(days=1)
    ).strftime("%Y-%m-%d")
    DATE_GLOBAL = datetime.strptime(DATE_GLOBAL, "%d-%m-%Y").strftime("%d.%m.%Y")

    SVOD = pd.read_csv(
        Dir.get("covi_list") + "/Автосвод " + DATE_SVOD + ".csv",
        na_filter=False,
        dtype=str,
        delimiter=";",
        engine="python",
        encoding="utf-8",
    )

    FILE_RPN = (
        Dir.get("COVID_RPN") + "/Заболевшие COVID в ФС на " + DATE_GLOBAL + ".xlsx"
    )
    try:
        df = pd.read_excel(FILE_RPN, dtype=str)
    except:
        try:
            df = pd.read_excel(FILE_RPN[:-1], dtype=str)
        except:
            raise my_except("Не найден файлик РПН")

    RPN = pd.DataFrame()
    RPN["Unnamed: 0"] = df.index + 1
    RPN["фио"] = df["фио"]
    RPN["Дата рождения "] = df["Дата рождения "]
    RPN["м/ж"] = df["м/ж"]
    RPN["Учреждение зарегистрировавшее диагноз"] = df[
        "Учреждение зарегистрировавшее диагноз"
    ]

    # Подготавливаем ФИО и ДР для сравнения
    # Используем отдельные датафреймы

    svod_1 = SVOD.copy()
    svod_1["Фио"] = svod_1["Фио"].str.lower().str.replace(" ", "")
    svod_1["дата рождения"] = pd.to_datetime(svod_1["дата рождения"], errors="coerce")
    svod_1 = svod_1[svod_1["дата рождения"].notnull()]
    svod_1.index = range(len(svod_1))

    rpn_1 = RPN.copy()
    rpn_1["фио"] = rpn_1["фио"].str.lower().str.replace(" ", "")
    rpn_1["Дата рождения "] = pd.to_datetime(rpn_1["Дата рождения "], errors="coerce")
    rpn_1 = rpn_1[rpn_1["Дата рождения "].notnull()]
    rpn_1.index = rpn_1["Unnamed: 0"]

    # Находим пересечение

    join = svod_1.merge(
        rpn_1,
        how="outer",
        left_on=["Фио", "дата рождения"],
        right_on=["фио", "Дата рождения "],
    )

    # Находим дубли и у них добавляем значение в поле 'Дата занесения в базу'
    DUBLI = join.loc[(join["Фио"].notnull()) & (join["фио"].notnull())].index
    SVOD.loc[DUBLI, "Дата занесения в базу"] = (
        SVOD.loc[DUBLI, "Дата занесения в базу"] + " , " + DATE_GLOBAL
    )

    # Находим новые уникальные строчки
    NEW_ROW = join.loc[
        (join["Фио"].isnull()) & ~(join["фио"].isnull()), "Unnamed: 0"
    ].unique()
    RPN = RPN.loc[RPN["Unnamed: 0"].isin(NEW_ROW)][
        ["фио", "Дата рождения ", "м/ж", "Учреждение зарегистрировавшее диагноз"]
    ]
    RPN.columns = ["Фио", "дата рождения", "адрес", "Направил материал"]
    RPN["Дата занесения в базу"] = DATE_GLOBAL
    RPN["Роспотребнадзор"] = "Роспотребнадзор"
    RPN.index = range(len(RPN))
    # Добавляем их к основному файлу
    SVOD = SVOD.append(RPN, ignore_index=True)

    SVOD.index = range(len(SVOD))

    # Записываем файл
    FILE = (
        Dir.get("covi_list")
        + "/Автосвод "
        + datetime.strptime(DATE_GLOBAL, "%d.%m.%Y").strftime("%Y-%m-%d")
        + ".csv"
    )

    SVOD.to_csv(FILE, index=False, sep=";", encoding="utf-8", errors="replace")

    # Выводим ответ
    mess = (
        "Свод уникальных пациентов за дату "
        + DATE_GLOBAL
        + " сделан!"
        + "\nНайдено дублей: "
        + str(len(DUBLI))
        + "\nНовых пациентов: "
        + str(len(RPN))
        + "\nВсего уникальных пациентов: "
        + str(len(SVOD))
    )

    return mess
