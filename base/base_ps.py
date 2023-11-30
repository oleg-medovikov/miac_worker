import pandas as pd
import sqlalchemy

from conf import DATABASE_PS


def ps_sql(sql):
    "Делаем запросы в локальную базу"
    with sqlalchemy.create_engine(DATABASE_PS, pool_pre_ping=True).connect() as con:
        return pd.read_sql(sql, con)
