import pandas as pd
import sqlalchemy

from conf import DATABASE_MIAC_DS

def miac_ds_sql(sql):
    "Делаем запросы к базу ковид"
    with  sqlalchemy.create_engine(
            DATABASE_MIAC_DS,
            pool_pre_ping=True).connect() as con:
        return pd.read_sql(sql,con)



def miac_ds_exec(sql):
    with  sqlalchemy.create_engine(
                DATABASE_MIAC_DS,
                pool_pre_ping=True).connect() as con:
            Session = sessionmaker(bind=con)
            session = Session()
            session.execute(sql)
            session.commit()
            session.close()

def miac_ds_insert(DF, TABLE, SCHEMA, INDEX, IF_EXISTS):
    "Загружаем данные в таблицу COVID"
    with  sqlalchemy.create_engine(
                DATABASE_MIAC_DS,
                pool_pre_ping=True).connect() as con:
            DF.to_sql (
                TABLE,
                con,
                schema = SCHEMA,
                index = INDEX,
                if_exists = IF_EXISTS
                    )


