from datetime import datetime, timedelta
import shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

class my_except(Exception):
    pass

FILES = [
    'parus/sql/covid_40_exit.sql',
    'parus/sql/covid_40_spytnic.sql',
    'parus/sql/covid_40_spytnic_old.sql',
    'parus/sql/covid_40_epivak.sql',
    'parus/sql/covid_40_epivak_old.sql',
    'parus/sql/covid_40_covivak.sql',
    'parus/sql/covid_40_covivak_old.sql',
    'parus/sql/covid_40_revac.sql',
    'parus/sql/covid_40_revac_old_new.sql',
    'parus/sql/covid_40_light.sql',
    'parus/sql/covid_40_light_old.sql'
        ]

def svod_40_covid_19():
    sql = open(FILES[0],'r').read()
    MO = parus_sql(sql)

    def change_sql(FILE : str, MO ):
        """Меняем запрос, добавляя в него выбывшие организации"""
        sql = open(FILE, 'r').read()
        if len(MO) == 0:
            return sql
        
        MO_str = ''

        for _ in MO['ORG'].unique():
            MO_str += "'" + _ + "',"

        MO_str = MO_str[:-1]


        if 'old' in FILE:
            string = f"\t\t\tand ( ( r.BDATE = trunc(SYSDATE) - 2  and a.AGNNAME not in ( {MO_str} ) )"
            for i in range(len(MO)):
                string += f"\n\t\t\tOR(r.BDATE = TO_DATE('{MO.at[i,'DAY']}','DD.MM.YYYY') - 1  and a.AGNNAME = '{MO.at[i,'ORG']}' ) "
            string += ')'
        else:
            string = f"\t\t\tand (( r.BDATE = trunc(SYSDATE) - 1 and a.AGNNAME not in ({MO_str} ) )"
            for i in range(len(MO)):
                string += f"\n\t\t\tOR(r.BDATE = TO_DATE('{MO.at[i,'DAY']}','DD.MM.YYYY') and a.AGNNAME = '{MO.at[i,'ORG']}' ) "
            string += ')'
        
        for  line in sql.split('\n'):
            if 'trunc' in line:
                sql = sql.replace(line, string)
        
        with open('temp/' + FILE.rsplit('/')[-1], 'w') as f:
            f.write(sql)

        return sql
    

    try:
        sput = parus_sql( change_sql( FILES[1], MO )) 
    except Exception as e:
        raise my_except('Сломанный запрос sput' + '\n' + str(e))
    try:
        sput_old = parus_sql( change_sql( FILES[2], MO ))
    except:
        raise my_except('Сломанный запрос sput_old')
    try:
        epivak = parus_sql( change_sql ( FILES[3], MO))
    except:
        raise my_except('Сломанный запрос epivak')
    try:
        epivak_old = parus_sql( change_sql( FILES[4], MO))
    except:
        raise my_except('Сломанный запрос epivak_old')
    try:
        covivak = parus_sql( change_sql( FILES[5], MO))
    except:
        raise my_except('Сломанный запрос covivak')
    try:
        covivak_old  = parus_sql( change_sql( FILES[6], MO))
    except:
        raise my_except('Сломанный запрос covivak_old')
    try:
        revac = parus_sql( change_sql( FILES[7], MO))
    except:
        raise my_except('Сломанный запрос revac')
    try:
        revac_old = parus_sql( change_sql( FILES[8], MO ))
    except:
        raise my_except('Сломанный запрос revac_old')
    try:
        light = parus_sql( change_sql( FILES[9], MO ))
    except:
        raise my_except('Сломанный запрос light')
    try:
        light_old = parus_sql( change_sql( FILES[10], MO ))
    except:
        raise my_except('Сломанный запрос light_old')
    
    #sput        = sput.loc[~sput[sput.columns[5]].isnull()]
    #sput_old    = sput_old.loc[~sput_old[sput_old.columns[5]].isnull()]
    #epivak      = epivak.loc[~epivak[epivak.columns[5]].isnull()]
    #epivak_old  = epivak_old.loc[~epivak_old[epivak_old.columns[5]].isnull()]
    #covivak     = covivak.loc[~covivak[covivak.columns[5]].isnull()]
    #covivak_old = covivak_old.loc[~covivak_old[covivak_old.columns[5]].isnull()]
    #revac       = revac.loc[~revac[revac.columns[6]].isnull()]
    #revac_old   = revac_old.loc[~revac_old[revac_old.columns[6]].isnull()]
    #light       = light.loc[~light[light.columns[5]].isnull()]
    #light_old   = light_old.loc[~light_old[light_old.columns[5]].isnull()]
    

    del sput ['ORGANIZATION']
    del sput_old ['ORGANIZATION']
    del epivak ['ORGANIZATION']
    del epivak_old ['ORGANIZATION']
    del covivak ['ORGANIZATION']
    del covivak_old ['ORGANIZATION']
    #del revac ['INDX']    
    #del revac_old ['INDX']
    del light ['ORGANIZATION']
    del light_old ['ORGANIZATION']

    #sput.drop_duplicates(keep='first', inplace=True)
    #sput_old.drop_duplicates(keep='first', inplace=True)
    #epivak.drop_duplicates(keep='first', inplace=True)
    #epivak_old.drop_duplicates(keep='first', inplace=True)
    #covivak.drop_duplicates(keep='first', inplace=True)
    #covivak_old.drop_duplicates(keep='first', inplace=True)
    #revac.drop_duplicates(keep='first', inplace=True)
    #revac_old.drop_duplicates(keep='first', inplace=True)
    #light.drop_duplicates(keep='first', inplace=True)
    #light_old.drop_duplicates(keep='first', inplace=True)

    revac = revac.loc[revac['TIP'] == 'Медицинская организация']
    revac_old = revac_old.loc[revac_old['TIP'] == 'Медицинская организация']

    date_otch = (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y')

    new_name_pred ='temp/40_COVID_19_БОТКИНА_' + date_otch + '_предварительный.xlsx'
    new_name_osn  ='temp/40_COVID_19_БОТКИНА_' + date_otch + '_основной.xlsx'

    
    shutil.copyfile('help/40_COVID_19_pred.xlsx' , new_name_pred)
    shutil.copyfile('help/40_COVID_19_osn.xlsx'  , new_name_osn)

    wb= openpyxl.load_workbook( new_name_pred)
    
    ws = wb['Спутник-V']
    rows = dataframe_to_rows(sput,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['Вчера_Спутник']
    rows = dataframe_to_rows(sput_old,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['ЭпиВакКорона']
    rows = dataframe_to_rows(epivak,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    ws = wb['Вчера_ЭпиВак']
    rows = dataframe_to_rows(epivak_old,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['КовиВак']
    rows = dataframe_to_rows(covivak,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['Спутник Лайт']
    rows = dataframe_to_rows(light,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)


    ws = wb['Вчера_КовиВак']
    rows = dataframe_to_rows(covivak_old,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['Ревакцинация']
    rows = dataframe_to_rows(revac,index=False, header=False)
    for r_idx, row in enumerate(rows,9):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['Вчера_ревакцин']
    rows = dataframe_to_rows(revac_old,index=False, header=False)
    for r_idx, row in enumerate(rows,9):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    ws = wb['Вчера_Спутник Лайт']
    rows = dataframe_to_rows(light_old,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save( new_name_pred) 

    # основной отчёт
    del sput[sput.columns[-1]]
    #del sput[sput.columns[-1]]
    #del sput[sput.columns[-1]]

    wb= openpyxl.load_workbook( new_name_osn)
    ws = wb['Спутник-V']
    rows = dataframe_to_rows(sput,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    del epivak[epivak.columns[-1]]
    #del epivak[epivak.columns[-1]]
    #del epivak[epivak.columns[-1]]
    
    ws = wb['ЭпиВакКорона']
    rows = dataframe_to_rows(epivak,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    del covivak[covivak.columns[-1]]
    #del covivak[covivak.columns[-1]]
    #del covivak[covivak.columns[-1]]

    ws = wb['КовиВак']
    rows = dataframe_to_rows(covivak,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)
    
    del light[light.columns[-1]]
    #del light[light.columns[-1]]
    #del light[light.columns[-1]]

    ws = wb['Спутник Лайт']
    rows = dataframe_to_rows(light,index=False, header=False)
    for r_idx, row in enumerate(rows,5):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    del revac['SCEP']

    ws = wb['Ревакцинация']
    rows = dataframe_to_rows(revac,index=False, header=False)
    for r_idx, row in enumerate(rows,9):  
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save( new_name_osn) 

    return new_name_pred + ';' + new_name_osn

