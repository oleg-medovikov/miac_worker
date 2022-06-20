import glob, datetime, os
import pandas as pd
from .put_excel_for_mo import put_excel_for_mo
from .put_svod_for_mo  import put_svod_for_mo

from clas import Dir

CHANGE_MO =[
[r'Больница №20 Поликлиническое отделение №42 (площадка Ленсовета)'
,r'СПб ГБУЗ "Городская больница №20"']
,[r'СПб ГБУЗ "Городская больница №40" площадка Пансионат "Заря"'
,r'СПб ГБУЗ "Городская больница №40"']
,[r'СПб ГБУЗ "Городская Александровская больница"'
,r'СПб ГБУЗ "Александровская больница"']
,[r'СПб ГБУЗ "Клиническая больница Святителя Луки"'
,r'СПб ГБУЗ Клиническая больница Святителя Луки']
,[r'СПб ГБУЗ "Городская больница Святой преподобномученицы Елизаветы"'
,r'СПб ГБУЗ "Елизаветинская больница"']
,[r'СПб ГБУЗ "Детская городская больница Святой Ольги"'
,r'СПб ГБУЗ "ДГБ Св. Ольги"']
,[r'СПб ГБУЗ "Детская городская клиническая больница №5 имени Нила Федоровича Филатова"'
,r'СПб ГБУЗ "ДГКБ №5 им. Н.Ф.Филатова"']
,[r'СПб ГКУЗ "Городская психиатрическая больница №3 им.И.И.Скворцова-Степанова"'
,r'СПб ГКУЗ "ГПБ №3 им. И.И.Скворцова-Степанова"']
,[r'СПб ГБУЗ "ДГМКЦ ВМТ им.К.А.Раухфуса"'
,r'СПБ ГБУЗ «ДГМКЦ ВМТ им. К.А.Раухфуса»']
,[r'СПб ГБУЗ "Центр по профилактике и борьбе со СПИД и инфекционными заболеваниями"'
,r'СПб ГБУЗ "Центр СПИД и инфекционных заболеваний"']
,[r'ФГБОУ ВО ПСПбГМУ им. И.П.Павлова" Минздрава России'
,r'ФГБОУ ВО ПСПбГМУ им. И.П.Павлова Минздрава России']
,[r'ФГБОУ ВО СЗГМУ им.И.И.Мечникова Минздрава России'
,r'ФГБОУ ВО СЗГМУ им. И.И. Мечникова Минздрава России']
,[r'ФГБУЗ «Клиническая больница №122 им.Л.Г.Соколова» ФМБА России'
,r'ФГБУ "СЗОНКЦ им.Л.Г.Соколова ФМБА России"']
,[r'СПб ГБУЗ "Введенская больница"'
,r'СПБ ГБУЗ "Введенская больница"']
,[r'СПб ГБУЗ "Психиатрическая больница №1 им.П.П.Кащенко"'
,r'СПб ГБУЗ "Санкт-Петербургская психиатрическая больница №1 им.П.П.Кащенко"']
,[r'ФГБОУ ВО "Санкт-Петербургский Государственный педиатрический медицинский университет Минздрава России"'
,r'ФГБОУ ВО СПбГПМУ Минздрава России']
,[r'СПб ГБУЗ "Госпиталь для ветеранов войн" площадка "ЛЕНЭКСПО"'
,r'СПб ГБУЗ "Госпиталь для ветеранов войн"']
,[r'ФГБОУ ВО СПБГПМУ МИНЗДРАВА РОССИИ'
,r'ФГБОУ ВО СПбГПМУ Минздрава России']
,[r'СПб ГБУЗ "Детская городская клиническая больница №5 имени Нила Федоровича Филатова"'
,r'СПб ГБУЗ "ДГКБ №5 им. Н.Ф.Филатова"']
,[r'СПб ГБУЗ "Городская многопрофильная больница №2"'
,r'СПб ГБУЗ "ГМПБ 2"']
,[r'СПб ГБУЗ "Клиническая инфекционная больница им. С.П. Боткина"'
,r'СПб ГБУЗ "Больница Боткина"']
    ]

S_org = [
'ФГБОУ ВО СЗГМУ им. И.И. Мечникова Минздрава России'
,'ФГБОУ ВО ПСПбГМУ им. И.П.Павлова Минздрава России'
,'СПб ГБУЗ "Городская больница №40"'
,'СПб ГБУЗ "Городская больница №20"'
,'СПб ГБУЗ "Николаевская больница"'
    ]

class my_except(Exception):
    pass

async def IVL():
    DATE = datetime.datetime.now().strftime('%Y_%m_%d')
    PATH = await Dir.get('path_robot')
    
    FILE_VP = PATH + '/Мониторинг_ВП.xlsx'
    if not os.path.exists( FILE_VP ):
        raise my_except("Нет файла 'Мониторинг_ВП.xlsx'")

    try:
        FILE_FR = glob.glob(PATH + '/[!~]*едеральный*15-00.csv')[0]
    except:
        raise my_except('Не найден трёхчасовой федеральный регистр')


    NAMES = ['Дата изменения РЗ','Медицинская организация'
            ,'Исход заболевания','ИВЛ','Вид лечения'
            ,'Субъект РФ','Диагноз']

    FR = pd.read_csv(
            FILE_FR,
            usecols = NAMES,
            sep=';',
            engine='python',
            encoding='utf-8')

    DATE_OTCH = pd.to_datetime(
            fr['Дата изменения РЗ'],
            format='%d.%m.%Y').max().date()

    del fr['Дата изменения РЗ']
    NAMES = ['mo','vp_zan','vp_ivl','cov_zan','cov_ivl']
    
    vp = pd.read_excel(
            FILE_VP,
            usecols = "A,I,L,Y,AB",
            header=7,
            names=NAMES)

    # Считаем числа в в федеральном регистре 
    zan1 = FR.loc[FR['Исход заболевания'].isnull() \
            & FR['Вид лечения'].isin(['Стационарное лечение']) \
            & FR['Субъект РФ'].isin(['г. Санкт-Петербург']) \
            & FR['Медицинская организация'].isin(S_org) \
            & (FR['Диагноз'].str.contains('J12.')\
            | fr['Диагноз'].str.contains('J18.') \
            | fr['Диагноз'].isin(['U07.1','U07.2']) )  ]

    zan1 ['Занятые койки'] = 1 
    zan1 = zan1.groupby(
            'Медицинская организация',
            as_index=False)['Занятые койки'].sum()

    zan2 = FR.loc[fr['Исход заболевания'].isnull() \
            & FR['Субъект РФ'].isin(['г. Санкт-Петербург']) \
            & ~FR['Медицинская организация'].isin(S_org) \
            & (FR['Диагноз'].str.contains('J12.') \
            | FR['Диагноз'].str.contains('J18.') \
            | FR['Диагноз'].isin(['U07.1','U07.2']) )  ]
    
    zan2 ['Занятые койки'] = 1 
    zan2 = zan2.groupby(
            'Медицинская организация',
            as_index=False)['Занятые койки'].sum()

    zan = pd.concat([zan1,zan2], ignore_index=True)

    ivl1 = FR.loc[fr['Исход заболевания'].isnull() \
            & FR['ИВЛ'].notnull() \
            & FR['Вид лечения'].isin(['Стационарное лечение']) \
            & FR['Медицинская организация'].isin(S_org) ]
    
    ivl1 ['ИВЛ'] = 1
    ivl1 = ivl1.groupby(
            'Медицинская организация',
            as_index=False)['ИВЛ'].sum()

    ivl2 = FR.loc[FR['Исход заболевания'].isnull() \
            & FR['ИВЛ'].notnull() \
            & ~FR['Медицинская организация'].isin(S_org) ]

    ivl2 ['ИВЛ'] = 1
    ivl2 = ivl2.groupby(
            'Медицинская организация',
            as_index=False)['ИВЛ'].sum()

    ivl = pd.concat([ivl1,ivl2], ignore_index=True)

    df = zan.merge(ivl,how='outer')

    df = df.fillna(0)

    vp = vp.fillna(0)
    # Меняем названия МО и сумируем строки 
    zamena = 'произошла замена строки '
    for i in range(len(vp)):
        vp.loc[i,'zan'] = vp.at[i,'vp_zan'] + vp.at[i,'cov_zan']
        vp.loc[i,'ivl'] = vp.at[i,'vp_ivl'] + vp.at[i,'cov_ivl']
        for bad,good in CHANGE_MO:
            if vp.loc[i,'mo'] == bad:
                vp.loc[i,'mo'] = good
                zamena += '\n ' + bad + ' на ' + good

    vp = vp.groupby('mo',as_index=False)['zan','ivl'].sum()
    vp.index = range(len(vp))

    # получаем отчёт по ИВЛ
    ivl_otchet = vp.merge(
            df,
            left_on='mo',
            right_on='Медицинская организация',
            how='left')
    del ivl_otchet ['mo']
    del ivl_otchet ['Занятые койки']
    del ivl_otchet ['zan']
    ivl_otchet = ivl_otchet.fillna(0)

    for i in range(len(ivl_otchet)):
        ivl_otchet.loc[i,'Разница'] = ivl_otchet.at[i,'ИВЛ'] - ivl_otchet.at[i,'ivl']

    ivl_otchet.rename(
            columns = { 'ivl':'ИВЛ из ежедневного отчёта',
                        'ИВЛ':'ИВЛ из Фед Регистра'},
            inplace = True)

    columnsTitles=['Медицинская организация',
                   'ИВЛ из ежедневного отчёта',
                   'ИВЛ из Фед Регистра',
                   'Разница']

    ivl_otchet = ivl_otchet[ivl_otchet['Медицинская организация'] != 0 ]
    ivl_otchet=ivl_otchet.reindex(columns=columnsTitles)

    ivl_otchet.index = range(1,len(ivl_otchet)+1)

    medorg_ivl_otchet = ivl_otchet['Медицинская организация'].unique()

    # получаем отчёт по койкам
    zan_otchet = vp.merge(
            df,
            left_on='mo',
            right_on='Медицинская организация',
            how='left')

    del zan_otchet ['mo']
    del zan_otchet ['ИВЛ']
    del zan_otchet['ivl']
    zan_otchet = zan_otchet.fillna(0)

    for i in range(len(zan_otchet)):
        zan_otchet.loc[i,'Разница'] = zan_otchet.at[i,'Занятые койки'] - zan_otchet.at[i,'zan']

    zan_otchet.rename(
            columns = {'zan':'Заняты койки из ежедневного отчёта',
                       'Занятые койки':'Койки из Фед Регистра'},
            inplace = True)
    
    columnsTitles=['Медицинская организация',
                   'Заняты койки из ежедневного отчёта',
                   'Койки из Фед Регистра',
                   'Разница']

    zan_otchet=zan_otchet.reindex(columns=columnsTitles)
    zan_otchet = zan_otchet[zan_otchet['Медицинская организация'] != 0 ]
    zan_otchet.index=range(1,len(zan_otchet)+1)

    medorg_zan_otchet = zan_otchet['Медицинская организация'].unique()

    PATH_OTC = await Dir.get('zam_svod') + '/сверка ИВЛ и занятые койки'
    FILE_OTCH = PATH_OTCH +'/'+ DATE_OTCH.strftime('%Y_%m_%d') + ' пациенты на ИВЛ новый.xlsx' 

    with pd.ExcelWriter( FILE_OTCH ) as writer:
        ivl_otchet.to_excel(writer,sheet_name='ИВЛ')
        zan_otchet.to_excel(writer,sheet_name='занятые койки')
    
    STAT_1 = await put_excel_for_mo(
            ivl_otchet,
            'Пациенты на ИВЛ',
            DATE_OTCH)
    STAT_2 = await put_excel_for_mo(
            zan_otchet,
            'Занятые койки',
            DATE_OTCH)
    
    return STAT_1 + ';' + STAT_2


