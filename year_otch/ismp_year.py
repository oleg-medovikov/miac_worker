from datetime import datetime, timedelta
import pandas as pd

from base import parus_sql

pokazatel = {
    "ИОХВ": [
        "iohv_00",
        "iohv_01",
        "iohv_02",
        "iohv_03",
        "iohv_04",
        "iohv_05",
        "iohv_06",
        "iohv_07",
        "iohv_08",
        "iohv_09",
        "iohv_10",
        "iohv_11",
        "iohv_12",
    ],
    "мо ИОХВ": [
        "moiohv_01",
        "moiohv_02",
        "moiohv_03",
        "moiohv_04",
        "moiohv_05",
        "moiohv_06",
        "moiohv_07",
        "moiohv_08",
        "moiohv_09",
        "moiohv_10",
        "moiohv_11",
        "moiohv_12",
        "moiohv_13",
        "moiohv_14",
        "moiohv_15",
        "moiohv_16",
        "moiohv_17",
        "moiohv_18",
        "moiohv_19",
        "moiohv_20",
        "moiohv_21",
        "moiohv_22",
        "moiohv_23",
        "moiohv_24",
        "moiohv_25",
        "moiohv_26",
        "moiohv_27",
        "moiohv_28",
        "moiohv_29",
        "moiohv_30",
    ],
    "ВИНДП": [
        "vindp_01",
        "vindp_02",
        "vindp_03",
        "vindp_04",
        "vindp_05",
        "vindp_06",
        "vindp_07",
        "vindp_08",
        "vindp_09",
        "vindp_10",
        "vindp_11",
        "vindp_12",
        "vindp_13",
        "vindp_14",
        "vindp_15",
        "vindp_16",
        "vindp_17",
        "vindp_18",
    ],
    "мо ВИНДП": [
        "movimvp_01",
        "movimvp_02",
        "movimvp_03",
        "movimvp_04",
        "movimvp_05",
        "movimvp_06",
        "movimvp_07",
        "movimvp_08",
        "movimvp_09",
        "movimvp_10",
        "movimvp_11",
        "movimvp_12",
        "movimvp_13",
        "movimvp_14",
        "movimvp_15",
        "movimvp_16",
        "movimvp_17",
        "movimvp_18",
        "movimvp_19",
        "movimvp_20",
        "movindp_01",
        "movindp_02",
        "movindp_03",
        "movindp_04",
        "movindp_05",
        "movindp_06",
        "movindp_07",
        "movindp_08",
        "movindp_09",
        "movindp_10",
        "movindp_11",
        "movindp_12",
        "movindp_13",
        "movindp_14",
        "movindp_15",
        "movindp_16",
        "movindp_17",
        "movindp_18",
        "movindp_19",
        "movindp_20",
    ],
    "ВИМВП": [
        "vimvp_01",
        "vimvp_02",
        "vimvp_03",
        "vimvp_04",
        "vimvp_05",
        "vimvp_06",
        "vimvp_07",
        "vimvp_08",
        "vimvp_09",
        "vimvp_10",
        "vimvp_11",
        "vimvp_12",
        "vimvp_13",
        "vimvp_14",
        "vimvp_15",
        "vimvp_16",
        "vimvp_17",
        "vimvp_18",
    ],
    "мо ВИМВП": [
        "movimvp_01",
        "movimvp_02",
        "movimvp_03",
        "movimvp_04",
        "movimvp_05",
        "movimvp_06",
        "movimvp_07",
        "movimvp_08",
        "movimvp_09",
        "movimvp_10",
        "movimvp_11",
        "movimvp_12",
        "movimvp_13",
        "movimvp_14",
        "movimvp_15",
        "movimvp_16",
        "movimvp_17",
        "movimvp_18",
        "movimvp_19",
        "movimvp_20",
    ],
    "ВИКР": [
        "vikr_01",
        "vikr_02",
        "vikr_03",
        "vikr_04",
        "vikr_05",
        "vikr_06",
        "vikr_07",
        "vikr_08",
        "vikr_09",
        "vikr_10",
        "vikr_11",
        "vikr_12",
        "vikr_13",
        "vikr_14",
        "vikr_15",
        "vikr_16",
        "vikr_17",
        "vikr_18",
    ],
    "мо ВИКР": [
        "movikr_01",
        "movikr_02",
        "movikr_03",
        "movikr_04",
        "movikr_05",
        "movikr_06",
        "movikr_07",
        "movikr_08",
        "movikr_09",
        "movikr_10",
        "movikr_11",
        "movikr_12",
        "movikr_13",
        "movikr_14",
        "movikr_15",
        "movikr_16",
        "movikr_17",
        "movikr_18",
        "movikr_19",
        "movikr_20",
    ],
    "ГСИ": [
        "gsi_01",
        "gsi_02",
        "gsi_03",
        "gsi_04",
        "gsi_05",
        "gsi_06",
        "gsi_07",
        "gsi_08",
        "gsi_09",
        "gsi_10",
        "gsi_11",
        "gsi_12",
        "gsi_13",
        "gsi_14",
        "gsi_15",
        "gsi_16",
        "gsi_17",
        "gsi_18",
    ],
    "мо ГСИ": [
        "mogsi_01",
        "mogsi_02",
        "mogsi_03",
        "mogsi_04",
        "mogsi_05",
        "mogsi_06",
        "mogsi_07",
        "mogsi_08",
        "mogsi_09",
        "mogsi_10",
        "mogsi_11",
        "mogsi_12",
        "mogsi_13",
        "mogsi_14",
        "mogsi_15",
        "mogsi_16",
        "mogsi_17",
        "mogsi_18",
        "mogsi_19",
        "mogsi_20",
        "mogsi_21",
        "mogsi_22",
        "mogsi_23",
        "mogsi_24",
        "mogsi_25",
        "mogsi_26",
        "mogsi_27",
        "mogsi_28",
        "mogsi_29",
        "mogsi_30",
    ],
}

columns = {
    "iohv_00": "01. Число случаев инфекций в области хирургического вмешательства (ИОХВ) ВСЕГО",
    "iohv_01": "02. Число случаев ИОХВ у пациентов с I классом операционной раны",
    "iohv_02": "03. Число случаев ИОХВ у пациентов со II классом операционной раны",
    "iohv_03": "04. Число случаев ИОХВ у пациентов с III классом операционной раны",
    "iohv_04": "05. Число случаев ИОХВ у пациентов с IV классом операционной раны",
    "iohv_05": "06. Количество случаев поверхностных ИОХВ",
    "iohv_06": "07. Количество  случаев глубоких ИОХВ ",
    "iohv_07": "08. Количество случаев ИОХВ органа или полости",
    "iohv_7_": "09. Количество пациентов с ИОХВ  ВСЕГО",
    "iohv_08": "10. Количество пациентов с ИОХВ, выявленными в ходе стационарного лечения",
    "iohv_09": "11. Количество пациентов с ИОХВ, выявленными после выписки из стационара",
    "iohv_10": "12. Количество пациентов с ИОХВ с бактериологическим обследованием",
    "iohv_11": "13. Количество бактериологических исследований биологического материала пациентов с ИОХВ",
    "iohv_12": "14. Количество положительных бактериологических исследований биологического материала пациентов с ИОХВ",
}


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
WHERE rf.CODE = 'ИнфконтрольИСМП' 
and bi.CODE in (__pokazatel__)
and r.BDATE between  to_date(__start__,'yyyymmdd')
    AND  to_date(__stop__,'yyyymmdd')
"""


def ismp_year():
    """"""
    START = (datetime.today() - timedelta(days=90)).strftime("%Y%m%d")
    STOP = (datetime.today() + timedelta(days=90)).strftime("%Y%m%d")

    dict_ = {}
    for key, value in pokazatel.items():
        _sql = sql.replace("__pokazatel__", "".join("'" + _ + "', " for _ in value))
        _sql = _sql.replace("__start__", START)
        _sql = _sql.replace("__stop__", STOP)
        _sql = _sql.replace("', )", "')")
        df = parus_sql(_sql)

        if key == "ИОХВ":
            df.POKAZATEL = df.POKAZATEL.map(columns)
            df = df.pivot_table(
                index=["ORGANIZATION"],
                columns=["POKAZATEL"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df[columns.get("iohv_7_")] = (
                df[columns.get("iohv_08")] + df[columns.get("iohv_09")]
            )
            df.reindex(sorted(df.columns), axis=1)
            df = df.reset_index()
            del df["level_1"]

        if key == "мо ИОХВ":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_04",
                        "_07",
                        "_10",
                        "_13",
                        "_16",
                        "_19",
                        "_22",
                        "_25",
                        "_28",
                    )
                ),
                "Количество изолятов, выделенных из проб биологического материала пациентов",
            ] = "1. с поверхностными ИОХВ"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_02",
                        "_05",
                        "_08",
                        "_11",
                        "_14",
                        "_17",
                        "_20",
                        "_23",
                        "_26",
                        "_29",
                    )
                ),
                "Количество изолятов, выделенных из проб биологического материала пациентов",
            ] = "2. с глубокими ИОХВ"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_03",
                        "_06",
                        "_09",
                        "_12",
                        "_15",
                        "_18",
                        "_21",
                        "_24",
                        "_27",
                        "_30",
                    )
                ),
                "Количество изолятов, выделенных из проб биологического материала пациентов",
            ] = "3. с ИОХВ органа или полости"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_02", "_03")),
                "Наименование микроорганизма",
            ] = "01. Staphylococcus aureus"
            df.loc[
                df.POKAZATEL.str.endswith(("_04", "_05", "_06")),
                "Наименование микроорганизма",
            ] = "02. Klebsiella pneumoniae"
            df.loc[
                df.POKAZATEL.str.endswith(("_07", "_08", "_09")),
                "Наименование микроорганизма",
            ] = "03. Pseudomonas aeruginosa"
            df.loc[
                df.POKAZATEL.str.endswith(("_10", "_11", "_12")),
                "Наименование микроорганизма",
            ] = "04. Acinetobacter baumannii"
            df.loc[
                df.POKAZATEL.str.endswith(("_13", "_14", "_15")),
                "Наименование микроорганизма",
            ] = "05. Enterococcus faecalis"
            df.loc[
                df.POKAZATEL.str.endswith(("_16", "_17", "_18")),
                "Наименование микроорганизма",
            ] = "06. Enterococcus faecium"
            df.loc[
                df.POKAZATEL.str.endswith(("_19", "_20", "_21")),
                "Наименование микроорганизма",
            ] = "07. Echerihia coli"
            df.loc[
                df.POKAZATEL.str.endswith(("_22", "_23", "_24")),
                "Наименование микроорганизма",
            ] = "08. другие Грам(+) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(("_25", "_26", "_27")),
                "Наименование микроорганизма",
            ] = "09. другие Грам(-) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(("_28", "_29", "_30")),
                "Наименование микроорганизма",
            ] = "10. грибы рода Candida"

            df = df.pivot_table(
                index=[
                    "ORGANIZATION",
                    "Количество изолятов, выделенных из проб биологического материала пациентов",
                ],
                columns=["Наименование микроорганизма"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)

            df = df.reset_index()
            del df["level_2"]

        if key == "ВИНДП":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_02",
                        "_03",
                        "_04",
                        "_05",
                        "_06",
                    )
                ),
                "Специализация отделения",
            ] = "1. реанимационное"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_07",
                        "_08",
                        "_09",
                        "_10",
                        "_11",
                        "_12",
                    )
                ),
                "Специализация отделения",
            ] = "2. хирургическое"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_13",
                        "_14",
                        "_15",
                        "_16",
                        "_17",
                        "_18",
                    )
                ),
                "Специализация отделения",
            ] = "3. терапевтическое"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_07", "_13")), "column"
            ] = "1. Количество внутрибольничных случаев инфекций нижних дыхательных путей (ВИНДП) ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_02", "_08", "_14")), "column"
            ] = "2. Количество ВИНДП, связанных с использованием ИВЛ"
            df.loc[
                df.POKAZATEL.str.endswith(("_03", "_09", "_15")), "column"
            ] = "3. Количество пациентов с ВИНДП ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_04", "_10", "_16")), "column"
            ] = "4. Количество пациентов с ВИНДП с бактериологическим обследованием"
            df.loc[
                df.POKAZATEL.str.endswith(("_05", "_11", "_17")), "column"
            ] = "5. Количество бактериологических исследований проб биологического материала пациентов с ВИНДП ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_06", "_12", "_18")), "column"
            ] = "6. Количество положительных бактериологических исследований проб биологического материала пациентов с ВИНДП"

            df = df.pivot_table(
                index=["ORGANIZATION", "Специализация отделения"],
                columns=["column"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        if key == "мо ВИНДП":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_03",
                        "_05",
                        "_07",
                        "_09",
                        "_11",
                        "_13",
                        "_15",
                        "_17",
                        "_19",
                    )
                ),
                "Количество изолятов, выделенных из биологического материала пациентов с ВИНДП",
            ] = "1. ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_02",
                        "_04",
                        "_06",
                        "_08",
                        "_10",
                        "_12",
                        "_14",
                        "_16",
                        "_18",
                        "_20",
                    )
                ),
                "Количество изолятов, выделенных из биологического материала пациентов с ВИНДП",
            ] = "2. связанные с использованием ИВЛ"

            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_02",
                    )
                ),
                "Наименование микроорганизма",
            ] = "01. Staphylococcus aureus"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_03",
                        "_04",
                    )
                ),
                "Наименование микроорганизма",
            ] = "02. Klebsiella pneumoniae"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_05",
                        "_06",
                    )
                ),
                "Наименование микроорганизма",
            ] = "03. Pseudomonas aeruginosa"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_07",
                        "_08",
                    )
                ),
                "Наименование микроорганизма",
            ] = "04. Acinetobacter baumannii"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_09",
                        "_10",
                    )
                ),
                "Наименование микроорганизма",
            ] = "05. Enterococcus faecalis"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_11",
                        "_12",
                    )
                ),
                "Наименование микроорганизма",
            ] = "06. Enterococcus faecium"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_13",
                        "_14",
                    )
                ),
                "Наименование микроорганизма",
            ] = "07. Echerihia coli"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_15",
                        "_16",
                    )
                ),
                "Наименование микроорганизма",
            ] = "08. другие Грам(+) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_17",
                        "_18",
                    )
                ),
                "Наименование микроорганизма",
            ] = "09. другие Грам(-) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_19",
                        "_20",
                    )
                ),
                "Наименование микроорганизма",
            ] = "10. грибы рода Candida"

            df = df.pivot_table(
                index=[
                    "ORGANIZATION",
                    "Количество изолятов, выделенных из биологического материала пациентов с ВИНДП",
                ],
                columns=["Наименование микроорганизма"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        if key == "ВИМВП":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_02",
                        "_03",
                        "_04",
                        "_05",
                        "_06",
                    )
                ),
                "Специализация отделения",
            ] = "1. реанимационное"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_07",
                        "_08",
                        "_09",
                        "_10",
                        "_11",
                        "_12",
                    )
                ),
                "Специализация отделения",
            ] = "2. хирургическое"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_13",
                        "_14",
                        "_15",
                        "_16",
                        "_17",
                        "_18",
                    )
                ),
                "Специализация отделения",
            ] = "3. терапевтическое"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_07", "_13")), "column"
            ] = "1. Количество внутрибольничных случаев инфекций мочевыводящих путей (ВИМВП) ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_02", "_08", "_14")), "column"
            ] = "2. Количество ВИМВП, связанных с использованием катетеров"
            df.loc[
                df.POKAZATEL.str.endswith(("_03", "_09", "_15")), "column"
            ] = "3. Количество пациентов с ВИМВП ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_04", "_10", "_16")), "column"
            ] = "4. Количество пациентов с ВИМВП с бактериологическим обследованием"
            df.loc[
                df.POKAZATEL.str.endswith(("_05", "_11", "_17")), "column"
            ] = "5. Количество пациентов с ВИМВП с бактериологическим обследованием ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_06", "_12", "_18")), "column"
            ] = "6. Количество положительных бактериологических исследований проб биологического материала пациентов с ВИМВП"

            df = df.pivot_table(
                index=["ORGANIZATION", "Специализация отделения"],
                columns=["column"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        if key == "мо ВИМВП":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_03",
                        "_05",
                        "_07",
                        "_09",
                        "_11",
                        "_13",
                        "_15",
                        "_17",
                        "_19",
                    )
                ),
                "Количество изолятов, выделенных из биологического материала пациентов с ВИМВП",
            ] = "1. ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_02",
                        "_04",
                        "_06",
                        "_08",
                        "_10",
                        "_12",
                        "_14",
                        "_16",
                        "_18",
                        "_20",
                    )
                ),
                "Количество изолятов, выделенных из биологического материала пациентов с ВИМВП",
            ] = "2. связанных с использованием мочевых катетеров"

            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_02",
                    )
                ),
                "Наименование микроорганизма",
            ] = "01. Staphylococcus aureus"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_03",
                        "_04",
                    )
                ),
                "Наименование микроорганизма",
            ] = "02. Klebsiella pneumoniae"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_05",
                        "_06",
                    )
                ),
                "Наименование микроорганизма",
            ] = "03. Pseudomonas aeruginosa"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_07",
                        "_08",
                    )
                ),
                "Наименование микроорганизма",
            ] = "04. Acinetobacter baumannii"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_09",
                        "_10",
                    )
                ),
                "Наименование микроорганизма",
            ] = "05. Enterococcus faecalis"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_11",
                        "_12",
                    )
                ),
                "Наименование микроорганизма",
            ] = "06. Enterococcus faecium"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_13",
                        "_14",
                    )
                ),
                "Наименование микроорганизма",
            ] = "07. Echerihia coli"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_15",
                        "_16",
                    )
                ),
                "Наименование микроорганизма",
            ] = "08. другие Грам(+) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_17",
                        "_18",
                    )
                ),
                "Наименование микроорганизма",
            ] = "09. другие Грам(-) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_19",
                        "_20",
                    )
                ),
                "Наименование микроорганизма",
            ] = "10. грибы рода Candida"

            df = df.pivot_table(
                index=[
                    "ORGANIZATION",
                    "Количество изолятов, выделенных из биологического материала пациентов с ВИМВП",
                ],
                columns=["Наименование микроорганизма"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        if key == "ВИКР":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_02",
                        "_03",
                        "_04",
                        "_05",
                        "_06",
                    )
                ),
                "Специализация отделения",
            ] = "1. реанимационное"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_07",
                        "_08",
                        "_09",
                        "_10",
                        "_11",
                        "_12",
                    )
                ),
                "Специализация отделения",
            ] = "2. хирургическое"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_13",
                        "_14",
                        "_15",
                        "_16",
                        "_17",
                        "_18",
                    )
                ),
                "Специализация отделения",
            ] = "3. терапевтическое"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_07", "_13")), "column"
            ] = "1. Количество внутрибольничных случаев инфекций кровотока (ВИКР) ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_02", "_08", "_14")), "column"
            ] = "2. Количество ВИКР, связанных с использованием катетеров"
            df.loc[
                df.POKAZATEL.str.endswith(("_03", "_09", "_15")), "column"
            ] = "3. Количество пациентов с ВИКР ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_04", "_10", "_16")), "column"
            ] = "4. Количество пациентов с  ВИКР с бактериологическим обследованием"
            df.loc[
                df.POKAZATEL.str.endswith(("_05", "_11", "_17")), "column"
            ] = "5. Количество бактериологических исследований проб биологического материала пациентов с ВИКР ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_06", "_12", "_18")), "column"
            ] = "6. Количество положительных бактериологических проб исследований биологического материала пациентов с ВИКР"

            df = df.pivot_table(
                index=["ORGANIZATION", "Специализация отделения"],
                columns=["column"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        if key == "мо ВИКР":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_03",
                        "_05",
                        "_07",
                        "_09",
                        "_11",
                        "_13",
                        "_15",
                        "_17",
                        "_19",
                    )
                ),
                "Количество изолятов, выделенных из биологического материала пациентов с ВИКР",
            ] = "1. ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_02",
                        "_04",
                        "_06",
                        "_08",
                        "_10",
                        "_12",
                        "_14",
                        "_16",
                        "_18",
                        "_20",
                    )
                ),
                "Количество изолятов, выделенных из биологического материала пациентов с ВИКР",
            ] = "2. связанных с использованием катетеров"

            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_02",
                    )
                ),
                "Наименование микроорганизма",
            ] = "01. Staphylococcus aureus"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_03",
                        "_04",
                    )
                ),
                "Наименование микроорганизма",
            ] = "02. Klebsiella pneumoniae"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_05",
                        "_06",
                    )
                ),
                "Наименование микроорганизма",
            ] = "03. Pseudomonas aeruginosa"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_07",
                        "_08",
                    )
                ),
                "Наименование микроорганизма",
            ] = "04. Acinetobacter baumannii"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_09",
                        "_10",
                    )
                ),
                "Наименование микроорганизма",
            ] = "05. Enterococcus faecalis"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_11",
                        "_12",
                    )
                ),
                "Наименование микроорганизма",
            ] = "06. Enterococcus faecium"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_13",
                        "_14",
                    )
                ),
                "Наименование микроорганизма",
            ] = "07. Echerihia coli"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_15",
                        "_16",
                    )
                ),
                "Наименование микроорганизма",
            ] = "08. другие Грам(+) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_17",
                        "_18",
                    )
                ),
                "Наименование микроорганизма",
            ] = "09. другие Грам(-) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_19",
                        "_20",
                    )
                ),
                "Наименование микроорганизма",
            ] = "10. грибы рода Candida"

            df = df.pivot_table(
                index=[
                    "ORGANIZATION",
                    "Количество изолятов, выделенных из биологического материала пациентов с ВИКР",
                ],
                columns=["Наименование микроорганизма"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        if key == "ГСИ":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_02",
                        "_03",
                        "_04",
                        "_05",
                        "_06",
                    )
                ),
                "Специализация отделения",
            ] = "1. реанимационное"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_07",
                        "_08",
                        "_09",
                        "_10",
                        "_11",
                        "_12",
                    )
                ),
                "Специализация отделения",
            ] = "2. хирургическое"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_13",
                        "_14",
                        "_15",
                        "_16",
                        "_17",
                        "_18",
                    )
                ),
                "Специализация отделения",
            ] = "3. терапевтическое"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_07", "_13")), "column"
            ] = "1. Количество внутрибольничных случаев абсцессов ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_02", "_08", "_14")), "column"
            ] = "2. Количество внутрибольничных случаев флегмон ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_03", "_09", "_15")), "column"
            ] = "3. Количество внутрибольничных случаев флебитов ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_04", "_10", "_16")), "column"
            ] = "4. Количество пациентов с прочими ГСИ с бактериологическим обследованием"
            df.loc[
                df.POKAZATEL.str.endswith(("_05", "_11", "_17")), "column"
            ] = "5. Количество бактериологических исследований биологического материала пациентов с прочими ГСИ ВСЕГО"
            df.loc[
                df.POKAZATEL.str.endswith(("_06", "_12", "_18")), "column"
            ] = "6. Количество положительных бактериологических исследований биологического материала пациентов с ГСИ"

            df = df.pivot_table(
                index=["ORGANIZATION", "Специализация отделения"],
                columns=["column"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        if key == "мо ГСИ":
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_01",
                        "_04",
                        "_07",
                        "_10",
                        "_13",
                        "_16",
                        "_19",
                        "_22",
                        "_25",
                        "_28",
                    )
                ),
                "Количество изолятов, выделенных из проб биологического материала пациентов",
            ] = "1. с внутрибольничными абсцессами"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_02",
                        "_05",
                        "_08",
                        "_11",
                        "_14",
                        "_17",
                        "_20",
                        "_23",
                        "_26",
                        "_29",
                    )
                ),
                "Количество изолятов, выделенных из проб биологического материала пациентов",
            ] = "2. с внутрибольничными флебитами"
            df.loc[
                df.POKAZATEL.str.endswith(
                    (
                        "_03",
                        "_06",
                        "_09",
                        "_12",
                        "_15",
                        "_18",
                        "_21",
                        "_24",
                        "_27",
                        "_30",
                    )
                ),
                "Количество изолятов, выделенных из проб биологического материала пациентов",
            ] = "3. с внутрибольничными флегмонами"

            df.loc[
                df.POKAZATEL.str.endswith(("_01", "_02", "_03")),
                "Наименование микроорганизма",
            ] = "01. Staphylococcus aureus"
            df.loc[
                df.POKAZATEL.str.endswith(("_04", "_05", "_06")),
                "Наименование микроорганизма",
            ] = "02. Klebsiella pneumoniae"
            df.loc[
                df.POKAZATEL.str.endswith(("_07", "_08", "_09")),
                "Наименование микроорганизма",
            ] = "03. Pseudomonas aeruginosa"
            df.loc[
                df.POKAZATEL.str.endswith(("_10", "_11", "_12")),
                "Наименование микроорганизма",
            ] = "04. Acinetobacter baumannii"
            df.loc[
                df.POKAZATEL.str.endswith(("_13", "_14", "_15")),
                "Наименование микроорганизма",
            ] = "05. Enterococcus faecalis"
            df.loc[
                df.POKAZATEL.str.endswith(("_16", "_17", "_18")),
                "Наименование микроорганизма",
            ] = "06. Enterococcus faecium"
            df.loc[
                df.POKAZATEL.str.endswith(("_19", "_20", "_21")),
                "Наименование микроорганизма",
            ] = "07. Echerihia coli"
            df.loc[
                df.POKAZATEL.str.endswith(("_22", "_23", "_24")),
                "Наименование микроорганизма",
            ] = "08. другие Грам(+) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(("_25", "_26", "_27")),
                "Наименование микроорганизма",
            ] = "09. другие Грам(-) микроорганизмы"
            df.loc[
                df.POKAZATEL.str.endswith(("_28", "_29", "_30")),
                "Наименование микроорганизма",
            ] = "10. грибы рода Candida"

            df = df.pivot_table(
                index=[
                    "ORGANIZATION",
                    "Количество изолятов, выделенных из проб биологического материала пациентов",
                ],
                columns=["Наименование микроорганизма"],
                values=["VALUE"],
                aggfunc="first",
            ).stack(0)
            df = df.reset_index()
            del df["level_2"]

        dict_[key] = df

    filename = "/tmp/ismp_year.xlsx"

    with pd.ExcelWriter(filename, engine="xlsxwriter") as wb:
        for key, value in dict_.items():
            value.to_excel(wb, sheet_name=key, index=False, header=False, startrow=1)
            sheet = wb.sheets[key]

            cell_format = wb.book.add_format()
            # cell_format.set_font_color("white")
            cell_format.set_align("top")
            cell_format.set_font_size(11)
            cell_format.set_text_wrap()
            cell_format.set_bold()

            for col, name in enumerate(value.columns):
                try:
                    width = max(value[name].astype(str).map(len).max(), len(name))
                except:
                    width = 40

                width = {
                    width > 45: 45,
                    width < 20: 20,
                }.get(True, width)

                sheet.write(0, col, name, cell_format)
                sheet.set_column(0, col, width)
            sheet.autofilter(0, 0, value.shape[0], len(value.columns) - 1)

    return filename
