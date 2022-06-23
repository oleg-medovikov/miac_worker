import xlrd, glob, asyncio
import pandas as pd
from datetime import datetime, timedelta

from clas import Dir

NAMES = [
    'п/н','Дата создания РЗ','УНРЗ','Дата изменения РЗ',
    'СНИЛС','ФИО','Пол','Дата рождения',
    'Диагноз','Диагноз установлен',
    'Осложнение основного диагноза','Субъект РФ',
    'Медицинская организация','Ведомственная принадлежность',
    'Вид лечения','Дата госпитализации',
    'Дата исхода заболевания','Исход заболевания',
    'Степень тяжести','Посмертный диагноз','ИВЛ','ОРИТ',
    'МО прикрепления','Медицинский работник'
    ]

class my_except(Exception):
    pass

def slojit_fr():

    xlrd.xlsx.ensure_elementtree_imported(False, None)
    xlrd.xlsx.Element_has_iter = True

    PATH = Dir.get('robot') + '/_ФР_по_частям'
    DATE = datetime.now().strftime("%Y_%m_%d")
    nameSheetShablon = "Sheet1"
    
    FILES = glob.glob(PATH + '/Федеральный регистр лиц*.xlsx')

    if not len(FILES):
        raise my_except('В папке нет файлов!')

    LIST_ = []
    async def read_file(FILE):
        df = pd.read_excel(
                FILE,
                header= 1,
                usecols=NAMES,
                engine='xlrd',
                skipfooter=1 )
        LIST_.append(df)

    TASKS = []
    for FILE in FILES:
        task = read_file(FILE)
        TASKS.append(task)

    await asyncio.gather( TASKS )

    svod = pd.concat( LIST_ )

    svod["п/н"] = range(1, len(svod)+1)

    tomorrow = (datetime.now + timedelta(1)).strftime('%Y_%m_%d')
   
    NEW_FEDREG = Dir.get('robot') +'/'+ tomorrow \
            +'/Федеральный регистр лиц, больных - ' + DATE + '.csv'

    svod.to_csv(
            NEW_FEDREG,
            index=False,
            sep=";",
            encoding='cp1251')

