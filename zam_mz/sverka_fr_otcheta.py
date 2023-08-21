import glob
import pandas as pd
from datetime import datetime

from clas import Dir
from .put_excel_for_mo import put_excel_for_mo_2
from base import covid_sql


class my_except(Exception):
    pass


# замена названий
def change_MO_dict() -> dict:
    "возвращаем словарь заменяемых названий"
    sql = "SELECT lower(Bad_Name) as Bad_Name, Good_Name FROM Nsi.MO_Name"
    CHANGE_MO = {}
    df = covid_sql(sql)

    for _ in df.index:
        CHANGE_MO[df.at[_, 'Bad_Name']] = df.at[_, 'Good_Name']
    return CHANGE_MO


def sverka_fr_otcheta():
    "Это мы сверяем с выгрузкой 12:00"

    DATE_OTCH = datetime.now().strftime("%Y_%m_%d")
    MASK = Dir.get('path_robot') + '/' + DATE_OTCH + '/' \
        + 'Федеральный*[!ИАЦ]*12-00.csv'

    # Список больниц с поликлиниками
    POL_BOL = [
      'ФГБОУ ВО СЗГМУ им. И.И. Мечникова Минздрава России',
      'ФГБОУ ВО ПСПбГМУ им. И.П.Павлова Минздрава России',
      'СПб ГБУЗ "Городская больница №40"',
      'СПб ГБУЗ "Городская больница №20"',
      'СПб ГБУЗ "Николаевская больница"'
    ]

    # Дополнительные организации, которые нужно показать
    # просто записываю в пустые значения mo значения из Медицинская организация
    DOP_ORG = [
        'ЧУЗ «КБ «РЖД-МЕДИЦИНА» Г. С-ПЕТЕРБУРГ"',
        'ООО Ава-Петер',
        'ООО «Медицентр ЮЗ»',
        'ООО "ЦСМ "21 ВЕК"',
        'ООО "УЧАСТКОВЫЕ ВРАЧИ"',
        'АНО "Медицинский центр "Двадцать первый век"'
               ]

    try:
        FILE_FR = glob.glob(MASK)[0]
    except IndexError:
        raise my_except('Не найден двенадцатичасовой федеральный регистр')

    MASK = Dir.get('path_robot') + '/' + DATE_OTCH + '/' \
        + 'Поликлиники*.xlsx'

    try:
        FILE_VP = glob.glob(MASK)[0]
    except IndexError:
        raise my_except('Не найден файл Поликлиники.xlsx')

    # Читаем файлы
    names = ['mo', 'cov_il', 'cov_rec']
    VP = pd.read_excel(
            FILE_VP,
            usecols='A,C,U',
            header=5,
            names=names
            )

    VP = VP.loc[~VP.mo.isnull()]
    VP = VP.fillna(0)

    cols = [
       'Медицинская организация', 'Диагноз',
       'Дата исхода заболевания', 'Исход заболевания',
       'Вид лечения', 'УНРЗ'
    ]
    FR = pd.read_csv(
            FILE_FR,
            usecols=cols,
            sep=';',
            engine='python',
            encoding='utf-8'
            )

    # Меняем названия организаций
    CHANGE_MO = change_MO_dict()
    VP['mo'] = VP['mo'].str.lower().map(CHANGE_MO)
    FR['mo'] = FR['Медицинская организация'].str.lower().map(CHANGE_MO)
    POL_BOL = [CHANGE_MO.get(_.lower()) for _ in POL_BOL]

    # удаляем лишнее из ФР
    FR = FR.drop(
        FR[
            FR['mo'].isin(POL_BOL)
            & FR['Вид лечения'].isin(['Стационарное лечение', 'Карантин'])
            ].index
        )
    # считаем и сравниваем
    FR_IL = FR.loc[
        (FR['Диагноз'] == 'U07.1')
        & (FR['Исход заболевания'].isnull())
        ].groupby(
            'mo',
            as_index=False
        )['УНРЗ'].count().rename(columns={'УНРЗ': 'cov_il_fr'})

    FR_REC = FR.loc[
        (FR['Диагноз'] == 'U07.1')
        & (FR['Исход заболевания'].str.contains('Выздоровление'))
        ].groupby(
            'mo',
            as_index=False
        )['УНРЗ'].count().rename(columns={'УНРЗ': 'cov_rec_fr'})

    VP = VP.merge(FR_IL, how='left', on='mo')
    VP = VP.merge(FR_REC, how='left', on='mo')

    # VP = VP.set_index('mo')
    VP = VP.fillna(0)

    VP.loc[VP.mo == 'Всего', 'cov_il_fr'] = VP['cov_il_fr'].sum()
    VP.loc[VP.mo == 'Всего', 'cov_rec_fr'] = VP['cov_rec_fr'].sum()
    VP['delta_il'] = VP['cov_il'] - VP['cov_il_fr']
    VP['delta_rec'] = VP['cov_rec'] - VP['cov_rec_fr']
    VP.loc[VP.mo.isin(POL_BOL), 'mo'] = VP['mo'] + ' (амб.)'

    # разбиваем на части и переименовываем
    IL = VP[[
        'mo', 'cov_il', 'cov_il_fr', 'delta_il'
        ]].rename(columns={
            'mo': 'Медицинская организация',
            'cov_il': 'болеют ковид из ежедневного отчета',
            'cov_il_fr': 'ФР диагноз U07.1',
            'delta_il': 'Разница',
            })
    REC = VP[[
        'mo', 'cov_rec', 'cov_rec_fr', 'delta_rec'
        ]].rename(columns={
            'mo': 'Медицинская организация',
            'cov_rec': 'выздоровело от ковида из ежедневного отчета',
            'cov_rec_fr': 'ФР выздоровело от U07.1',
            'delta_rec': 'Разница',
            })

    PATH = Dir.get('sverka_fr_and_otcheta')

    FILE = PATH + '/' + DATE_OTCH + ' Поликлинники COVID.xlsx'
    with pd.ExcelWriter(FILE) as writer:
        IL.to_excel(writer, sheet_name='болеющие')
        REC.to_excel(writer, sheet_name='выздоровевшие')

    STAT_FILE = put_excel_for_mo_2(
        IL,
        REC,
        'Сверка ФР и ежедневного отчёта',
        'болеющие',
        'выздоровевшие',
        None
            )
    return STAT_FILE
