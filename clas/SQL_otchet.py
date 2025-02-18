from datetime import datetime, timedelta


class SQL_otchet:
    filename = str
    sql = str
    pokazatel = dict
    columns = dict
    cols_name = str
    rows = dict
    rows_name = str
    del_col = list
    pivot = dict

    def __init__(
        self,
        filename,
        sql,
        pokazatel={},
        columns={},
        cols_name="",
        rows={},
        rows_name="",
        del_col=[],
        pivot={},
    ):
        self.filename = filename
        self.sql = sql
        self.pokazatel = pokazatel
        self.columns = columns
        self.cols_name = cols_name
        self.rows = rows
        self.rows_name = rows_name
        self.del_col = del_col
        self.pivot = pivot

    def update_sql(self, poks=[]):
        if "__pokazatel__" in str(self.sql):
            self.sql = str(self.sql).replace(
                "__pokazatel__", "".join("'" + _ + "', " for _ in poks)
            )
            self.sql = str(self.sql).replace("', )", "')")

        if "__start__" and "__stop__" in str(self.sql):
            self.sql = str(self.sql).replace(
                "__start__", (datetime.today() - timedelta(days=60)).strftime("%Y%m%d")
            )
            self.sql = str(self.sql).replace(
                "__stop__", (datetime.today() + timedelta(days=30)).strftime("%Y%m%d")
            )

    def name(self):
        return str(self.filename)[:-5] + f"_{datetime.now().year}.xlsx"
