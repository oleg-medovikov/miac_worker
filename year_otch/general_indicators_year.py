from base import parus_sql

from year_otch.dop.info_NRD import info_NRD


def general_indicators_year():
    """"""
    files = []

    # ИнфконтрольНРД

    info_NRD.update_sql()
    df = parus_sql(info_NRD.sql)
    df.POKAZATEL = df.POKAZATEL.map(info_NRD.pokazatel)

    df = df.pivot_table(
        index=["ORGANIZATION"], columns=["POKAZATEL"], values=["VALUE"], aggfunc="first"
    ).stack(0)
    df = df.reset_index()
    del df["level_1"]
    df.to_excel(info_NRD.filename, index=False)
    files.append(info_NRD.filename)

    return "".join(_ + ";" for _ in files)
