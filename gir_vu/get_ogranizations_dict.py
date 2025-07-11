import requests
import json
import urllib3

from conf import NSIUI_URL

# Отключаем предупреждения о SSL (если нужно)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_organizations_dict():
    headers = {"Content-Type": "application/json"}

    payload = {
        "data": json.dumps(
            {
                "tag": "dictionary_item",
                "id_dictionary": 64,
                "attributes": ["code", "display", "oid"],
                "regime": "data",
                "count": 4000,
                "page": 1,
                "sort_field": "7cc9c3ac-bd69-47d0-8c8e-872a951d9c8f",
                "sort_direct": "asc",
                "filter": [{"field": "oid", "value": " != ''"}],
            }
        ),
        "guid": "",
    }

    try:
        response = requests.post(NSIUI_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()  # Проверка на ошибки HTTP

        data = response.json()

        # Создаем словарь {code: oid}
        org_dict = {
            str(item[1]): str(item[3])
            for item in data.get("response", {}).get("data", [])
            if len(item) >= 4 and item[1] is not None and item[3] is not None
        }

        # print(f"Справочник успешно загружен. Организаций: {len(org_dict)}")
        return org_dict

    except Exception as e:
        print(f"Ошибка при получении справочника организаций: {str(e)}")
        return {}
