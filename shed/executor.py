from clas import Task, Command
from func import bot_send_text, bot_send_file

import os, warnings
warnings.filterwarnings("ignore")

def executor(TASK : Task ):
    COMMAND = Command.get(TASK.c_id)

    try:
        return_value =  TASK.start()
    except Exception as e:
        # если функция сломалась
        TASK.comment = str(e)
        TASK.stop()
        bot_send_text( str(e), TASK.client )
    else:
        #Если все хорошо, то получаем список, кому вернуть результат
        USERS = TASK.users()
        TASK.stop()
        #Возвращаем результат
            
        if COMMAND.return_file:
            for FILE in return_value.split(';'):
                for USER in USERS:
                    bot_send_file(FILE, USER)
                os.remove(FILE)
        else:
            for USER in USERS:
                bot_send_text(return_value, USER)

