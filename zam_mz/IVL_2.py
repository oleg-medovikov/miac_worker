import glob
import pandas as pd
from datetime import datetime
import os

from clas import Dir
from .put_excel_for_mo import put_excel_for_mo
from base import covid_sql


class my_except(Exception):
    pass


# замена названий
def change_MO_dict() -> dict:
    "возвращаем словарь заменяемых названий"
    sql = "SELECT lower(Bad_Name) as Bad_Name, Good_Name FROM Nsi.MO_Name"
    CHANGE_MO = {}
    df = covid_sql(sql)

    for _ in df.index:
        CHANGE_MO[df.at[_, "Bad_Name"]] = df.at[_, "Good_Name"]
    return CHANGE_MO


def IVL():
    "это трехчасовое сравнение"
    DATE = datetime.now().strftime("%Y_%m_%d")
    PATH = Dir.get("path_robot")

    FILE_VP = PATH + "/" + DATE + "/Мониторинг_ВП.xlsx"
    if not os.path.exists(FILE_VP):
        raise my_except("Нет файла 'Мониторинг_ВП.xlsx'")

    MASK = PATH + "/" + DATE + "/Федеральный*15-00.csv"
    try:
        FILE_FR = glob.glob(MASK)[0]
    except IndexError:
        raise my_except("Не найден трёхчасовой федеральный регистр")

    NAMES = [
        "Дата изменения РЗ",
        "Медицинская организация",
        "Исход заболевания",
        "ИВЛ",
        "Вид лечения",
        "Субъект РФ",
        "Диагноз",
    ]

    FR = pd.read_csv(FILE_FR, usecols=NAMES, sep=";", engine="python", encoding="utf-8")

    DATE_OTCH = pd.to_datetime(FR["Дата изменения РЗ"], format="%d.%m.%Y").max().date()

    del FR["Дата изменения РЗ"]

    NAMES = ["mo", "vp_zan", "vp_ivl", "cov_zan", "cov_ivl"]

    vp = pd.read_excel(FILE_VP, usecols="A,I,L,Y,AB", header=7, names=NAMES).dropna()

    # Меняем названия организаций
    S_org = [
        "ФГБОУ ВО СЗГМУ им. И.И. Мечникова Минздрава России",
        "ФГБОУ ВО ПСПбГМУ им. И.П.Павлова Минздрава России",
        'СПб ГБУЗ "Городская больница №40"',
        'СПб ГБУЗ "Городская больница №20"',
        'СПб ГБУЗ "Николаевская больница"',
    ]

    CHANGE_MO = change_MO_dict()
    vp["mo"] = vp["mo"].str.lower().map(CHANGE_MO)
    FR["mo"] = FR["Медицинская организация"].str.lower().map(CHANGE_MO)
    S_org = [CHANGE_MO.get(_.lower()) for _ in S_org]

    # Считаем числа в в федеральном регистре
    zan1 = FR.loc[
        FR["Исход заболевания"].isnull()
        & FR["Вид лечения"].isin(["Стационарное лечение"])
        & FR["Субъект РФ"].isin(["г. Санкт-Петербург"])
        & FR["mo"].isin(S_org)
        & (
            FR["Диагноз"].str.contains("J12.")
            | FR["Диагноз"].str.contains("J18.")
            | FR["Диагноз"].isin(["U07.1", "U07.2"])
        )
    ]

    zan1["Занятые койки"] = 1
    zan1 = zan1.groupby("mo", as_index=False)["Занятые койки"].sum()

    zan2 = FR.loc[
        FR["Исход заболевания"].isnull()
        & FR["Субъект РФ"].isin(["г. Санкт-Петербург"])
        & ~FR["mo"].isin(S_org)
        & (
            FR["Диагноз"].str.contains("J12.")
            | FR["Диагноз"].str.contains("J18.")
            | FR["Диагноз"].isin(["U07.1", "U07.2"])
        )
    ]

    zan2["Занятые койки"] = 1
    zan2 = zan2.groupby("mo", as_index=False)["Занятые койки"].sum()

    zan = pd.concat([zan1, zan2], ignore_index=True)

    ivl1 = FR.loc[
        FR["Исход заболевания"].isnull()
        & FR["ИВЛ"].notnull()
        & FR["Вид лечения"].isin(["Стационарное лечение"])
        & FR["mo"].isin(S_org)
    ]

    ivl1["ИВЛ"] = 1
    ivl1 = ivl1.groupby("mo", as_index=False)["ИВЛ"].sum()

    ivl2 = FR.loc[
        FR["Исход заболевания"].isnull() & FR["ИВЛ"].notnull() & ~FR["mo"].isin(S_org)
    ]

    ivl2["ИВЛ"] = 1
    ivl2 = ivl2.groupby("mo", as_index=False)["ИВЛ"].sum()

    ivl = pd.concat([ivl1, ivl2], ignore_index=True)

    df = zan.merge(ivl, how="outer")
    df = df.fillna(0)

    vp = vp.fillna(0)
    # Меняем названия МО и сумируем строки
    vp["zan"] = vp["vp_zan"] + vp["cov_zan"]
    vp["ivl"] = vp["vp_ivl"] + vp["cov_ivl"]

    vp["mo"] = vp["mo"].apply(
        lambda x: CHANGE_MO.get(x) if CHANGE_MO.get(x) is not None else x
    )

    vp = vp.groupby("mo", as_index=False)["zan", "ivl"].sum()
    vp.index = range(len(vp))

    # получаем отчёт по ИВЛ
    ivl_otchet = vp.merge(df, on="mo", how="left")
    ivl_otchet["Медицинская организация"] = ivl_otchet["mo"]
    try:
        del ivl_otchet["mo"]
        del ivl_otchet["Занятые койки"]
        del ivl_otchet["zan"]
    except KeyError:
        pass
    ivl_otchet = ivl_otchet.fillna(0)

    ivl_otchet["Разница"] = ivl_otchet["ИВЛ"] - ivl_otchet["ivl"]

    ivl_otchet.rename(
        columns={"ivl": "ИВЛ из ежедневного отчёта", "ИВЛ": "ИВЛ из Фед Регистра"},
        inplace=True,
    )

    columnsTitles = [
        "Медицинская организация",
        "ИВЛ из ежедневного отчёта",
        "ИВЛ из Фед Регистра",
        "Разница",
    ]

    ivl_otchet = ivl_otchet.reindex(columns=columnsTitles)
    ivl_otchet = ivl_otchet[ivl_otchet["Медицинская организация"] != 0]

    ivl_otchet.index = range(1, len(ivl_otchet) + 1)

    # получаем отчёт по койкам
    zan_otchet = vp.merge(df, on="mo", how="left")

    zan_otchet["Медицинская организация"] = zan_otchet["mo"]
    try:
        del zan_otchet["mo"]
        del zan_otchet["ИВЛ"]
        del zan_otchet["ivl"]
    except KeyError:
        pass
    zan_otchet = zan_otchet.fillna(0)

    zan_otchet["Разница"] = zan_otchet["Занятые койки"] - zan_otchet["zan"]

    zan_otchet.rename(
        columns={
            "zan": "Заняты койки из ежедневного отчёта",
            "Занятые койки": "Койки из Фед Регистра",
        },
        inplace=True,
    )

    columnsTitles = [
        "Медицинская организация",
        "Заняты койки из ежедневного отчёта",
        "Койки из Фед Регистра",
        "Разница",
    ]

    zan_otchet = zan_otchet.reindex(columns=columnsTitles)
    zan_otchet = zan_otchet[zan_otchet["Медицинская организация"] != 0]
    zan_otchet.index = range(1, len(zan_otchet) + 1)

    FILE_OTCH = (
        Dir.get("zam_svod")
        + "/сверка ИВЛ и занятые койки"
        + "/"
        + str(datetime.now().strftime("%Y_%m_%d"))
        + " пациенты на ИВЛ новый.xlsx"
    )

    with pd.ExcelWriter(FILE_OTCH) as writer:
        ivl_otchet.to_excel(writer, sheet_name="ИВЛ")
        zan_otchet.to_excel(writer, sheet_name="занятые койки")

    STAT_1 = put_excel_for_mo(
        ivl_otchet, "Пациенты на ИВЛ", DATE_OTCH.strftime("%Y-%m-%d")
    )
    STAT_2 = put_excel_for_mo(
        zan_otchet, "Занятые койки", DATE_OTCH.strftime("%Y-%m-%d")
    )

    return STAT_1 + ";" + STAT_2
