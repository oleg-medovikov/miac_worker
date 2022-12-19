from concurrent.futures import ThreadPoolExecutor
from clas import Task, Command

from loader import *
from parus import *
from zam_mz import *
from regiz import *
from cardio import *

from system import bot_send_text, bot_send_file

import sys
import os
import warnings
warnings.filterwarnings("ignore")


def executor(TASK: Task):
    COMMAND = Command.get(TASK.c_id)

    with ThreadPoolExecutor() as executor:
        if TASK.c_arg == 'no':
            future = executor.submit(globals()[COMMAND.c_procedure])
        else:
            future = executor.submit(
                    globals()[COMMAND.c_procedure],
                    TASK.c_arg)
        try:
            return_value = future.result()
        except Exception as e:
            # если функция сломалась
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ERROR = e, fname, exc_tb.tb_lineno

            TASK.comment = str(ERROR)
            TASK.stop()
            bot_send_text(str(e), TASK.client)
        else:
            # Если все хорошо, то получаем список, кому вернуть результат
            USERS = TASK.users()
            # Возвращаем результат

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
                    for MESS in return_value.split(';mess;'):
                        bot_send_text(MESS, USER)
