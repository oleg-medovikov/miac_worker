import glob, os, datetime, shutil
import pandas as pd

from clas import Dir
from base import covid_insert, covid_exec, covid_sql


NAMES =[
'№ п/п', 'Номер свидетельства о смерти', 'Дата выдачи',
'Взамен', 'Категория МС', 'Фамилия', 'Имя', 'Отчество',
'Пол', 'Дата рождения','Дата смерти', 'Возраст', 'Страна',
'Субъект', 'Район', 'Город', 'Населенный пункт',
'Элемент планировочной структуры','Район СПБ', 'Улица', 'Дом',
'Корпус', 'Строение', 'Квартира', 'Страна смерти',  'Субъект смерти',
'Район смерти','Город смерти', 'Населенный пункт смерти',
'Элемент планировочной структуры смерти', 'Район СПБ смерти',
'Улица смерти', 'Дом смерти','Корпус смерти', 'Строение смерти',
'Квартира смерти', 'Место смерти', 'Код МКБ-10 а',
'Болезнь или состояние, непосред приведшее к смерти','Код МКБ-10 б',
'Патол. состояние, кот. привело к указанной причине', 'Код МКБ-10 в',
'Первоначальная причина смерти', 'Код МКБ-10 г',
'Внешняя причина при травмах и отравлениях', 'Код II-1',
'Прочие важные состояния', 'Код МКБ-10 а(д)',
'Основное заболевание плода или ребенка','Код МКБ-10 б(д)',
'Другие заболевания плода или ребенка', 'Код МКБ-10 в(д)',
'Основное заболевание матери', 'Код МКБ-10 г(д)',
'Другие заболевания матери', 'Код МКБ-10 д(д)',
'Другие обстоятельства мертворождения', 'Установил причины смерти',
'Адрес МО', 'Краткое наименование', 'Осмотр трупа', 'Записи в мед.док.',
'Предшествующего наблюдения','Вскрытие', 'Статус МС', 'Дубликат',
'Испорченное', 'Напечатано', 'в случае смерти результате ДТП'
    ]
class my_except(Exception):
    pass

def vigruska_death_5_oclock():
    # Путь до файла УМСРС за день
    DATE = (datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y_%m_%d")
    PATH = Dir.get('covi') + '/' + DATE

    FILE = glob.glob(PATH + r'\*УМСРС*.xlsx')

    if len( FILE ) == 0:
        raise my_except('Файлик УМСРС не найден!')

    FILE = FILE[0]

    DF = pd.read_excel(
            FILE,
            sheet_name = 'COVID_оснв',
            header = 10,
            usecols=NAMES,
            dtype=str)

    """Названия колонок слишком сложные, чтобы их загрузить в базу
    упрощаем до простых номеров 1,2,3..."""

    DF.columns = range(len(DF.columns))

    covid_insert( DF, 'cv_input_umsrs_now_day', 'dbo', False, 'replace' )

    covid_exec( "EXEC   [dbo].[Insert_Table_cv_umsrs_now_day_2]" )

    SVERKA_1 = covid_sql("select * from dbo.v_Report_for_KZ_and_MO_Dead_Compare_At_All")
    SVERKA_2 = covid_sql("select * from dbo.v_Report_for_KZ_and_MO_Dead_Compare_At_All_2")
    SVERKA_3 = covid_sql("select * from v_Report_for_MO_Dead_Compare_At_All")

    DATE = (datetime.datetime.today() + datetime.timedelta(days=1)).strftime("%Y.%m.%d")

    FILES = glob.glob( PATH + '\[!Копия]*.xlsx')

    # Удаляем старые файлы, если они есть
    for file in FILES:
	    try:
		    os.remove(file)
	    except PermissionError:
		    pass

    with pd.ExcelWriter(PATH + '/' + DATE + '_Сверка_с_ФР.xlsx') as writer:
	    SVERKA_1.to_excel(writer,index=False)

    with pd.ExcelWriter(PATH + '/' + DATE + '_COVID_Умершие.xlsx') as writer:
	    SVERKA_2.to_excel(writer,index=False)

    MOs = SVERKA_3['Наименование МО'].unique()

    for mo in MOs:
	    otchet = SVERKA_3[ SVERKA_3 ['Наименование МО'] == mo ]
	    otchet.index = range(len(otchet))
        MO_FILE = PATH + '/'+ DATE + '_COVID_Умершие_' + mo.replace('"','') + '.xlsx'
	    with pd.ExcelWriter( MO_FILE ) as writer:
		    otchet.to_excel(writer,index=False)
        
        MO_DIR = Dir.get('УМСРС '+ mo )
        string = ''
        if MO_DIR is not None:
            shutil.move(MO_FILE, MO_DIR + MO_FILE.rsplit('/',1)[-1]
        else:
            string += '\n' + mo
    
    mess = "Вечерняя обработка УМСРС закончена. "
    if string != '':
        mess += '\n Не найдены директории для организаций: ' + string

    return mess

