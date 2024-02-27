import pandas as pd
from glob import glob


def lab_koklucsh():
    """Разовый отчет, простонужно от безысходности"""

    path = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/[!~]*.xlsx"
    mess = ""

    # все первые таблицы
    tables = [
        "Таблица 1.1",
        "Таблица 2.1",
        "Таблица СК1.1",
        "Таблица СК2.1",
        "Таблица БК1.1",
        "Таблица БК2.1",
    ]

    for table in tables:
        list_ = []
        for file in glob(path):
            org = file.rsplit("месяцам", 1)[-1]
            org = org.replace("_", "")
            try:
                df = pd.read_excel(file, sheet_name=table, header=1, usecols="A,C,D")

                year = 2018
                for i in df.index:
                    if not pd.isnull(df.at[i, "Год"]):
                        year = df.at[i, "Год"]
                    else:
                        df.loc[i, "Год"] = year
            except:
                mess += f"{table} ошибка в {org}\n"
                continue
            df["org"] = org
            df = df.fillna(0)
            list_.append(df)

        df = pd.concat(list_)
        df = df.pivot_table(
            index=["Год", "Цель обследования"],
            columns=["org"],
            values=["Число обследованных лиц"],
            aggfunc="first",
        )
        filename = f"/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/{table}.xlsx"
        df.to_excel(filename)

    # 'Таблица 1.2'

    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица 1.2",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K,L",
            )
            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[0, col]}, inplace=True)
            df = df.drop(df.index[0])
            df.dropna(how="all", inplace=True)
            df = df.loc[~df["Цель обследования"].isnull()]

            year = 2018
            reag = ""
            for i in df.index:
                if not pd.isnull(df.at[i, "Год"]):
                    year = df.at[i, "Год"]
                else:
                    df.loc[i, "Год"] = year

                if not pd.isnull(
                    df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                ):
                    reag = df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                else:
                    df.loc[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ] = reag
        except:
            mess += f"Таблица 1.2 ошибка в {org}\n"
            continue
        df["org"] = org
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица 1.2.xlsx"
    df.to_excel(filename)

    # 'Таблица 1.3'
    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица 1.3",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K,L",
            )
            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[0, col]}, inplace=True)
            df = df.drop(df.index[0])
            df.dropna(how="all", inplace=True)
            df = df.loc[~df["Цель обследования"].isnull()]

            month = "январь"
            reag = ""
            for i in df.index:
                if not pd.isnull(df.at[i, "Месяц 2023 года"]):
                    month = df.at[i, "Месяц 2023 года"]
                else:
                    df.loc[i, "Месяц 2023 года"] = month

                if not pd.isnull(
                    df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                ):
                    reag = df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                else:
                    df.loc[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ] = reag
        except:
            mess += f"Таблица 1.3 ошибка в {org}\n"
            continue
        df["org"] = org
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица 1.3.xlsx"
    df.to_excel(filename)

    # 'Таблица 1.4'

    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица 1.4",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K,L",
            )
            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[0, col]}, inplace=True)
            df = df.drop(df.index[0])
            df.dropna(how="all", inplace=True)
            df = df.loc[~df["Цель обследования"].isnull()]

            month = "январь"
            reag = ""
            for i in df.index:
                if not pd.isnull(df.at[i, "Месяц 2024 года"]):
                    month = df.at[i, "Месяц 2024 года"]
                else:
                    df.loc[i, "Месяц 2024 года"] = month

                if not pd.isnull(
                    df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                ):
                    reag = df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                else:
                    df.loc[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ] = reag
        except:
            mess += f"Таблица 1.4 ошибка в {org}\n"
            continue
        df["org"] = org
        list_.append(df)
    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица 1.4.xlsx"
    df.to_excel(filename)

    # 'Таблица  2.2'
    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица 2.2",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K,L",
            )
            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[0, col]}, inplace=True)
            df = df.drop(df.index[0])
            df.dropna(how="all", inplace=True)
            df = df.loc[~df["Цель обследования"].isnull()]

            year = 2018
            reag = ""
            for i in df.index:
                if not pd.isnull(df.at[i, "Год"]):
                    year = df.at[i, "Год"]
                else:
                    df.loc[i, "Год"] = year

                if not pd.isnull(
                    df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                ):
                    reag = df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                else:
                    df.loc[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ] = reag
        except:
            mess += f"Таблица 2.2 ошибка в {org}\n"
            continue
        df["org"] = org
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица 2.2.xlsx"
    df.to_excel(filename)

    # 'Таблица  2.3'
    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица 2.3",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K,L",
            )

            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[0, col]}, inplace=True)
            df = df.drop(df.index[0])
            df.dropna(how="all", inplace=True)
            df = df.loc[~df["Цель обследования"].isnull()]

            month = "январь"
            reag = ""
            for i in df.index:
                if not pd.isnull(df.at[i, "Месяц 2023 года"]):
                    month = df.at[i, "Месяц 2023 года"]
                else:
                    df.loc[i, "Месяц 2023 года"] = month

                if not pd.isnull(
                    df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                ):
                    reag = df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                else:
                    df.loc[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ] = reag
        except:
            mess += f"Таблица 2.3 ошибка в {org}\n"
            continue
        df["org"] = org
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица 2.3.xlsx"
    df.to_excel(filename)

    # 'Таблица  2.4

    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица 2.4",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K,L",
            )

            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[0, col]}, inplace=True)
            df = df.drop(df.index[0])
            df.dropna(how="all", inplace=True)
            df = df.loc[~df["Цель обследования"].isnull()]

            month = "январь"
            reag = ""
            for i in df.index:
                if not pd.isnull(df.at[i, "Месяц 2024 года"]):
                    month = df.at[i, "Месяц 2024 года"]
                else:
                    df.loc[i, "Месяц 2024 года"] = month

                if not pd.isnull(
                    df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                ):
                    reag = df.at[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ]
                else:
                    df.loc[
                        i,
                        "Набор реагентов, используемый\nна этапе проведения амплификации",
                    ] = reag
        except:
            mess += f"Таблица 2.4 ошибка в {org}\n"
            continue
        df["org"] = org
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица 2.4.xlsx"
    df.to_excel(filename)

    # Таблица СК1.2
    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица СК1.2",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K",
            )

            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[1, col]}, inplace=True)
            df = df.loc[~df["Возрастной контингент"].isnull()]

            year = 2018
            for i in df.index:
                if not pd.isnull(df.at[i, "Год"]):
                    year = df.at[i, "Год"]
                else:
                    df.loc[i, "Год"] = year
        except:
            mess += f"Таблица СК1.2 ошибка в {org}\n"
            continue
        df["org"] = org
        df = df.fillna(0)
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица СК1.2.xlsx"
    df.to_excel(filename)

    # Таблица СК1.3

    list_ = []
    for file in glob(path):
        # print(file)
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        names = [
            "Год",
            "Возрастной контингент",
            "РПГА всего анализов",
            "РПГА число лиц",
            "Число серопозитивных лиц",
            "РА всего анализов",
            "РА число лиц",
            "РА Число серопозитивных лиц",
        ]
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица СК1.3",
                header=1,
                usecols="A,C,D,E,F,G,H,I",
                names=names,
            )
            df = df.loc[~df["Возрастной контингент"].isnull()]

            year = 2018
            for i in df.index:
                if not pd.isnull(df.at[i, "Год"]):
                    year = df.at[i, "Год"]
                else:
                    df.loc[i, "Год"] = year
        except:
            mess += f"Таблица СК1.3 ошибка в {org}\n"
            continue

        df["org"] = org
        df = df.fillna(0)
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица СК1.3.xlsx"
    df.to_excel(filename)

    # Таблица СК2.2

    list_ = []
    for file in glob(path):
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица СК2.2",
                header=1,
                usecols="A,C,D,E,F,G,H,I,J,K",
            )

            for col in df.columns:
                if "Unnamed" in col:
                    df.rename(columns={col: df.at[1, col]}, inplace=True)
            df = df.loc[~df["Возрастной контингент"].isnull()]

            year = 2018
            for i in df.index:
                if not pd.isnull(df.at[i, "Год"]):
                    year = df.at[i, "Год"]
                else:
                    df.loc[i, "Год"] = year
        except:
            mess += f"Таблица СК2.2 ошибка в {org}\n"
            continue
        df["org"] = org
        df = df.fillna(0)
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица СК2.2.xlsx"
    df.to_excel(filename)

    # Таблица СК2.3

    list_ = []
    for file in glob(path):
        org = file.rsplit("месяцам", 1)[-1]
        org = org.replace("_", "")
        names = [
            "Год",
            "Возрастной контингент",
            "РПГА всего анализов",
            "РПГА число лиц",
            "Число серопозитивных лиц",
            "РА всего анализов",
            "РА число лиц",
            "РА Число серопозитивных лиц",
        ]
        try:
            df = pd.read_excel(
                file,
                sheet_name="Таблица СК2.3",
                header=1,
                usecols="A,C,D,E,F,G,H,I",
                names=names,
            )

            df = df.loc[~df["Возрастной контингент"].isnull()]

            year = 2018
            for i in df.index:
                if not pd.isnull(df.at[i, "Год"]):
                    year = df.at[i, "Год"]
                else:
                    df.loc[i, "Год"] = year
        except:
            mess += f"Таблица СК2.3 ошибка в {org}\n"
            continue

        df["org"] = org
        df = df.fillna(0)
        list_.append(df)

    df = pd.concat(list_)
    filename = "/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/Таблица СК2.3.xlsx"
    df.to_excel(filename)

    # Таблица БК1.2

    tables = ["Таблица БК1.2", "Таблица БК2.2"]
    list_ = []
    for table in tables:
        for file in glob(path):
            org = file.rsplit("месяцам", 1)[-1]
            org = org.replace("_", "")
            names = [
                "Год",
                "Возрастной контингент",
                "Количество выполненных анализов",
                "Bordetella pertussis 1.2.3.",
                "Bordetella pertussis 1.2.0",
                "Bordetella pertussis 1.0.0.",
                "Bordetella pertussis 1.0.3",
                "Bordetella pertussis -",
                "Bordetella parapertussis",
                "Bordetella bronchiseptica",
                "Других представителей рода Bordetella вид",
                "Других представителей рода Bordetella количество",
            ]
            try:
                df = pd.read_excel(
                    file,
                    sheet_name=table,
                    header=4,
                    usecols="A,C,D,E,F,G,H,I,J,K,L,M",
                    names=names,
                )
                df = df.loc[~df["Возрастной контингент"].isnull()]

                year = 2018
                for i in df.index:
                    if not pd.isnull(df.at[i, "Год"]):
                        year = df.at[i, "Год"]
                    else:
                        df.loc[i, "Год"] = year
            except:
                mess += f"{table} ошибка в {org}\n"
                continue

            df["org"] = org
            df = df.fillna(0)
            list_.append(df)

        df = pd.concat(list_)
        filename = f"/mnt/lab/2024 год/ДИФТЕРИЯ КОКЛЮШ_43 таблицы от 20.02.2023/ОТВЕТЫ МО/svod/{table}.xlsx"
        df.to_excel(filename)

    if mess == "":
        mess = "Все получилось!"
    else:
        mess = mess.replace("_", " ")

    return mess
