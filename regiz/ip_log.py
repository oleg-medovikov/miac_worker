from clas import Dir
from system import write_styling_excel_file

import pandas as pd
import glob


def ip_log():
    "собирает эксельки в кучу"

    PATH = Dir.get('ip_log') + '/*_log.xlsx'

    list_ = []
    for file in glob.glob(PATH):
        DATE = file.rsplit('/',1)[-1][:10]
        TABLE = pd.read_excel(file)
        TABLE['date'] = DATE
        list_.append(TABLE)


    DF = pd.concat(list_, ignore_index=True)

    FILE_NAME = '/tmp/ip_log_svod.xlsx'

    write_styling_excel_file(FILE_NAME, DF, 'ip_log')
    
    return FILE_NAME

