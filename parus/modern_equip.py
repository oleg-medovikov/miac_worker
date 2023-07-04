import shutil
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

names_1 = {
    '00': '1. Медицинские организации, оказывающие первичную медико-санитарную помощь (Всего):',
    '01': '1.01 Поликлиники для взрослых',
    '02': '1.02 Поликлиники для детей',
    '03': '1.03 Поликлиники, обслуживающие взрослое и детское население',
    '04': '1.04 Поликлинические отделения для взрослых',
    '05': '1.05 Поликлинические отделения для детей',
    '06': '1.06 Отделения общеврачебной практики',
    '07': '1.07 Врачебные амбулатории',
    '08': '1.08 Фельдшерско-акушерские пункты',
    '09': '1.09 Фельдшерские пункты',
    '10': '1.10 Центральные районные больницы',
    '11': '1.11 Районные больницы',
    '12': '1.12 Участковые больницы',
    }
names_2 = {
    '00': '1. Количество медицинского оборудования, необходимого в соответствии с утвержденными порядками оказания медицинской помощи в том числе:',
    '01': '1.1 эндоскопическое оборудование (эндоскопический комплекс)',
    '02': '1.2 флюорограф',
    '03': '1.3 маммограф',
    '04': '1.4 рентгеновский комплекс',
    '05': '1.5 компьютерный томограф',
    '06': '1.6 оборудование для ультразвуковой диагностики',
    '07': '1.7 оборудование для оснащения офтальмологического кабинета',
    '08': '1.8 оборудование для функциональной диагностики',
    '09': '1.9 магнитно-резонансный томограф',
}

cols_1 = ['03', '06', '09', '12', '13', '14', '17']
cols_2 = ['03', '06', '09', '10', '11']


def modern_equip():
    SQL_1 = open('parus/sql/modern_equip_1.sql', 'r').read()
    SQL_2 = open('parus/sql/modern_equip_2.sql', 'r').read()

    DF_1 = parus_sql(SQL_1)
    DF_2 = parus_sql(SQL_2)

    DF_1['row'] = DF_1['POKAZATEL'].str.split('_').str[1]
    DF_1['col'] = DF_1['POKAZATEL'].str.split('_').str[2]
    DF_1['row'] = DF_1['row'].map(names_1)

    DF_2['row'] = DF_2['POKAZATEL'].str.split('_').str[1]
    DF_2['col'] = DF_2['POKAZATEL'].str.split('_').str[2]
    DF_2['row'] = DF_2['row'].map(names_2)

    DF_1_all = DF_1.pivot_table(index=['ORGANIZATION', 'row'], columns=['col'], values='VALUE', aggfunc='first')
    DF_1_all.index.names = [None, None]
    DF_1_svd = DF_1_all[cols_1]
    DF_1_svd.index.names = [None, None]
    DF_1_sum = DF_1.pivot_table(index=['row'], columns=['col'], values='VALUE', aggfunc='sum')[cols_1].reset_index()

    DF_2_all = DF_2.pivot_table(index=['ORGANIZATION', 'row'], columns=['col'], values='VALUE', aggfunc='first')
    DF_2_all.index.names = [None, None]
    DF_2_svd = DF_2_all[cols_2]
    DF_2_svd.index.names = [None, None]
    DF_2_sum = DF_2.pivot_table(index=['row'], columns=['col'], values='VALUE', aggfunc='sum')[cols_2].reset_index()

    DATE = DF_1['DAY'].max()
    FILE = f'/tmp/Модернизация_оснащения_за_{DATE}.xlsx'
    shutil.copyfile('help/modern_equip.xlsx', FILE)

    wb = openpyxl.load_workbook(FILE)

    WRITE = {
        'ЗДАНИЯ':            (DF_1_all, 3, 1, True),
        'ОБОРУДОВАНИЕ':      (DF_2_all, 3, 1, True),
        'Свод зд мо':        (DF_1_svd, 2, 1, True),
        'Свод об мо':        (DF_2_svd, 2, 1, True),
        'Свод здания':       (DF_1_sum, 3, 1, False),
        'Свод оборудование': (DF_2_sum, 3, 1, False),
    }

    for key, value in WRITE.items():
        ws = wb[key]
        rows = dataframe_to_rows(value[0], index=value[3], header=False)
        for r_idx, row in enumerate(rows, value[1]):
            for c_idx, val in enumerate(row, value[2]):
                ws.cell(row=r_idx, column=c_idx, value=val)

    wb.save(FILE)

    return FILE
