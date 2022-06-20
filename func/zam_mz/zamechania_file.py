import shutil,openpyxl
from base import covid_sql

SQL_NAMES = [
['no_snils.sql', 'Без СНИЛСа'],
['no_OMS.sql', 'Нет сведений ОМС'],
['bez_ishod.sql', 'Без исхода заболевания больше 30 дней'],
['net_dnevnik.sql','Нет дневниковых записей'],
['net_pad.sql', 'Нет ПАД'],
['neverni_vid_lecenia.sql','Неверный вид лечения'],
['bez_ambulat_level.sql', 'Нет амбулаторного этапа'],
['bez_ambulat_level_amb.sql', 'Нет амбулаторного этапа (Амб.)'],
['bez_ambulat_level_noMO.sql', 'Нет амбулаторного этапа (Без МО)']
    ]

async def zamechania_file():
    SQL = """
    SELECT max([Дата изменения РЗ]) as 'дата отчета'
        FROM robo.v_FedReg
    """
    DATE = covid_sql( SQL ).iat[0,0]

    SQL = open('func/zam_mz/sql/kolichestvo.sql', 'r')

    DF = covid_sql( SQL )

    for FILE, NAME in SQL_NAMES:
        SQL = open( 'func/zam_mz/sql/' + FILE, 'r').read()
        PART = covid_sql( SQL )
        PART = PART.groupby(
                by=["Медицинская организация"],
                as_index=False).size()

        PART.rename(columns={"size": NAME}, inplace=True)

        DF = DF.merge(
                PART,
                how = "left",
                left_on = 'Медицинская организация',
                right_on = 'Медицинская организация' )

    DF.fillna(0, inplace=True)

    del DF ['Уникальных пациентов']
    DF = DF.loc[~(DF['Медицинская организация'] == 'МО другого региона') ]
    DF.index = range(len(DF))

    
    NEW_FILE = "temp/Замечания_за_" + DATE.strftime('%Y-%m-%d') + ".xlsx"
    shutil.copyfile( 'help/Zamechania.xlsx',  NEW_FILE)

    wb = openpyxl.load_workbook( NEW_FILE )

    ws = wb['main']   
    PART = DF.copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)
   
    ws = wb['amb']   
    PART = DF.loc[DF['Тип организации'] == 'Амбулаторная' ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['amb_dist'] 
    PART = DF.loc[(DF['Тип организации'] == 'Амбулаторная' )\
            & ~(DF['Принадлежность'].isin([
                'комитет здравоохранения',
                'частные','федеральные']) ) ].copy()
    del PART ['Тип организации']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['amb_kz']   
    PART = DF.loc[(DF['Тип организации'] == 'Амбулаторная' )\
            & ( DF['Принадлежность'].isin([
                'комитет здравоохранения']) ) ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['amb_fed']   
    PART = DF.loc[(DF['Тип организации'] == 'Амбулаторная' )\
            & ( DF['Принадлежность'].isin([
                'федеральные']) ) ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['amb_ch']   
    PART = DF.loc[(DF['Тип организации'] == 'Амбулаторная' )\
            & ( DF['Принадлежность'].isin(['частные']) ) ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['stat']   
    PART = DF.loc[DF['Тип организации'] == 'Стационарная' ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['stat_dist']   
    PART = DF.loc[(DF['Тип организации'] == 'Стационарная' )\
            & ~(DF['Принадлежность'].isin([
                'комитет здравоохранения',
                'частные','федеральные']) ) ].copy()
    del PART ['Тип организации']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['stat_kz']   
    PART = DF.loc[(DF['Тип организации'] == 'Стационарная' )\
            & ( DF['Принадлежность'].isin([
                'комитет здравоохранения']) )  ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['stat_fed']
    PART = DF.loc[(DF['Тип организации'] == 'Стационарная' )\
            &  (DF['Принадлежность'].isin([
                'федеральные']) ) ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['stat_ch']   
    PART = DF.loc[(DF['Тип организации'] == 'Стационарная' )\
            & ( DF['Принадлежность'].isin(['частные']) ) ].copy()
    del PART ['Тип организации']
    del PART ['Принадлежность']
    rows = dataframe_to_rows(PART,index=False, header=False)
    for r_idx, row in enumerate(rows,5):
        for c_idx, value in enumerate(row, 7):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save( NEW_FILE )
 

    return NEW_FILE


