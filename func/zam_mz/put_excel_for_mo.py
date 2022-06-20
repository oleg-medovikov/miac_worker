import datetime, os
import pandas as pd
from clas import Dir


async def put_excel_for_mo(DF,NAME,DATE):
    "Раскладываем файлы по папкам организаций"
    
    if DATE is None:
        DATE = datetime.datetime.now().strftime('%Y-%m-%d')

    STAT = pd.DataFrame()
    
    ROOT = Dir.get('covid')
    
    for ORG in DF ['Медицинская организация'].unique():
        
        STAT.loc[ len(STAT),'Медицинская организация'] = ORG
        
        PART = DF.loc[DF['Медицинская организация'] == ORG ]
        PART.index = range(1, len( PART )+1)
        PART.fillna(0, inplace = True)
        PART = PART.applymap(str)
        
        USER = Dir.get( ORG )
        
        if USER:
            PATH = ROOT + USER
            try:
                os.makedirs( PATH )
            except OSError:
                pass

            FILE = PATH + '/' + DATE + ' ' + NAME + '.xlsx'
            
            with pd.ExcelWriter( FILE ) as writer:
                PART.to_excel(writer,sheet_name='унрз')
            
            STAT.loc[len(STAT) - 1, 'Статус']    = 'Файл положен'
            STAT.loc[len(STAT) -1 , 'Имя файла'] = FILE
        else:
            STAT.loc[len(STAT) - 1, 'Статус']   = 'Не найдена директория для файла'
    
    STAT.index = range(1, len(STAT) + 1)
    
    STAT_FILE = 'temp/отчёт по разложению ' + NAME + '.xlsx'

    with pd.ExcelWriter( STAT_FILE ) as writer:
        STAT.to_excel(writer,sheet_name='унрз') 

    return STAT_FILE
