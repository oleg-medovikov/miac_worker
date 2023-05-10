from pandas import DataFrame

from base import parus_sql
from .HCV_MO_list import HCV_MO_list


def HCV_dolg():
    SQL = open('parus/sql/HCV_dolg.sql', 'r').read()

    DF = parus_sql(SQL)

    DELTA = set(HCV_MO_list) - set(DF['ORGANIZATION'])
    DATE = DF.at[0, 'DAY']
    DF = DataFrame(
            data=DELTA,
            columns=['должники']
        )

    NEW_NAME = 'temp/' + DATE + '_ХВГС_должники.xlsx'
    DF.to_excel(NEW_NAME)

    return NEW_NAME
