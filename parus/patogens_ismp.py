from datetime import datetime, timedelta
from typing import NewType
from base import parus_sql
from pandas import to_numeric


def patogens_ismp():
    """
    Захватова. квартальный отчет по ИСМП
    это возбудители инфекции из-за медицинской помощи
    """

    # свод случаев  ИСМП
    SQL = open("parus/sql/patogens_ismp_1.sql", "r").read()

    DF = parus_sql(SQL)
    DATE = DF.at[0, "BDATE"].strftime("%d_%m_%Y")

    names = {
        "1_01_001": "Численность пользованных пациентов в стационаре в отчетном периоде",
        "1_01_002": "Кол-во случаев ИСМП (всего)",
        "1_01_003": "Кол-во случаев  ИОХВ",
        "1_01_004": "Кол-во операций ",
        "1_01_005": "Кол-во внутрибольничных случаев  ИНДП (всего) ",
        "1_01_006": "в том числе кол-во случаев ИВЛ-ассоциированных ИНДП",
        "1_01_007": "Кол-во ИВЛ-дней",
        "1_01_008": "Кол-во внутрибольничных случаев ИКР (всего)",
        "1_01_009": "в том числе кол-во случаев катетер-ассоциированных ИКР (КАИК)",
        "1_01_010": "Кол-во сосудистых катетеро-дней",
        "1_01_011": "Кол-во случаев  ИСМП, связанных с применением эндоскоп. методов исследования",
        "1_01_012": "Кол-во эндоск. исследований",
        "1_01_013": "Кол-во внутрибольничных случаев ИМВП (всего)",
        "1_01_014": "в том числе кол-во случаев  катетер-ассоциированных ИМВП",
        "1_01_015": "Кол-во мочевых катетеро-дней",
        "1_01_016": "Кол-во случаев внутрибольничных постинъекционных инфекций ",
        "1_01_017": "Кол-во внутрибольничных случаев ИСМП, связанных с переливанием крови и ее препаратов",
        "1_01_018": "Кол-во переливаний крови и ее препаратов",
        "1_01_019": "Кол-во случаев ИСМП родильниц",
        "1_01_020": "Кол-во родов",
        "1_01_021": "Кол-во случаев  ИСМП новорожденных",
        "1_01_022": "Численность новорожденных",
        "1_01_023": "Кол-во случаев  ВУИ новорожденных",
        "1_01_024": "Кол-во внутрибольничных случаев ОКИ",
        "1_01_025": "Кол-во внутрибольничных случаев ВКИ",
        "1_01_026": "Кол-во случаев ИСМП у мед.работников",
        "1_01_027": "Кол- во мед.работников",
        "s_001": "Формы ИСМП у мед.работников (указать)",
        "1_01_028": "Кол-во случаев прочих ИСМП",
        "s_002": "Формы прочих ИСМП (указать)",
        "1_01_029": "Кол-во вспышек ИСМП",
        "s_003": "Комментарии к вспышке (указать нозологическую группу, количество пострадавших)",
        "1_01_030": "Численность умерших от ИСМП",
    }

    DF = DF.pivot_table(
        index=["ORGANIZATION"], columns=["POKAZATEL"], values=["VALUE"], aggfunc="first"
    ).stack(0)
    for name in names.keys():
        if name not in DF.columns:
            DF[name] = None
    DF = DF[names.keys()]
    DF.rename(columns=names, inplace=True)

    NEW_NAME_1 = "/tmp/" + DATE + "_свод_случаев_ИСМП.xlsx"

    DF.to_excel(NEW_NAME_1)

    # вспышки_ИнфЗаб
    SQL = open("parus/sql/patogens_ismp_2.sql", "r").read()

    DF = parus_sql(SQL)
    DATE = DF.at[0, "BDATE"].strftime("%d_%m_%Y")

    names = {
        "s_001": "Форма ИСМП",
        "i_z_01": "Профиль МО",
        "1_01_001": "Численность пострадавших",
        "s_002": "Возбудители ИСМП",
        "s_003": "Фено (гено)-тип",
        "1_01_002": "Кол-во групп АМП, используемых для типирования выделенных возбудителей ИСМП",
        "i_z_02": "в том числе наименование групп АМП, к представителям которых выделенные возбудители ИСМП резистентны",
        "1_01_003": "Кол-во групп дезинфекционных средств (по действующему веществу) использовали для типирования выделенных возбудителей ИСМП",
        "i_z_03": "в том числе наименование групп дезинфектантов, к которым выделенные возбудители ИСМП резистентны",
        "s_004": "Источник ИСМП",
        "s_005": "Факторы передачи",
        "1_01_004": "Длительность вспышки (в днях)",
        "1_01_005": "Количество летальных исходов",
    }

    DF = DF.pivot_table(
        index=["ORGANIZATION", "AGN_COMMENT"],
        columns=["POKAZATEL"],
        values=["VALUE"],
        aggfunc="first",
    ).stack(0)

    for name in names.keys():
        if name not in DF.columns:
            DF[name] = None

    DF = DF[names.keys()]
    DF.rename(columns=names, inplace=True)

    NEW_NAME_2 = "/tmp/" + DATE + "_вспышки_ИнфЗаб.xlsx"

    DF.to_excel(NEW_NAME_2)

    # Возбудители ИСМП
    SQL = open("parus/sql/patogens_ismp_3.sql", "r").read()

    DF = parus_sql(SQL)
    DATE = DF.at[0, "BDATE"].strftime("%d_%m_%Y")

    DF.loc[DF.POKAZATEL.str.startswith("7_01_"), "COLUMN"] = "J"
    DF.loc[DF.POKAZATEL.str.startswith("7_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("7_01_"), "POKAZATEL"]
        .str.replace("7_01_", "")
        .str.replace("013", "010")
        .str.replace("014", "011")
        .str.replace("015", "012")
        .str.replace("016", "013")
    )
    DF.loc[DF.POKAZATEL.str.startswith("8_01_"), "COLUMN"] = "K"
    DF.loc[DF.POKAZATEL.str.startswith("8_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("8_01_"), "POKAZATEL"]
        .str.replace("8_01_", "")
        .str.replace("013", "010")
        .str.replace("014", "011")
        .str.replace("015", "012")
        .str.replace("016", "013")
    )
    DF.loc[DF.POKAZATEL.str.startswith("10_01_"), "COLUMN"] = "M"
    DF.loc[DF.POKAZATEL.str.startswith("10_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("10_01_"), "POKAZATEL"]
        .str.replace("10_01_", "")
        .str.replace("013", "010")
        .str.replace("014", "011")
        .str.replace("015", "012")
        .str.replace("016", "013")
    )
    DF.loc[DF.POKAZATEL.str.startswith("11_01_"), "COLUMN"] = "N"
    DF.loc[DF.POKAZATEL.str.startswith("11_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("11_01_"), "POKAZATEL"]
        .str.replace("11_01_", "")
        .str.replace("013", "010")
        .str.replace("014", "011")
        .str.replace("015", "012")
        .str.replace("016", "013")
    )

    DF.loc[DF.POKAZATEL.str.startswith("19_01_"), "COLUMN"] = "C"
    DF.loc[DF.POKAZATEL.str.startswith("19_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("19_01_"), "POKAZATEL"].str.replace(
            "19_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("ICMP"), "COLUMN"] = "D"
    DF.loc[DF.POKAZATEL.str.startswith("ICMP"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("ICMP"), "POKAZATEL"].str.replace("ICMP", "")
    )
    DF.loc[DF.POKAZATEL.str.startswith("2_01_"), "COLUMN"] = "E"
    DF.loc[DF.POKAZATEL.str.startswith("2_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("2_01_"), "POKAZATEL"].str.replace(
            "2_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("3_01_"), "COLUMN"] = "F"
    DF.loc[DF.POKAZATEL.str.startswith("3_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("3_01_"), "POKAZATEL"].str.replace(
            "3_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("4_01_"), "COLUMN"] = "G"
    DF.loc[DF.POKAZATEL.str.startswith("4_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("4_01_"), "POKAZATEL"].str.replace(
            "4_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("5_01_"), "COLUMN"] = "H"
    DF.loc[DF.POKAZATEL.str.startswith("5_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("5_01_"), "POKAZATEL"].str.replace(
            "5_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("6_01_"), "COLUMN"] = "I"
    DF.loc[DF.POKAZATEL.str.startswith("6_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("6_01_"), "POKAZATEL"].str.replace(
            "6_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "COLUMN"] = "L"
    DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "POKAZATEL"].str.replace(
            "9_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("12_01_"), "COLUMN"] = "O"
    DF.loc[DF.POKAZATEL.str.startswith("12_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("12_01_"), "POKAZATEL"].str.replace(
            "12_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("13_01_"), "COLUMN"] = "P"
    DF.loc[DF.POKAZATEL.str.startswith("13_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("13_01_"), "POKAZATEL"].str.replace(
            "13_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("14_01_"), "COLUMN"] = "Q"
    DF.loc[DF.POKAZATEL.str.startswith("14_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("14_01_"), "POKAZATEL"].str.replace(
            "14_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("15_01_"), "COLUMN"] = "R"
    DF.loc[DF.POKAZATEL.str.startswith("15_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("15_01_"), "POKAZATEL"].str.replace(
            "15_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("16_01_"), "COLUMN"] = "S"
    DF.loc[DF.POKAZATEL.str.startswith("16_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("16_01_"), "POKAZATEL"].str.replace(
            "16_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("17_01_"), "COLUMN"] = "T"
    DF.loc[DF.POKAZATEL.str.startswith("17_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("17_01_"), "POKAZATEL"].str.replace(
            "17_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("s_ICMP"), "COLUMN"] = "U"
    DF.loc[DF.POKAZATEL.str.startswith("s_ICMP"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("s_ICMP"), "POKAZATEL"].str.replace(
            "s_ICMP", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("18_01_"), "COLUMN"] = "V"
    DF.loc[DF.POKAZATEL.str.startswith("18_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("18_01_"), "POKAZATEL"].str.replace(
            "18_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("s_1"), "COLUMN"] = "W"
    DF.loc[DF.POKAZATEL.str.startswith("s_1"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("s_1"), "POKAZATEL"].str.replace("s_1", "")
    )

    row = {
        1: "01. Инфекции в области хирургического вмешательства (ИОХВ)",
        2: "02. Инфекции нижних дыхательных путей (ИНДП)",
        3: "03. ИВЛ-ассоциированные ИНДП",
        4: "04. Инфекции кровотока (ИК)",
        5: "05. Катетер-ассоциированные инфекции кровотока (КАИК)",
        6: "06. ИСМП, связанные с применением эндоскопических методов исследования",
        7: "07. Инфекции мочевыводящих путей (ИМВП)",
        8: "08. Катетер-ассоциированные ИМВП",
        9: "09. Постинъекционные инфекции",
        10: "10. ИСМП, связанные с переливанием крови и препаратов крови",
        11: "11. ИСМП родильниц",
        12: "12. ИСМП новорожденных",
        13: "13. ВУИ новорожденных",
    }

    column = {
        "C": "C. Кол-во случаев ИСМП данной формы  (всего)",
        "D": "D. Численность пациентов с ИСМП данной формы (всего)",
        "E": "E. в том числе пациентов, материал которых исследован на возбудителей ИСМП",
        "F": "F. Кол-во проб материала пациентов с ИСМП данной формы (всего)",
        "G": "G. в том числе проб, из которых выделены возбудители ИСМП",
        "H": "H. Всего выделено возбудителей ИСМП (всего штаммов)",
        "I": "I. Кол-во штаммов S.aureus",
        "J": "J. Кол-во штаммов S.epidermidis",
        "K": "K. Кол-во штаммов Klebsiella spp.",
        "L": "L. Кол-во штаммов Acinetobacter spp.",
        "M": "M. Кол-во штаммов P.aeruginosa",
        "N": "N. Кол-во штаммов Enterococcus spp.",
        "O": "O. Кол-во штаммов Proteus spp.",
        "P": "P. Кол-во штаммов E.coli",
        "Q": "Q. Кол-во штаммов других Грам (+) микроорганизмов",
        "R": "R. Кол-во штаммов других Грам (-) микроорганизмов",
        "S": "S. Кол-во штаммов грибов",
        "T": "T. Кол-во штаммов других микроорганизмов",
        "U": "U. Комментарии (расписать другие микроорганизмы и количество штаммов)",
        "V": "V. Кол-во  ассоциаций",
        "W": "W. Комментарии (расписать виды микроорганизмов в ассоциации и количество штаммов)",
    }

    DF["ROW"] = DF["ROW"].map(row)
    DF["COLUMN"] = DF["COLUMN"].map(column)

    DF = DF.pivot_table(
        index=["ORGANIZATION", "ROW"],
        columns=["COLUMN"],
        values=["VALUE"],
        aggfunc="first",
    ).stack(0)

    NEW_NAME_3 = "/tmp/" + DATE + "_Возбудители_ИСМП.xlsx"

    DF.to_excel(NEW_NAME_3)

    # Чув. к воз. ИСМП
    SQL = open("parus/sql/patogens_ismp_4.sql", "r").read()

    DF = parus_sql(SQL)
    DATE = DF.at[0, "BDATE"].strftime("%d_%m_%Y")

    DF.loc[DF.POKAZATEL.str.startswith("1_01_"), "COLUMN"] = "C"
    DF.loc[DF.POKAZATEL.str.startswith("1_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("1_01_"), "POKAZATEL"].str.replace(
            "1_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("2_01_"), "COLUMN"] = "D"
    DF.loc[DF.POKAZATEL.str.startswith("2_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("2_01_"), "POKAZATEL"].str.replace(
            "2_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("3_01_"), "COLUMN"] = "E"
    DF.loc[DF.POKAZATEL.str.startswith("3_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("3_01_"), "POKAZATEL"].str.replace(
            "3_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("4_01_"), "COLUMN"] = "F"
    DF.loc[DF.POKAZATEL.str.startswith("4_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("4_01_"), "POKAZATEL"].str.replace(
            "4_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("3ICMP"), "COLUMN"] = "G"
    DF.loc[DF.POKAZATEL.str.startswith("3ICMP"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("3ICMP"), "POKAZATEL"].str.replace(
            "3ICMP", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("32ICMP"), "COLUMN"] = "H"
    DF.loc[DF.POKAZATEL.str.startswith("32ICMP"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("32ICMP"), "POKAZATEL"].str.replace(
            "32ICMP", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("7_01_"), "COLUMN"] = "I"
    DF.loc[DF.POKAZATEL.str.startswith("7_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("7_01_"), "POKAZATEL"].str.replace(
            "7_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("8_01_"), "COLUMN"] = "J"
    DF.loc[DF.POKAZATEL.str.startswith("8_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("8_01_"), "POKAZATEL"].str.replace(
            "8_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "COLUMN"] = "K"
    DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "POKAZATEL"].str.replace(
            "9_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "COLUMN"] = "K"
    DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("9_01_"), "POKAZATEL"].str.replace(
            "9_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("10_01_"), "COLUMN"] = "L"
    DF.loc[DF.POKAZATEL.str.startswith("10_01_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("10_01_"), "POKAZATEL"].str.replace(
            "10_01_", ""
        )
    )
    DF.loc[DF.POKAZATEL.str.startswith("s_2400_"), "COLUMN"] = "L"
    DF.loc[DF.POKAZATEL.str.startswith("s_2400_"), "ROW"] = to_numeric(
        DF.loc[DF.POKAZATEL.str.startswith("s_2400_"), "POKAZATEL"].str.replace(
            "s_2400_", ""
        )
    )

    row = {
        1: "01. Инфекции в области хирургического вмешательства (ИОХВ)",
        2: "02. Инфекции нижних дыхательных путей (ИНДП)",
        3: "03. ИВЛ-ассоциированные ИНДП",
        4: "04. Инфекции кровотока (ИК)",
        5: "05. Катетер-ассоциированные инфекции кровотока (КАИК)",
        6: "06. ИСМП, связанные с применением эндоскопических методов исследования",
        7: "07. Инфекции мочевыводящих путей (ИМВП)",
        8: "08. Катетер-ассоциированные ИМВП",
        9: "09. Постинъекционные инфекции",
        10: "10. ИСМП, связанные с переливанием крови и препаратов крови",
        11: "11. ИСМП родильниц",
        12: "12. ИСМП новорожденных",
        13: "13. ВУИ новорожденных",
    }

    column = {
        "C": "C. Кол-во штаммов возбудителей ИСМП (всего штаммов)",
        "D": "D. Кол-во штаммов с определением устойчивости к АМП",
        "E": "E. Кол-во штаммов с определением устойчивости к дез.средствам",
        "F": "F. Кол-во штаммов панрезистентных микроорганизмов",
        "G": "G. Кол-во штаммов MRSA",
        "H": "H. Кол-во штаммов VRE",
        "I": "I. Кол-во штаммов BLRS",
        "J": "J. Кол-во штаммов, устойчивых к ЧАС",
        "K": "K. Кол-во штаммов, устойчивых к гуанидинам",
        "L": "L. Кол-во штаммов, устойчивых к дезсредствам других групп",
        "M": "M. Комментарии (расписать к каким группам дезсредств и количество штаммов)",
    }

    DF["ROW"] = DF["ROW"].map(row)
    DF["COLUMN"] = DF["COLUMN"].map(column)

    DF = DF.pivot_table(
        index=["ORGANIZATION", "ROW"],
        columns=["COLUMN"],
        values=["VALUE"],
        aggfunc="first",
    ).stack(0)

    NEW_NAME_4 = "/tmp/" + DATE + "_Чувствительность_к_возбудителям_ИСМП.xlsx"

    DF.to_excel(NEW_NAME_4)

    return NEW_NAME_1 + ";" + NEW_NAME_2 + ";" + NEW_NAME_3 + ";" + NEW_NAME_4
