from base import parus_sql
from system import write_excel

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

    # ===================== формируем файл

    # filename = "/tmp/кадры_счет_14_15_16.xlsx"
    # dict_ = {"прил. 14": pr_14}
    # write_excel(filename, dict_)

    filename_14 = "/tmp/кадры_счет_приложение_14.xlsx"
    pr_14.to_excel(filename_14)

    return filename_14
