import glob
import pandas as pd
from base import covid_exec, covid_insert
from clas import Dir

UPDATE = """
update  a
        set a.[Примечания] = b.[Примечания]
        from [robo].[snils_comment] a inner join [tmp].[snils_comment] b
        on a.[УНРЗ] = b.[УНРЗ]
insert [robo].[snils_comment]
        ([УНРЗ]
      ,[Примечания])
     SELECT b.[УНРЗ]
            ,b.[Примечания]
    FROM [tmp].[snils_comment] b
    left join [robo].[snils_comment] a
    on a.[УНРЗ] = b.[УНРЗ]
    where a.[УНРЗ] is null
"""

async def load_snils_comment():
    MASK = Dir.get('snils_com') + '/*'
    
    text = ''
    for FILE in glob.glob( MASK ):
        try:
            DF = pd.read_excel(file,usecols=['УНРЗ','Примечания'])
        except Exception as e:
            text +=  FILE.rsplit('/',1)[1] +'\n' + str(e) 
        else:
            try:
                covid_exec("""TRUNCATE TABLE tmp.snils_comment""")
            except:
                pass
            
            covid_insert(DF,'snils_comment','tmp',False,'append')
            
            covid_exec( UPDATE )

            text += '\n Хорошо обработан файл ' + file.split('/')[-1]
    return text


