from datetime import datetime, timedelta
from pandas import ExcelWriter, to_numeric

from base import parus_sql

sql = """
SELECT
    --to_char(r.BDATE, 'DD.MM.YYYY') day,
    a.AGNNAME "медицинская организация",
    i.CODE pokazatel,
    ro.NUMB row_index ,
    CASE WHEN STRVAL  IS NOT NULL THEN STRVAL
        WHEN NUMVAL  IS NOT NULL THEN CAST(NUMVAL  AS varchar(30))
        WHEN DATEVAL IS NOT NULL THEN CAST(DATEVAL AS varchar(30))
        ELSE NULL END value
FROM PARUS.BLTBLVALUES v
INNER JOIN PARUS.BLTABLESIND si
on(v.BLTABLESIND = si.RN)
INNER JOIN PARUS.BALANCEINDEXES i
on(si.BALANCEINDEXES = i.RN)
INNER JOIN PARUS.BLTBLROWS ro
on(v.PRN = ro.RN)
INNER JOIN PARUS.BLSUBREPORTS s
on(ro.PRN = s.RN)
INNER JOIN PARUS.BLREPORTS r
on(s.PRN = r.RN)
INNER JOIN PARUS.AGNLIST a
on(r.AGENT = a.RN)
INNER JOIN PARUS.BLREPFORMED rd
on(r.BLREPFORMED = rd.RN)
INNER JOIN PARUS.BLREPFORM rf
on(rd.PRN = rf.RN)
WHERE rf.code = 'ДезинфСтерОбщ'
and i.CODE in (__pokazatel__)
"""
pokazatel = {
    "дезинфекция 1": [
        "dezinf_01",
        "dezinf_02",
        "dezinf_03",
        "dezinf_04",
        "dezinf_05",
        "dezinf_06",
        "dezinf_07",
        "dezinf_08",
        "dezinf_09",
        "dezinf_10",
    ],
    "дезинфекция 2": [
        "dezinf2_01",
        "dezinf2_02",
        "dezinf2_03",
        "dezinf2_04",
        "dezinf2_05",
        "dezinf2_06",
        "dezinf2_07",
        "dezinf2_08",
        "dezinf2_09",
        "dezinf2_10",
    ],
    "дезкамера": [
        "dezkam_01",
        "dezkam_02",
        "dezkam_03",
        "dezkam_04",
    ],
    "паровые": ["par_01", "par_02", "par_03", "par_04", "par_05", "par_06", "par_07"],
    "воздушные": ["vozd_01", "vozd_02", "vozd_03", "vozd_04", "vozd_05", "vozd_06"],
    "низкотемп": [
        "nizkotemp_01",
        "nizkotemp_02",
        "nizkotemp_03",
        "nizkotemp_04",
        "nizkotemp_05",
        "nizkotemp_06",
        "nizkotemp_07",
    ],
    "моечно-дез ИМН": [
        "moech_01",
        "moech_02",
        "moech_03",
        "moech_04",
        "moech_05",
        "moech_06",
    ],
    "моечно-дез эндоскоп": [
        "moeche_01",
        "moeche_02",
        "moeche_03",
        "moeche_04",
        "moeche_05",
        "moeche_06",
    ],
}

columns = {
    "dezinf_01": "01. Наименование дезинфектанта для химической стерилизации, дезинфекции высокого уровня эндоскопов",
    "dezinf_02": "02. Наименование активного действующего вещества",
    "dezinf_03": "03. Наименование дезинфектанта для дезинфекции наркозно-дыхательной аппаратуры, ИВЛ, кувезов",
    "dezinf_04": "04. Наименование активного действующего вещества",
    "dezinf_05": "05. Наименование дезинфектанта для дезинфекции и предстерилизационной очистки многоразового инструментария, в т.ч. хирургического",
    "dezinf_06": "06. Наименование активного действующего вещества",
    "dezinf_07": "07. Наименование дезинфектанта для дезинфекции поверхностей в помещениях, мебели, приборов и оборудования, санитарно-технического оборудования (текущая уборка)",
    "dezinf_08": "08. Наименование активного действующего вещества",
    "dezinf_09": "09. Наименование дезинфектанта для  дезинфекции поверхностей в помещениях, мебели, приборов и оборудования, санитарно-технического оборудования (генеральная уборка)",
    "dezinf_10": "10. Наименование активного действующего вещества",
    "dezinf2_01": "01. Наименование дезинфектанта для дезинфекции предметов ухода за больными",
    "dezinf2_02": "02. Наименование активного действующего вещества",
    "dezinf2_03": "03. Наименование антисептика  для  гигиенической антисептической обработки рук",
    "dezinf2_04": "04. Наименование активного действующего вещества",
    "dezinf2_05": "05. Наименование антисептика для хирургической антисептической обработки рук",
    "dezinf2_06": "06. Наименование активного действующего вещества",
    "dezinf2_07": "07. Наименование антисептика для обработки инъекционного поля",
    "dezinf2_08": "08. Наименование активного действующего вещества",
    "dezinf2_09": "09. Наименование антисептика для обработки операционного поля",
    "dezinf2_10": "10. Наименование активного действующего вещества",
    "dezkam_01": "1. Наименование дезкамеры",
    "dezkam_02": "2. Год начала эксплуатации дезкамеры",
    "dezkam_03": "3. Число комплектов ОБЩЕЕ",
    "dezkam_04": "4. Число комплектов, прошедших камерную обработку",
    "par_01": "1. Подразделение",
    "par_02": "2. Название в соответсвии с паспортом (полное)",
    "par_03": "3. Марка/ производитель",
    "par_04": "4. Год выпуска",
    "par_05": "5. Год начала эксплуатации",
    "par_06": "6. Год начала эксплуатации",
    "par_07": "7. Принцип действия",
    "vozd_01": "1. Подразделение",
    "vozd_02": "2. Название в соответсвии с паспортом (полное)",
    "vozd_03": "3. Марка/ производитель",
    "vozd_04": "4. Год выпуска",
    "vozd_05": "5. Год начала эксплуатации",
    "vozd_06": "6. Процент износа",
    "nizkotemp_01": "1. Подразделение",
    "nizkotemp_02": "2. Название в соответсвии с паспортом (полное)",
    "nizkotemp_03": "3. Марка/ производитель",
    "nizkotemp_04": "4. Год выпуска",
    "nizkotemp_05": "5. Год начала эксплуатации",
    "nizkotemp_06": "6. Процент износа",
    "nizkotemp_07": "7. Действующее начало",
    "moech_01": "1. Подразделение",
    "moech_02": "2. Название в соответсвии с паспортом (полное)",
    "moech_03": "3. Марка/ производитель",
    "moech_04": "4. Год выпуска",
    "moech_05": "5. Год начала эксплуатации",
    "moech_06": "6. Процент износа",
    "moeche_01": "1. Подразделение",
    "moeche_02": "2. Название в соответсвии с паспортом (полное)",
    "moeche_03": "3. Марка/ производитель",
    "moeche_04": "4. Год выпуска",
    "moeche_05": "5. Год начала эксплуатации",
    "moeche_06": "6. Процент износа",
}


def dezinfection_year():
    """"""
    START = (datetime.today() - timedelta(days=90)).strftime("%Y%m%d")
    STOP = (datetime.today() + timedelta(days=90)).strftime("%Y%m%d")
    dict_ = {}
    for key, value in pokazatel.items():
        # вставляем в запрос показатели и даты
        _sql = sql.replace("__pokazatel__", "".join("'" + _ + "', " for _ in value))
        _sql = _sql.replace("__start__", START)
        _sql = _sql.replace("__stop__", STOP)
        _sql = _sql.replace("', )", "')")

        df = parus_sql(_sql)

        df.POKAZATEL = df.POKAZATEL.map(columns)

        df = df.pivot_table(
            index=["медицинская организация", "ROW_INDEX"],
            columns=["POKAZATEL"],
            values=["VALUE"],
            aggfunc="first",
        ).stack(0)

        df = df.reset_index()
        if key == "дезкамера":
            df[columns.get("dezkam_04")] = to_numeric(df[columns.get("dezkam_04")])
            df[columns.get("dezkam_03")] = to_numeric(df[columns.get("dezkam_03")])
            df["5. Доля камерных обработок"] = (
                100 * df[columns.get("dezkam_04")] / df[columns.get("dezkam_03")]
            ).round()

        del df["ROW_INDEX"]
        del df["level_2"]
        dict_[key] = df

    # записываем в файл с форматированием
    filename = f"/tmp/Дезинфекция_общая_{datetime.now().year}.xlsx"
    with ExcelWriter(filename, engine="xlsxwriter") as wb:
        for key, value in dict_.items():
            value.to_excel(wb, sheet_name=key, index=False, header=False, startrow=1)
            sheet = wb.sheets[key]

            cell_format = wb.book.add_format()
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
