from clas import Task, Dir
from shed import executor

import time
from threading import Thread

def create_threads():
    while True:
        t =  Task.get()
        if t is None:
            time.sleep(2)
            continue

        
        t = Thread(
                name = str(t.t_id),
                target = executor,
                args=(t,),
                daemon=None)
        t.start()
        time.sleep(1)


if __name__ == '__main__':
    Task.restart()
    try:
        create_threads()
    except KeyboardInterrupt:
        pass
