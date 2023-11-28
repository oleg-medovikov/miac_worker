from pandas import DataFrame

from clas import SQL_otchet
from base import parus_sql


def df_processing(otchet: "SQL_otchet") -> "DataFrame":
    otchet.update_sql()
    df = parus_sql(otchet.sql)

    if isinstance(otchet.columns, dict) and len(otchet.columns):
        for key, value in otchet.columns.items():
            df.loc[df.POKAZATEL.str.endswith(value), otchet.cols_name] = key

    if isinstance(otchet.rows, dict) and len(otchet.rows):
        for key, value in otchet.rows.items():
            df.loc[df.POKAZATEL.str.endswith(value), otchet.rows_name] = key

    if isinstance(otchet.pokazatel, dict) and len(otchet.pokazatel):
        df.POKAZATEL = df.POKAZATEL.map(otchet.pokazatel)

    if isinstance(otchet.pivot, dict):
        df = df.pivot_table(**otchet.pivot).stack(0)
        df = df.reset_index()
        if otchet.cols_name != "":
            df.rename(
                columns={
                    "level_2": otchet.cols_name,
                },
                inplace=True,
            )
    if isinstance(otchet.del_col, list):
        for col in otchet.del_col:
            try:
                del df[col]
            except KeyError:
                continue
    return df
