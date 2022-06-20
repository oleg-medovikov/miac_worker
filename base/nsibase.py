import pandas as pd
import sqlalchemy

from conf import DATABASE_NSI

def nsi_sql(sql):
    "Делаем запросы к базу NSI"
    with  sqlalchemy.create_engine(
            DATABASE_NSI,
            pool_pre_ping=True).connect() as con:
        return pd.read_sql(sql,con)



