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

REPLACE = {
    1027804200313: 'Санкт-Петербургское государственное бюджетное учреждение здравоохранения "Городская поликлиника №107"',
    1027802738237: 'Санкт-Петербургское государственное бюджетное учреждение здравоохранения "Городская поликлиника №88"',
    1037832003714: 'САНКТ-ПЕТЕРБУРГСКОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ УЧРЕЖДЕНИЕ ЗДРАВООХРАНЕНИЯ "ГОРОДСКАЯ ПОЛИКЛИНИКА № 114"',
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

    for key, value in REPLACE.items():
        DICT[key] = value

    return DICT
