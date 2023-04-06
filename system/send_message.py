import requests
from requests.exceptions import ConnectionError
from time import sleep

from conf import TELEGRAM_API


def bot_send_text(mess: str, chat_id: int) -> bool:
    mess = mess.replace('_', '\\_').replace('@', '\\@').replace('&', '\\&')

    send_text = f'https://api.telegram.org/bot{TELEGRAM_API}/sendMessage'
    data = {
        'chat_id':    chat_id,
        'parse_mode': 'Markdown',
        'text':        mess
        }
    while True:
        try:
            requests.get(send_text, data=data)
        except ConnectionError:
            sleep(5)
            continue
        else:
            break

    return True


def bot_send_file(file: str, chat_id: int) -> None:

    with open(file, 'rb') as f:
        files = {'document': f}
#        title = file.rsplit('/', 1)[-1]
        url = f'https://api.telegram.org/bot{TELEGRAM_API}/sendDocument'
        while True:
            try:
                requests.post(url, data={"chat_id": chat_id}, files=files)
            except ConnectionError:
                sleep(5)
                continue
            else:
                break
