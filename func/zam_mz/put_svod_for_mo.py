import datetime, os
import pandas as pd

from clas import Dir

async def put_svod_for_mo(DF,NAME, DATE):
    if DATE is None:
        DATE = datetime.datetime.now().strftime( '%Y-%m-%d' )

    PATH = Dir.get( 'zam_svod' ) + '/' + NAME
    NAME = DATE + ' ' + NAME + '.xlsx'

    try:
        os.mkdir( PATH ) 
    except OSError:
        pass

    DF.index = range( 1, len(DF) + 1 )

    DF = DF.applymap( str )

    DF.fillna('пусто', inplace = True)

    with pd.ExcelWriter( PATH + '/' + NAME ) as writer:
        DF.to_excel(writer)

    return 1



