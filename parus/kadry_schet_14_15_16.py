from base import parus_sql

# from system import write_excel

SQL_14 = """SELECT
    extract(year from r.BDATE) year,
    a.AGNNAME ORGANIZATION ,
    bi.CODE  pokazatel,
    CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
        WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
        WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
        ELSE NULL END value
FROM PARUS.BLINDEXVALUES  d
INNER JOIN PARUS.BLSUBREPORTS s
ON (d.PRN = s.RN)
INNER JOIN PARUS.BLREPORTS r
ON(s.PRN = r.RN)
INNER JOIN PARUS.AGNLIST a 
on(r.AGENT = a.rn)
INNER JOIN PARUS.BLREPFORMED pf
on(r.BLREPFORMED = pf.RN)
INNER JOIN PARUS.BLREPFORM rf 
on(pf.PRN = rf.RN)
INNER JOIN PARUS.BALANCEINDEXES bi 
on(d.BALANCEINDEX = bi.RN)
WHERE rf.CODE = 'СчетПалата141516'
and bi.CODE like 'schetpl_0%'"""

SQL_15 = """SELECT
    extract(year from r.BDATE) year,
    a.AGNNAME ORGANIZATION ,
    bi.CODE  pokazatel,
    CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
        WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
        WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
        ELSE NULL END value
FROM PARUS.BLINDEXVALUES  d
INNER JOIN PARUS.BLSUBREPORTS s
ON (d.PRN = s.RN)
INNER JOIN PARUS.BLREPORTS r
ON(s.PRN = r.RN)
INNER JOIN PARUS.AGNLIST a 
on(r.AGENT = a.rn)
INNER JOIN PARUS.BLREPFORMED pf
on(r.BLREPFORMED = pf.RN)
INNER JOIN PARUS.BLREPFORM rf 
on(pf.PRN = rf.RN)
INNER JOIN PARUS.BALANCEINDEXES bi 
on(d.BALANCEINDEX = bi.RN)
WHERE rf.CODE = 'СчетПалата141516'
and bi.CODE like 'schetplt_0%'
"""


def kadry_schet_14_15_16():
    # ================ приложение 14
    df = parus_sql(SQL_14)

    df.loc[
        df.POKAZATEL.str.endswith(("01", "02", "03", "04", "05", "06")),
        "Количество работников",
    ] = "1.1 Принятых ВСЕГО"
    df.loc[
        df.POKAZATEL.str.endswith(("07", "08", "09", "10", "11", "12")),
        "Количество работников",
    ] = "1.1.1 после окончания учебного заведения"
    df.loc[
        df.POKAZATEL.str.endswith(("13", "14", "15", "16", "17", "18")),
        "Количество работников",
    ] = "1.1.2 вновь приняты, после выхода на пенсию"
    df.loc[
        df.POKAZATEL.str.endswith(("19", "20", "21", "22", "23", "24")),
        "Количество работников",
    ] = "1.1.3 приняты из других МО"

    df.loc[
        df.POKAZATEL.str.endswith(("25", "26", "27", "28", "29", "30")),
        "Количество работников",
    ] = "1.2 Уволенных ВСЕГО"
    df.loc[
        df.POKAZATEL.str.endswith(("31", "32", "33", "34", "35", "36")),
        "Количество работников",
    ] = "1.2.1 по собственному желанию"
    df.loc[
        df.POKAZATEL.str.endswith(("37", "38", "39", "40", "41", "42")),
        "Количество работников",
    ] = "1.2.2 в связи с выходом на пенсию"
    df.loc[
        df.POKAZATEL.str.endswith(("43", "44", "45", "46", "47", "48")),
        "Количество работников",
    ] = "1.2.3 по решению работодателя"
    df.loc[
        df.POKAZATEL.str.endswith(("49", "50", "51", "52", "53", "54")),
        "Количество работников",
    ] = "1.2.3 по иным причинам"

    df.loc[
        df.POKAZATEL.str.endswith(
            ("01", "07", "13", "19", "25", "31", "37", "43", "49")
        ),
        "Должности",
    ] = "1. АУП"
    df.loc[
        df.POKAZATEL.str.endswith(
            ("02", "08", "14", "20", "26", "32", "38", "44", "50")
        ),
        "Должности",
    ] = "2. Врачи ВСЕГО"
    df.loc[
        df.POKAZATEL.str.endswith(
            ("03", "09", "15", "21", "27", "33", "39", "45", "51")
        ),
        "Должности",
    ] = "3. Врачи заместители ГВ и руководители"
    df.loc[
        df.POKAZATEL.str.endswith(
            ("04", "10", "16", "22", "28", "34", "40", "46", "52")
        ),
        "Должности",
    ] = "4. СМП"
    df.loc[
        df.POKAZATEL.str.endswith(
            ("05", "11", "17", "23", "29", "35", "41", "47", "53")
        ),
        "Должности",
    ] = "5. ММП"
    df.loc[
        df.POKAZATEL.str.endswith(
            ("06", "12", "18", "24", "30", "36", "42", "48", "54")
        ),
        "Должности",
    ] = "6. Прочий персонал"

    pr_14 = df.pivot_table(
        index=["ORGANIZATION", "Количество работников"],
        columns=["YEAR", "Должности"],
        values=["VALUE"],
        aggfunc="first",
    )

    filename_14 = "/tmp/кадры_счет_приложение_14.xlsx"
    pr_14.to_excel(filename_14)
    # ============ приложение 15
    df = parus_sql(SQL_15)
    df.loc[
        df.POKAZATEL.str.endswith(
            (
                "01",
                "02",
                "03",
                "04",
                "05",
                "06",
                "07",
                "08",
                "09",
                "10",
                "11",
                "12",
                "13",
            )
        ),
        "Сотрудники экономической службы",
    ] = "1.1 Руководители"
    df.loc[
        df.POKAZATEL.str.endswith(
            (
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
            )
        ),
        "Сотрудники экономической службы",
    ] = "1.2 без руководителей"
    df.loc[
        df.POKAZATEL.str.endswith(
            (
                "27",
                "28",
                "29",
                "30",
                "31",
                "32",
                "33",
                "34",
                "35",
                "36",
                "37",
                "38",
                "39",
            )
        ),
        "Сотрудники экономической службы",
    ] = "1.2.1 из них, переведенные из бухгалтерии"
    df.loc[
        df.POKAZATEL.str.endswith(
            (
                "40",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "47",
                "48",
                "49",
                "50",
                "51",
                "52",
            )
        ),
        "Сотрудники экономической службы",
    ] = "1.3 ВСЕГО"

    df.loc[
        df.POKAZATEL.str.endswith(("01", "14", "27", "40")), "параметры"
    ] = "01. Средний возраст"
    df.loc[
        df.POKAZATEL.str.endswith(("02", "15", "28", "41")), "параметры"
    ] = "02. Высшее образование"
    df.loc[
        df.POKAZATEL.str.endswith(("03", "16", "29", "42")), "параметры"
    ] = "03. Неоконченное высшее"
    df.loc[
        df.POKAZATEL.str.endswith(("04", "17", "30", "43")), "параметры"
    ] = "04. Среднее профессиональное"
    df.loc[
        df.POKAZATEL.str.endswith(("05", "18", "31", "44")), "параметры"
    ] = "05. С экономическим (финансовым) образованием"
    df.loc[
        df.POKAZATEL.str.endswith(("06", "19", "32", "45")), "параметры"
    ] = "06. иным образованием"
    df.loc[
        df.POKAZATEL.str.endswith(("07", "20", "33", "46")), "параметры"
    ] = "07. не имеющие образование"
    df.loc[
        df.POKAZATEL.str.endswith(("08", "21", "34", "47")), "параметры"
    ] = "08. Количество штатных единиц"
    df.loc[
        df.POKAZATEL.str.endswith(("09", "22", "35", "48")), "параметры"
    ] = "09. Количество занятых ставок"
    df.loc[
        df.POKAZATEL.str.endswith(("10", "23", "36", "49")), "параметры"
    ] = "10. Количество физических лиц"
    df.loc[
        df.POKAZATEL.str.endswith(("11", "24", "37", "50")), "параметры"
    ] = "11. Фонд оплаты труда по итогам периода"
    df.loc[
        df.POKAZATEL.str.endswith(("12", "25", "38", "51")), "параметры"
    ] = "12. Доля фонда оплаты труда %"
    df.loc[
        df.POKAZATEL.str.endswith(("13", "26", "39", "52")), "параметры"
    ] = "13. Среднемесячная зарплата"

    pr_15 = df.pivot_table(
        index=["ORGANIZATION", "Сотрудники экономической службы", "YEAR"],
        columns=["параметры"],
        values=["VALUE"],
        aggfunc="first",
    ).stack(0)

    filename_15 = "/tmp/кадры_счет_приложение_15.xlsx"
    pr_15.to_excel(filename_15)

    # ===================== формируем файл

    # filename = "/tmp/кадры_счет_14_15_16.xlsx"
    # dict_ = {"прил. 14": pr_14}
    # write_excel(filename, dict_)

    return filename_14 + ";" + filename_15
