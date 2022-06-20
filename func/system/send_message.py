import requests
from conf import TELEGRAM_API 

def bot_send_text(mess, chat_id):

    send_text = 'https://api.telegram.org/bot' + TELEGRAM_API \
            + '/sendMessage?chat_id=' + chat_id \
            + '&parse_mode=Markdown&text=' + mess
    requests.get(send_text)

    return 1

def bot_send_file(file,chat_id):

    with open(file, 'rb') as f:
        files = {'document' : f}
        title = file.rsplit('/',1)[-1]
        url = 'https://api.telegram.org/bot'+ TELEGRAM_API \
                +'/sendDocument'
        requests.post(url, data={"chat_id":chat_id}, files=files)

