import requests
from requests.exceptions import ConnectionError
from time import sleep

from conf import TELEGRAM_API


def bot_send_text(mess: str, chat_id: int, html=False) -> bool:
    mess = mess.replace("_", "\\_").replace("@", "\\@").replace("&", "\\&")

    send_text = f"https://api.telegram.org/bot{TELEGRAM_API}/sendMessage"
    data = {"chat_id": chat_id, "parse_mode": "Markdown", "text": mess}
    if html:
        data["parse_mode"] = "HTML"
    while True:
        try:
            requests.get(send_text, data=data)
        except ConnectionError:
            sleep(1)
            continue
        else:
            break

    return True


def bot_send_file(file: str, chat_id: int) -> None:
    if file == "":
        return

    with open(file, "rb") as f:
        files = {"document": f}
        url = f"https://api.telegram.org/bot{TELEGRAM_API}/sendDocument"
        while True:
            try:
                requests.post(url, data={"chat_id": chat_id}, files=files)
            except ConnectionError:
                sleep(1)
                continue
            else:
                break
