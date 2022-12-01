from datetime import datetime
import glob

from clas import Dir


def check_robot():
    DATE = datetime.today().strftime("%Y_%m_%d")
    PATH = Dir.get('path_robot') + '/' + DATE + '/*'
    SPISOK = 'В директории Robot сейчас лежат файлы:'
    for file in glob.glob(PATH):
        SPISOK += '\n' + file.rsplit('/', 1)[-1]

    return SPISOK
