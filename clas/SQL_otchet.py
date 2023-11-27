from datetime import datetime, timedelta


class SQL_otchet:
    sql = str
    pokazatel = dict
    filename = str

    def __init__(self, sql, pokazatel, filename):
        self.sql = sql
        self.pokazatel = pokazatel
        self.filename = filename

    def update_sql(self):
        if "__start__" and "__stop__" in self.sql:
            START = (datetime.today() - timedelta(days=90)).strftime("%Y%m%d")
            STOP = (datetime.today() + timedelta(days=90)).strftime("%Y%m%d")
            self.sql = self.sql.replace("__start__", START)
            self.sql = self.sql.replace("__stop__", STOP)
