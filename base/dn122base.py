import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from conf import DATABASE_DN122


def dn122_sql(sql):
    "Делаем запросы к базу ковид"
    with sqlalchemy.create_engine(
            DATABASE_DN122,
            pool_pre_ping=True).connect() as con:
        return pd.read_sql(sql, con)


def dn122_exec(sql):
    with sqlalchemy.create_engine(
                DATABASE_DN122,
                pool_pre_ping=True).connect() as con:
        Session = sessionmaker(bind=con)
        session = Session()
        session.execute(sql)
        session.commit()
        session.close()


def dn122_insert(DF, TABLE, SCHEMA, INDEX, IF_EXISTS):
    "Загружаем данные в таблицу COVID"
    with sqlalchemy.create_engine(
                DATABASE_DN122,
                pool_pre_ping=True).connect() as con:
        DF.to_sql(
            TABLE,
            con,
            schema=SCHEMA,
            index=INDEX,
            if_exists=IF_EXISTS
                )
