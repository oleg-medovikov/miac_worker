from datetime import datetime, timedelta
import shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql

def svod_40_covid_19():
    sql_01 = open('parus/sql/covid_40_spytnic.sql','r').read()
    sql_02 = open('parus/sql/covid_40_spytnic_old.sql','r').read()
    sql_03 = open('parus/sql/covid_40_epivak.sql','r').read()
    sql_04 = open('parus/sql/covid_40_epivak_old.sql','r').read()
    sql_05 = open('parus/sql/covid_40_covivak.sql','r').read()
    sql_06 = open('parus/sql/covid_40_covivak_old.sql','r').read()
    sql_07 = open('parus/sql/covid_40_revac.sql','r').read()
    sql_08 = open('parus/sql/covid_40_revac_old_new.sql','r').read()
    sql_09 = open('parus/sql/covid_40_light.sql','r').read()
    sql_10 = open('parus/sql/covid_40_light_old.sql','r').read()

    sput         = parus_sql(sql_01)
    sput_old     = parus_sql(sql_02)
    epivak       = parus_sql(sql_03)
    epivak_old   = parus_sql(sql_04)
    covivak      = parus_sql(sql_05)
    covivak_old  = parus_sql(sql_06)
    revac        = parus_sql(sql_07)
    revac_old    = parus_sql(sql_08)
    light        = parus_sql(sql_09)
    light_old    = parus_sql(sql_10)

    OLD_ORG = ['ООО "Ава-Петер"']

    #sput = sput.loc[ (sput['ORGANIZATION'].isin(OLD_ORG) & sput['DAY']== '31.08.2022') | (~(sput['ORGANIZATION'].isin(OLD_ORG)) & sput['DAY'] != '31.08.2022') ]
    
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

    #del sput        ['DAY']
    del sput_old    ['DAY']
    del epivak      ['DAY']
    del epivak_old  ['DAY']
    del covivak     ['DAY']
    del covivak_old ['DAY']
    del revac       ['DAY']
    del revac_old   ['DAY']
    del light       ['DAY']
    del light_old   ['DAY']


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

















            
