import requests
import pandas as pd
import os
from glob import glob
from datetime import datetime


def get_nsi_dictinary(id: str):
    URL = "http://10.128.66.207:2226/nsiui/Api/Grid"
    if id == "1.2.643.2.69.1.1.1.31":
        data = {
            "data": '{"tag":"dictionary_item","id_dictionary":27,"attributes":["code","display"],"regime":"data","count":20000,"page":1,"filter":[]}',
            "guid": "",
        }
    elif id == "1.2.643.5.1.13.13.11.1081":
        data = {
            "data": '{"tag":"dictionary_item","id_dictionary":81,"attributes":["code","display"],"regime":"data","count":20000,"page":1,"filter":[]}',
            "guid": "",
        }
    elif id == "1.2.643.5.1.13.13.11.1477":
        data = {
            "data": '{"tag":"dictionary_item","id_dictionary":759,"attributes":["code","display"],"regime":"data","count":20000,"page":1,"filter":[]}',
            "guid": "",
        }
    else:
        return {}

    req = requests.post(URL, json=data)
    dict_ = {}
    for _, code, display in req.json()["response"]["data"]:
        dict_[code] = display
    return dict_


def analis_file(file: str, dict_31, dict_1081, dict_1477):
    def check_value(value, valid_values):
        if value in valid_values:
            return True
        else:
            return False

    df = pd.read_excel(file, dtype=str)
    # удаляем всякие пробелы
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df["Код ЛИ проверка"] = df["Код ЛИ"].apply(check_value, args=(dict_31.keys(),))
    df["Код ЛИ наименование по справочнику"] = df["Код ЛИ"].map(dict_31)
    df["Полное наименование ЛИ проверка"] = df["Полное наименование ЛИ"].apply(
        check_value, args=(dict_31.values(),)
    )
    for index, row in df.iterrows():
        key = row["Код ЛИ"]
        value = row["Полное наименование ЛИ"]
        if value == dict_31.get(key):
            df.loc[index, "Код ЛИ соответсвие полному наименованию ЛИ"] = True
        else:
            df.loc[index, "Код ЛИ соответсвие полному наименованию ЛИ"] = False

    df["Код БМ для ГС проверка"] = df["Код БМ для ГС "].apply(
        check_value, args=(dict_1081.keys(),)
    )
    df["Код БМ для ГС наименование по справочнику"] = df["Код БМ для ГС "].map(
        dict_1081
    )
    df["Наименование БМ для ГС  проверка"] = df["Наименование БМ для ГС "].apply(
        check_value, args=(dict_1081.values(),)
    )
    for index, row in df.iterrows():
        key = row["Код БМ для ГС "]
        value = row["Наименование БМ для ГС "]
        if value == dict_1081.get(key):
            df.loc[index, "Код БМ для ГС соответсвие полному наименованию БМ"] = True
        else:
            df.loc[index, "Код БМ для ГС соответсвие полному наименованию БМ"] = False

    grouped = (
        df.groupby("Код ГС")["Наименование ГС"]
        .apply(lambda x: ", ".join(map(str, x.unique())))
        .reset_index()
    )
    grouped.columns = [
        "Код ГС",
        "Количество уникальных наименований ГС (больше одного - ошибка)",
    ]
    df = df.merge(grouped, on="Код ГС", how="left")

    grouped = (
        df.groupby("Код ГС")["Код БМ для ГС "]
        .apply(lambda x: ", ".join(map(str, x.unique())))
        .reset_index()
    )
    grouped.columns = [
        "Код ГС",
        "Количество уникальных кодов БМ для ГС (больше одного - ошибка)",
    ]
    df = df.merge(grouped, on="Код ГС", how="left")

    df["Код локуса для ГС проверка"] = df["Код локуса для ГС "].apply(
        check_value, args=(dict_1477.keys(),)
    )
    df["Наименование локуса для ГС по справочнику"] = df["Код локуса для ГС "].map(
        dict_1477
    )
    df["Наименование локуса для ГС  проверка"] = df["Наименование локуса для ГС"].apply(
        check_value, args=(dict_1477.values(),)
    )
    for index, row in df.iterrows():
        key = row["Код локуса для ГС "]
        value = row["Наименование локуса для ГС"]
        if value == dict_1477.get(key):
            df.loc[index, "Код локуса для ГС соответсвие наименованию ГС"] = True
        else:
            df.loc[index, "Код локуса для ГС соответсвие наименованию ГС"] = False

    df.to_excel(
        file.rsplit("/", 1)[0] + "/проверено/" + file.rsplit("/", 1)[1], index=False
    )


def lab_check_dict():
    """Это для лаборатории сверка их файлов со справочниками"""
    dict_31 = get_nsi_dictinary("1.2.643.2.69.1.1.1.31")
    dict_1081 = get_nsi_dictinary("1.2.643.5.1.13.13.11.1081")
    dict_1477 = get_nsi_dictinary("1.2.643.5.1.13.13.11.1477")

    dateStr = datetime.now().strftime("%d.%m.%Y")
    path = f"/mnt/lab/2025 год/КИС ЕМИАС/ПРОФИЛЬ лабораторий/Ответы МО/{dateStr}"  # /[!~]*.xlsx"
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path + "/проверено"):
        os.makedirs(path + "/проверено")

    MESS = f"Рабочая дириктория: \n{path}\n"
    for file in glob(path + "/[!~]*.xlsx"):
        MESS += f"\nНачинаю работу над файлом {file.rsplit('/', 1)[1]}"
        try:
            analis_file(file, dict_31, dict_1081, dict_1477)
        except KeyError as e:
            MESS += f"\nОшибка в шапке  {str(e)}"
        except OSError:
            MESS += "\nНе смог сохранить файл, так как он занят"
        else:
            MESS += "\nГотово"

    return MESS
