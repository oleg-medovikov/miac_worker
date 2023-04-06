import requests


from conf import NSIUI_URL

atr = {
    "tag":           "dictionary_item",
    "id_dictionary": 64,
    "attributes":    ["display", "ogrn", "frmo_name"],
    "regime":        "data",
    "count":         1000,
    "page":          1,
    "filter":       [{"field": "moLevelId", "value": " LIKE &%I%&"}]
}


def dict_ogrn_frmoname() -> dict:
    "Возвращаем словарь названий мед организаций из ФРМО"

    data = {
        "data": str(atr).replace("'", '"').replace('&', "'"),
        "guid": ""
        }

    req = requests.post(NSIUI_URL,  json=data, verify=False)
    DICT = {}

    for id, name, ogrn, frmo in (req.json()['response']['data']):
        DICT[int(ogrn)] = frmo

    return DICT
