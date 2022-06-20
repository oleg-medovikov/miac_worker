import datetime, glob, os

from clas import Dir

async def delete_zam_mz(DATE):
    DATE = datetime.datetime.strptime(DATE, '%d-%m-%Y').strftime('%Y-%m-%d')    
    MASK = await Dir.get('covid') + f"/EPID.COVID.*/EPID.COVID.*/Замечания Мин. Здравоохранения/{DATE}*.xlsx"
    
    FILES = glob.glob( MASK )

    if not len( FILES ):
        return "Нет файлов за это число"

    k = len ( FILES )
    for FILE in FILES:
        try:
            os.remove( FILE )
        except:
            k -= 1

    return f"Я удалил {k}  файлов из {len( FILES )}  на дату {DATE}"


