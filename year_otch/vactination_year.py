from datetime import datetime, timedelta
from pandas import concat

from base import parus_sql

sql = """
SELECT
    a.AGNNAME ORGANIZATION ,
    bi.CODE  pokazatel,
    NUMVAL value
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
WHERE rf.CODE = 'ВакцинацияОбщ' 
and bi.CODE IN (__pokazatel__)
and r.BDATE between  to_date(__start__,'yyyy-mm-dd')
    AND  to_date(__stop__,'yyyy-mm-dd')
"""

pokazatel = {
    "1. ГРИПП": [
        "vakgr_01",
        "vakgr_02",
        "vakgr_03",
        "vakgr_04",
        "vakgr_05",
        "vakgr_06",
        "vakgr_07",
        "vakgr_08",
        "vakgr_09",
        "vakgr_10",
        "vakgr_11",
        "vakgr_12",
    ],
    "2. Коронавирус": [
        "vakcov_01",
        "vakcov_02",
        "vakcov_03",
        "vakcov_04",
        "vakcov_05",
        "vakcov_06",
        "vakcov_07",
        "vakcov_08",
    ],
    "3. Дифтерия": [
        "vakdift_01",
        "vakdift_02",
        "vakdift_03",
        "vakdift_04",
        "vakdift_05",
        "vakdift_06",
        "vakdift_07",
        "vakdift_08",
    ],
    "4. Геппатит В": [
        "vakgep_01",
        "vakgep_02",
        "vakgep_03",
        "vakgep_04",
        "vakgep_05",
        "vakgep_06",
        "vakgep_07",
        "vakgep_08",
    ],
    "5. Корь": [
        "vakjak_01",
        "vakjak_02",
        "vakjak_03",
        "vakjak_04",
        "vakjak_05",
        "vakjak_06",
        "vakjak_07",
        "vakjak_08",
    ],
    "6. Краснуха": [
        "vakkr_01",
        "vakkr_02",
        "vakkr_03",
        "vakkr_04",
        "vakkr_05",
        "vakkr_06",
        "vakkr_07",
        "vakkr_08",
    ],
    "7. Брюшнойтиф": [
        "vakbrtif_01",
        "vakbrtif_02",
        "vakbrtif_03",
        "vakbrtif_04",
        "vakbrtif_05",
        "vakbrtif_06",
        "vakbrtif_07",
        "vakbrtif_08",
    ],
    "8. геппатит А": [
        "vakgepa_01",
        "vakgepa_02",
        "vakgepa_03",
        "vakgepa_04",
        "vakgepa_05",
        "vakgepa_06",
        "vakgepa_07",
        "vakgepa_08",
    ],
}


def vactination_year():
    """отчет годовой для Захватовой по Вакцинации мед работников"""

    START = (datetime.today() - timedelta(days=90)).strftime("%Y%m%d")
    STOP = (datetime.today() + timedelta(days=90)).strftime("%Y%m%d")
    list_ = []
    for key, value in pokazatel.items():
        # вставляем в запрос показатели и даты
        _sql = sql.replace("__pokazatel__", "".join("'" + _ + "', " for _ in value))
        _sql = _sql.replace("__start__", START)
        _sql = _sql.replace("__stop__", STOP)
        _sql = _sql.replace("', )", "')")

        df = parus_sql(_sql)
        df["диагноз"] = key
        if key == "1. ГРИПП":
            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_02", "_03")), "Персонал"
            ] = "1. врачи"
            df.loc[
                df.POKAZATEL.str.endswith(("_04", "_05", "_06")), "Персонал"
            ] = "2. средний медицинский персонал"
            df.loc[
                df.POKAZATEL.str.endswith(("_07", "_08", "_09")), "Персонал"
            ] = "3. младший медицинский персонал"
            df.loc[
                df.POKAZATEL.str.endswith(("_10", "_11", "_12")), "Персонал"
            ] = "4. прочие"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_04", "_07", "_10")), "вакцинация"
            ] = "0. Численность МР"
            df.loc[
                df.POKAZATEL.str.endswith(("_02", "_05", "_08", "_11")), "вакцинация"
            ] = "1. МР подлежащие вакцинации"
            df.loc[
                df.POKAZATEL.str.endswith(("_03", "_06", "_09", "_12")), "вакцинация"
            ] = "2. МР привитые"
        else:
            df.loc[df.POKAZATEL.str.endswith(("_01", "_02")), "Персонал"] = "1. врачи"
            df.loc[
                df.POKAZATEL.str.endswith(("_03", "_04")), "Персонал"
            ] = "2. средний медицинский персонал"
            df.loc[
                df.POKAZATEL.str.endswith(("_05", "_06")), "Персонал"
            ] = "3. младший медицинский персонал"
            df.loc[df.POKAZATEL.str.endswith(("_07", "_08")), "Персонал"] = "4. прочие"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_03", "_05", "_07")), "вакцинация"
            ] = "1. МР подлежащие вакцинации"
            df.loc[
                df.POKAZATEL.str.endswith(("_02", "_04", "_06", "_08")), "вакцинация"
            ] = "2. МР привитые"

        list_.append(df)

    # собираем отчеты в кучу
    df = concat(list_)
    df = df.pivot_table(
        index=["ORGANIZATION", "Персонал"],
        columns=["диагноз", "вакцинация"],
        values=["VALUE"],
        aggfunc="first",
    ).stack(0)

    for key in pokazatel.keys():
        df[(key, "Охват")] = (
            100 * df[(key, "2. МР привитые")] / df[(key, "1. МР подлежащие вакцинации")]
        ).round()

    df = df.reindex(sorted(df.columns), axis=1)

    filename = f"/tmp/Вакцинация_общая_{datetime.now().year}.xlsx"
    df.to_excel(filename)
    return filename
