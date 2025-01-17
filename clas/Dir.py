from pandas.core.generic import JSONSerializable
from pydantic import BaseModel

from conf import MIAC_API_URL, TOKEN
import requests
from simplejson.errors import JSONDecodeError


class Dir(BaseModel):
    d_id: int
    d_name: str
    directory: str
    description: str
    working: bool

    @staticmethod
    def get(NAME) -> str:
        "Получить директорию по имени"
        HEADERS = dict(
            KEY=TOKEN,
        )
        URL = MIAC_API_URL + "/get_dir"

        req = requests.get(URL, headers=HEADERS, json=NAME)
        try:
            json = req.json()
        except JSONDecodeError:
            json = {}
        return json

    def add(self, USER_ID):
        "Добавляем новую директорию"
        HEADERS = dict(KEY=TOKEN, UID=str(USER_ID))
        URL = MIAC_API_URL + "/add_dir"
        BODY = self.__dict__

        requests.post(URL, headers=HEADERS, json=BODY)
