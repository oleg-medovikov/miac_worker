import pandas as pd
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from conf import DATABASE_COVID


def covid_sql(sql):
    "Делаем запросы к базу ковид"
    with sqlalchemy.create_engine(
        DATABASE_COVID,
        pool_pre_ping=True,
        pool_size=5,  # Размер пула
        max_overflow=10,  # Максимальное количество дополнительных соединений
        pool_timeout=30,  # Таймаут получения соединения из пула
        pool_recycle=3600,  # Время жизни соединения (в секундах)
    ).connect() as con:
        return pd.read_sql(sql, con)


def covid_exec(sql):
    with sqlalchemy.create_engine(DATABASE_COVID, pool_pre_ping=True).connect() as con:
        Session = sessionmaker(bind=con)
        session = Session()
        session.execute(sql)
        session.commit()
        session.close()


def covid_insert(DF, TABLE, SCHEMA, INDEX, IF_EXISTS):
    "Загружаем данные в таблицу COVID"
    with sqlalchemy.create_engine(
        DATABASE_COVID,
        pool_pre_ping=True,
        pool_size=5,  # Размер пула
        max_overflow=10,  # Максимальное количество дополнительных соединений
        pool_timeout=30,  # Таймаут получения соединения из пула
        pool_recycle=3600,  # Время жизни соединения (в секундах)
    ).connect() as con:
        DF.to_sql(TABLE, con, schema=SCHEMA, index=INDEX, if_exists=IF_EXISTS)
