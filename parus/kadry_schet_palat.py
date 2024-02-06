from base import parus_sql

sql = """
SELECT
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
WHERE rf.CODE = 'Кадры Счётная палата' 
and r.BDATE =  to_date('20240201','yyyy-mm-dd')
"""

DICT_POKAZATEL = {
    "schetp_01": (2021, 1),
    "schetp_02": (2021, 2),
    "schetsumm_01": (2021, 3),
    "schetp_03": (2021, 4),
    "schetp_04": (2021, 5),
    "schetp_05": (2021, 6),
    "schetp_06": (2021, 7),
    "schetp_07": (2021, 8),
    "schetp_08": (2021, 9),
    "schetp_09": (2021, 10),
    "schetp_10": (2021, 11),
    "schetp_11": (2021, 12),
    "schetp_12": (2021, 13),
    "schetp_13": (2021, 14),
    "schetp_14": (2021, 15),
    "schetp_15": (2021, 16),
    "schetp_16": (2021, 17),
    "schetp_17": (2021, 18),
    "schetp_18": (2022, 1),
    "schetp_19": (2022, 2),
    "schetsumm_02": (2022, 3),
    "schetp_20": (2022, 4),
    "schetp_21": (2022, 5),
    "schetp_22": (2022, 6),
    "schetp_23": (2022, 7),
    "schetp_24": (2022, 8),
    "schetp_25": (2022, 9),
    "schetp_26": (2022, 10),
    "schetp_27": (2022, 11),
    "schetp_28": (2022, 12),
    "schetp_29": (2022, 13),
    "schetp_30": (2022, 14),
    "schetp_31": (2022, 15),
    "schetp_32": (2022, 16),
    "schetp_33": (2022, 17),
    "schetp_34": (2022, 18),
    "schetp_35": (2023, 1),
    "schetp_36": (2023, 2),
    "schetsumm_03": (2023, 3),
    "schetp_37": (2023, 4),
    "schetp_38": (2023, 5),
    "schetp_39": (2023, 6),
    "schetp_40": (2023, 7),
    "schetp_41": (2023, 8),
    "schetp_42": (2023, 9),
    "schetp_43": (2023, 10),
    "schetp_44": (2023, 11),
    "schetp_45": (2023, 12),
    "schetp_46": (2023, 13),
    "schetp_47": (2023, 14),
    "schetp_48": (2023, 15),
    "schetp_49": (2023, 16),
    "schetp_50": (2023, 17),
    "schetp_51": (2023, 18),
}


def kadry_schet_palat():
    """Генерация словаря для того чтобы расположить показатели в нескеолько строк"""

    df = parus_sql(sql)
    if df is None:
        return

    a = df.copy()
    a["year"] = a["POKAZATEL"].map(lambda x: DICT_POKAZATEL.get(x, (None, None))[0])
    a["column"] = a["POKAZATEL"].map(lambda x: DICT_POKAZATEL.get(x, (None, None))[1])

    a = a.pivot_table(
        index=["ORGANIZATION", "year"],
        columns="column",
        values="VALUE",
        aggfunc="first",
    )

    file_1 = "/tmp/приложение_3.xlsx"
    a.to_excel(file_1)

    dict_ = {}

    for i in range(1, 15):
        dict_[f"schetpl_{i:02}"] = (2021, "Врачи", i)

    for i in range(15, 28):
        if i == 18:
            continue
        dict_[f"schetpl_{i:02}"] = (
            2021,
            "Средний медицинский персонал",
            i - 12 if i < 18 else i - 13,
        )

    for i in range(28, 42):
        dict_[f"schetpl_{i:02}"] = (2022, "Врачи", i - 27)

    for i in range(42, 54):
        dict_[f"schetpl_{i:02}"] = (2022, "Средний медицинский персонал", i - 39)

    for i in range(54, 68):
        dict_[f"schetpl_{i:02}"] = (2023, "Врачи", i - 53)

    for i in range(69, 81):
        dict_[f"schetpl_{i:02}"] = (2023, "Средний медицинский персонал", i - 66)

    b = df.copy()

    b["year"] = b["POKAZATEL"].map(lambda x: dict_.get(x, (None, None, None))[0])
    b["post"] = b["POKAZATEL"].map(lambda x: dict_.get(x, (None, None, None))[1])
    b["column"] = b["POKAZATEL"].map(lambda x: dict_.get(x, (None, None, None))[2])

    b = b.pivot_table(
        index=["ORGANIZATION", "year", "post"],
        columns="column",
        values="VALUE",
        aggfunc="first",
    )
    file_2 = "/tmp/приложение_5.xlsx"
    b.to_excel(file_2)

    return file_1 + ";" + file_2
