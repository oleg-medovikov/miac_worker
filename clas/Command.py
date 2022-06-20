from datetime import date
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

from conf import MIAC_API_URL, TOKEN
import requests 

class Command(BaseModel):
    c_id : int
    c_category : str
    c_name : str
    c_procedure : str
    c_arg : str
    return_file : bool
    asc_day : bool

    def add(self, USER_ID):
        "добавление новой команды"
        HEADERS = dict(
                KEY=TOKEN,
                UID=str(USER_ID) )
        BODY = self.__dict__
        URL = MIAC_API_URL + '/add_command'
        req  = requests.post(URL,headers=HEADERS, json = BODY)
        
        return req.json()

    def get_all(USER_ID):
        "Получение всех комманд"
        HEADERS = dict(
                KEY=TOKEN,
                UID=str(USER_ID) )
        URL = MIAC_API_URL + '/all_commands'
        req  = requests.get(URL,headers=HEADERS)
        return req.json()

    def get( C_ID ):
        "Получение команды по айдишнику"
        HEADERS = dict(
                KEY=TOKEN,
                CID=str(C_ID) )

        URL = MIAC_API_URL + '/get_command'
        req  = requests.get(URL,headers=HEADERS)
        
        if not req.json() is None:
            return Command(**req.json())

