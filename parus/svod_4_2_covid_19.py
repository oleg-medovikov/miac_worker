import time, datetime, shutil, openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from base import parus_sql
import pandas as pd

NAMES = [
'region','ORGANIZATION','FULLNAME','MIAC_COVID4.2_vrach','MIAC_COVID4.2_telefo',
'MIAC_COVID4.2_gl','MIAC_COVID4.2_kl','MIAC_COVID4.2_rez','MIAC_COVID4.2_tipmo',
'MIAC_COVID4.2spm_vs','MIAC_COVID4.2spm_ivs','MIAC_COVID4.2spm_11',
'MIAC_COVID4.2spm_12','MIAC_COVID4.2spm_13','MIAC_COVID4.2spm_14',
'MIAC_COVID4.2spm_15','MIAC_COVID4.2spm_16','voditel','MIAC_COVID4.2spm_18',
'MIAC_COVID4.2pol_101','MIAC_COVID4.2pol_103','MIAC_COVID4.2pol_102',
'MIAC_COVID4.2pol_104','MIAC_COVID4.2pol_105','MIAC_COVID4.2pol_106',
'MIAC_COVID4.2pol_107','MIAC_COVID4.2pol_108','MIAC_COVID4.2pol_109',
'MIAC_COVID4.2pol_110','MIAC_COVID4.2pol_111','MIAC_COVID4.2pol_112',
'MIAC_COVID4.2pol_113','MIAC_COVID4.2pol_114','MIAC_COVID4.2pol_115',
'MIAC_COVID4.2pol_116','MIAC_COVID4.2_129','MIAC_COVID4.2_101',
'MIAC_COVID4.2_102','MIAC_COVID4.2_103','MIAC_COVID4.2_104',
'MIAC_COVID4.2_105','MIAC_COVID4.2_106','MIAC_COVID4.2_107','MIAC_COVID4.2_108',
'MIAC_COVID4.2_109','MIAC_COVID4.2_110','MIAC_COVID4.2_111','MIAC_COVID4.2_112',
'MIAC_COVID4.2_113','MIAC_COVID4.2_114','MIAC_COVID4.2_115','MIAC_COVID4.2_116',
'MIAC_COVID4.2_117','MIAC_COVID4.2_118','MIAC_COVID4.2_119','MIAC_COVID4.2_120',
'MIAC_COVID4.2_121','MIAC_COVID4.2_122','MIAC_COVID4.2_123','MIAC_COVID4.2_124',
'MIAC_COVID4.2_125','MIAC_COVID4.2_126','MIAC_COVID4.2_127','MIAC_COVID4.2_128',
'MIAC_COVID4.2_229','MIAC_COVID4.2_201','MIAC_COVID4.2_202','MIAC_COVID4.2_203',
'MIAC_COVID4.2_204','MIAC_COVID4.2_205','MIAC_COVID4.2_206','MIAC_COVID4.2_207',
'MIAC_COVID4.2_208','MIAC_COVID4.2_209','MIAC_COVID4.2_210','MIAC_COVID4.2_211',
'MIAC_COVID4.2_212','MIAC_COVID4.2_213','MIAC_COVID4.2_214','MIAC_COVID4.2_215',
'MIAC_COVID4.2_216','MIAC_COVID4.2_217','MIAC_COVID4.2_218','MIAC_COVID4.2_219',
'MIAC_COVID4.2_220','MIAC_COVID4.2_221','MIAC_COVID4.2_222','MIAC_COVID4.2_223',
'MIAC_COVID4.2_224','MIAC_COVID4.2_225','MIAC_COVID4.2_226','MIAC_COVID4.2_227',
'MIAC_COVID4.2_228','COVID4.2pol_109.1','COVID4.2pol_109.2','COVID4.2pol_109.3',
'COVID4.2pol_112.1','COVID4.2pol_112.2','COVID4.2pol_116.1','COVID4.2spm_16.1',
'COVID4.2spm_16.2','COVID4.2spm_16.3','COVID4.2spm_16.4','COVID4.2spm_16.5',
'COVID4.2spm_16.6','MIAC_COVID4.2_120.1','MIAC_COVID4.2_220.1','felsheri'
]

def svod_4_2_covid_19():
    SQL = open('parus/sql/covid_4.2_svod.sql', 'r').read()

    DF = parus_sql( SQL )

    DATE = DF.at[0, 'DAY']
    del DF['DAY']

    NEW_NAME =  'temp/4.2_COVID_19_' + DATE + '.xlsx'

    shutil.copyfile('help/4.2_COVID_19_svod.xlsx', NEW_NAME)

    ot = pd.DataFrame(columns=NAMES)

    ot['ORGANIZATION'] = pd.Series(DF['ORGANIZATION'].unique())
    ot['FULLNAME'] = ot['ORGANIZATION']

    for i in range(len(DF)):
        if DF.at[i,'POKAZATEL'] in NAMES:
            ot.loc[ot['ORGANIZATION'] == DF.at[i,'ORGANIZATION'], DF.at[i,'POKAZATEL'] ] = DF.at[i,'VALUE']

    ot['region'] = 'г. Санкт-Петербург'
    ot['MIAC_COVID4.2_vrach'] = ot['MIAC_COVID4.2_vrach'].str.replace('\n', '').str.replace('\r', '').str.replace('\t', ' ')
    ot['MIAC_COVID4.2_telefo'] = ot['MIAC_COVID4.2_telefo'].str.replace('\n', '').str.replace('\r', '').str.replace('\t', ' ')

    ot = ot.fillna(0)

    wb= openpyxl.load_workbook( NEW_NAME )

    ws = wb['svod']

    rows = dataframe_to_rows(ot,index=False, header=False)
    for r_idx, row in enumerate(rows,2):
        for c_idx, value in enumerate(row, 1):
            ws.cell(row=r_idx, column=c_idx, value=value)

    wb.save( NEW_NAME )

    return NEW_NAME
