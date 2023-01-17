from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os
import shutil
import glob

from clas import Dir


def sbor_death_week_files():
    """Собираем назад умерших за неделю,
    из папок организаций в одну папку"""

    DATE_END = (datetime.today() + relativedelta(weeks=-1, weekday=2)).date()
    DATE_START = DATE_END - timedelta(days=6)

    MASK = Dir.get('covid') \
        + '/EPID.COVID.*/EPID.COVID.*/Умершие за неделю/' \
        + '*{DATE_START} по {DATE_END}*.xlsx'

    NEW_DIR = Dir.get('death_week') + f'/с {DATE_START} по {DATE_END}'

    try:
        os.mkdir(NEW_DIR)
    except FileExistsError:
        pass

    for FILE in glob.iglob(MASK):
        # формируем имя нового файла из ftp юзера и имени файла
        _ = FILE.rsplit('/', 3)

        shutil.copyfile(FILE, NEW_DIR + f'/{_[1]} {_[3]}')

    return f'Файлы с {DATE_START} по {DATE_END} собраны в папку'
