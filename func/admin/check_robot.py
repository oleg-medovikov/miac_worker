import datetime, glob

from clas import Dir


def check_robot():
    date = datetime.datetime.today().strftime("%Y_%m_%d")
    path = Dir.get('path_robot') +'/'+ date + '/*'
    spisok = 'В директории Robot сейчас лежат файлы:'
    for file in glob.glob(path):
        spisok += '\n' + file.rsplit('/',1)[-1]

    return spisok
