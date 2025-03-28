import requests
from requests.exceptions import ConnectionError
from time import sleep

from conf import TELEGRAM_API


def bot_send_text(mess: str, chat_id: int, html=False) -> bool:
    # Экранирование специальных символов для Markdown
    if not html:
        mess = mess.replace("_", "\\_").replace("@", "\\@").replace("&", "\\&")

    # Максимальная длина сообщения в Telegram
    MAX_MESSAGE_LENGTH = 4096

    # Разделяем сообщение на части, если оно слишком длинное
    message_parts = []
    if len(mess) > MAX_MESSAGE_LENGTH:
        # Разбиваем сообщение по переносам строк, если они есть
        if "\n" in mess:
            parts = mess.split("\n")
            current_part = ""
            for part in parts:
                if len(current_part) + len(part) + 1 > MAX_MESSAGE_LENGTH:
                    message_parts.append(current_part)
                    current_part = part
                else:
                    if current_part:
                        current_part += "\n" + part
                    else:
                        current_part = part
            if current_part:
                message_parts.append(current_part)
        else:
            # Просто разбиваем по максимальной длине
            for i in range(0, len(mess), MAX_MESSAGE_LENGTH):
                message_parts.append(mess[i : i + MAX_MESSAGE_LENGTH])
    else:
        message_parts.append(mess)

    send_text = f"https://api.telegram.org/bot{TELEGRAM_API}/sendMessage"
    parse_mode = "HTML" if html else "Markdown"

    for part in message_parts:
        data = {"chat_id": chat_id, "parse_mode": parse_mode, "text": part}

        while True:
            try:
                response = requests.post(send_text, data=data)
                # Проверяем статус ответа
                if response.status_code != 200:
                    raise ConnectionError(f"Telegram API error: {response.text}")
            except ConnectionError as e:
                print(f"Connection error: {e}. Retrying...")
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
