import cx_Oracle
import pandas as pd

from conf import DATABASE_PARUS

def parus_sql(SQL):
    "Делаем запросы к базе паруса"
    try:
        with cx_Oracle.connect(DATABASE_PARUS, encoding='UTF-8') as CON:
            df = pd.read_sql(SQL,CON)
    except Exception as e:
        raise str(e)
    return df
