from base import covid_sql


def svod_all_sick():
    # SQL = "SELECT * FROM [robo].[values]"

    SQL_1 = """
    select [Диагноз установлен], count(*) as all
    from robo.v_FedReg
    where [Диагноз] = 'u07.1'
    group by [Диагноз установлен]
    order by [Диагноз установлен]
    """
    SQL_2 = """
    select [Дата исхода заболевания], count(*) as rec
    from robo.v_FedReg
    where [Диагноз] = 'u07.1'
    and [Исход заболевания] = 'Выздоровление'
    group by [Дата исхода заболевания]
    order by [Дата исхода заболевания]

    """

    df_1 = covid_sql(SQL_1)
    df_2 = covid_sql(SQL_2)

    filename_1 = "/tmp/all.xlsx"
    filename_2 = "/tmp/rec.xlsx"
    df_1.to_excel(filename_1)
    df_2.to_excel(filename_2)

    return filename_1 + ";" + filename_2
