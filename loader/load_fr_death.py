import datetime, glob, openpyxl
import pandas as pd

from clas import Dir
from base import covid_insert, covid_exec

NAMES=[
'1', '2', '3', '4', '6', '7', '8', '9', '10',
'11', '12', '13', '14', '15', '16', '17', '18',
'19', '20', '21', '22','23', '24', '25', '26',
'27', '28', '29', '30', '31', '32', '33', '34',
'35', '36', '37', '38', '39', '40', '41', '42',
'43', '44', '45', '46', '47', '48', '49', '50',
'51', '52', '53'
    ]

class my_exept(Exception):
    pass

def excel_to_csv(file_excel):
    """Конвертация чтобы убрать ненужное форматирование"""
    import csv
    file_csv = file_excel[:-4] + 'csv'
    excel = openpyxl.load_workbook(file_excel)
    sheet = excel.active 
    col = csv.writer(open(file_csv, 'w',newline=""),delimiter=';')
    for r in sheet.rows: 
        col.writerow([cell.value for cell in r]) 
    return file_csv

def search_file():
    path = Dir.get('path_robot') + '/' + datetime.datetime.now().strftime("%Y_%m_%d")
    
    file_csv   = glob.glob(path + '/*Умершие пациенты*.csv')
    if len(file_csv) > 0:
        return file_csv[0]
    
    file_excel = glob.glob(path + '/*Умершие пациенты*.xlsx')
    if len(file_excel) > 0:
        return excel_to_csv( file_excel[0] )

    raise my_exept('Не найден файл умерших пациентов')



def load_fr_death():
    """Загрузка умерших пациентов"""
    
    FILE_CSV = search_file()
    
    for i in range(10):
        try:
            DF = pd.read_csv(
                FILE_CSV,
                header = i,
                usecols = NAMES,
                na_filter = False,
                dtype = str,
                delimiter=';',
                engine='python')
        except:
            continue
        else:
            break

    # Обрезаю слишком длинные строки
    DF = DF.apply(lambda x: x.loc[::].str[:255] )

    # Убираю Nan из таблицы
    DF = DF.apply(lambda x: x.loc[::].str.replace('nan','') )
    
    covid_insert(DF, 'cv_input_fr_d_all_2', 'dbo', False, 'replace')

    covid_exec("""
            EXEC   [dbo].[Insert_Table_cv_input_fr_d_all_2]
            EXEC   [dbo].[cv_from_d_all_to_d_covid]
            EXEC   [dbo].[cv_Load_FedReg_d_All]
            EXEC   [dbo].[cv_Load_FedReg_d_covid]
            """)

    return "34 отчёт по погибшим успешно загружен \n" + 'Файл: ' + FILE_CSV.rsplit('/',1)[-1]

