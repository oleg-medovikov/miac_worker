from clas import Task, Command

from loader import * 
from parus  import *
from zam_mz import *

from system import bot_send_text,bot_send_file

import os, warnings
warnings.filterwarnings("ignore")
from concurrent.futures import ThreadPoolExecutor


def executor(TASK : Task ):
    COMMAND = Command.get(TASK.c_id)
    
    with ThreadPoolExecutor() as executor:
        if TASK.c_arg == 'no':
            future = executor.submit(globals()[COMMAND.c_procedure])
        else:
            future = executor.submit(
                    globals()[COMMAND.c_procedure],
                    TASK.c_arg)
        try:
            return_value =  future.result()
        except Exception as e:
            # если функция сломалась
            TASK.comment = str(e)
            TASK.stop()
            bot_send_text( str(e), TASK.client )
        else:
            #Если все хорошо, то получаем список, кому вернуть результат
            USERS = TASK.users()
            #Возвращаем результат
                
            if COMMAND.return_file:
                TASK.stop()
                for FILE in return_value.split(';'):
                    for USER in USERS:
                        bot_send_file(FILE, USER)
                    os.remove(FILE)
            else:
                TASK.comment = return_value
                TASK.stop()
                for USER in USERS:
                    bot_send_text(return_value, USER)
