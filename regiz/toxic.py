import pandas as pd
import requests
from datetime import datetime, timedelta

from conf import REGIZ_AUTH, DADATA_TOKEN, DADATA_SECRET

from .dict_toxic import Dict_Aim_Poison, Dict_Boolean_Alc, \
                        Dict_Place_Incident, Dict_Place_Poison, \
                        Dict_MKB, Dict_Type_Poison, Dict_Medical_Help, \
                        Dict_Set_Diagnosis, XML


class my_except(Exception):
    pass



def get_cases(START,END):
    """Получаем начальную выборку"""

    URL = f" https://regiz.gorzdrav.spb.ru/N3.BI/getDData?id=1078&args={START},{END}&auth={REGIZ_AUTH}"

    DF = pd.DataFrame( data = requests.get(URL).json() )

    if len(DF) == 0:
        raise my_except(f'Нет случаев отравления за период c {START} по {END}')

    DF['date_aff_first'] = pd.to_datetime(DF['date_aff_first'], format='%Y-%m-%d')
    DF.sort_values(by=['date_aff_first'], inplace=True )
    DF.drop_duplicates(subset=DF.columns.drop('date_aff_first'), keep='last', inplace=True )
    DF.index = range(len(DF))
    return DF


def get_address_multi(DF):
    """Получение адреса в много потоков"""
    def func(x):
        URL = f"https://regiz.gorzdrav.spb.ru/N3.BI/getDData?id=1079&args={x}&auth={REGIZ_AUTH}"

        try:
            s = requests.get(URL).json()[0]['address']
        except:
            s = ''

        if s is None:
            s = ''

        return s
    
    import hashlib
    from multiprocesspandas import applyparallel
    return DF['luid'].apply_parallel(func, num_processes=10 )


def parsing_address(DF):
    """Парсинг адреса на составные части"""
    print ( 'tokens', DADATA_TOKEN, DADATA_SECRET)

    from dadata import Dadata
    for i in range(len(DF)):
        with Dadata(DADATA_TOKEN, DADATA_SECRET) as dadata:
            s = dadata.clean(name="address", source=DF.at[i, 'address'])
        
        DF.loc[i, 'region']  = s['region']
        DF.loc[i, 'area']    = s['area']
        DF.loc[i, 'street']  = s['street']
        DF.loc[i, 'house']   = s['house']
        DF.loc[i, 'flat']    = s['flat']
    
    return DF


def get_observation(START, END, DF):  
    for i in range(len(DF)):
        URL = f"http://10.128.66.207/N3.BI/getDData?id=1118&args={START},{END},{DF.at[i,'luid']},{DF.at[i,'history_number']}&auth=9f9208b9-f7e1-4e17-8cfc-a6832e03a12f"
        req = requests.get(URL).json()
        
        try:
            DF.loc[i, 'diagnosis'] = Dict_MKB.get(DF.loc[i, 'diagnosis'] ) + ';' + DF.loc[i, 'diagnosis']
        except:
            pass
        
        DF['date_first_recourse'] = ''
        DF['data_poison'] = ''
        DF['place_incident'] = ''
        DF['place_incident_name'] = ''
        DF['date_first_recourse'] = ''
        DF['boolean_alc'] = ''
        DF['set_diagnosis'] = ''
        DF['medical_help'] = ''
        DF['type_poison'] = ''
        DF['aim_poison'] = ''
        DF['place_poison'] = ''

        for part in req:
            if   part['observation_code'] == '1101':
                "место происшествия Place_Incident"
                DF.loc[i, 'place_incident'] = Dict_Place_Incident.get(part['observation_value'])
            
            elif part['observation_code'] == '1102':
                "наименование места происшествия  Place_Incident_Name"
                DF.loc[i, 'place_incident_name'] = part['observation_value']
            
            elif part['observation_code'] == '1104':
                "Дата отравления DataPoison"
                DF.loc[i, 'data_poison'] = part['observation_value']
            
            elif part['observation_code'] == '1105':
                "Дата первичного обращения DateFirstRecourse"
                DF.loc[i, 'date_first_recourse'] = part['observation_value']
            
            elif part['observation_code'] == '1108':
                "Сочетание с алкоголем BooleanAlc"
                DF.loc[i, 'boolean_alc'] = Dict_Boolean_Alc.get(part['observation_value']) 
            
            elif part['observation_code'] == '1109':
                "Лицо установившее диагноз SetDiagnosis"
                DF.loc[i, 'set_diagnosis'] = Dict_Set_Diagnosis.get(part['observation_value']) 
        
            elif part['observation_code'] == '1110':
                "Оказана медицинская помощь MedicalHelp"
                DF.loc[i, 'medical_help'] =  Dict_Medical_Help.get(part['observation_value']) 
            
            elif part['observation_code'] == '1113':
                "характер отравления TypePoison"
                DF.loc[i, 'type_poison'] =  Dict_Type_Poison.get(part['observation_value'])
                
            elif part['observation_code'] == '1115':
                "Обстоятельство отравления AimPoison"
                DF.loc[i, 'aim_poison'] =  Dict_Aim_Poison.get(part['observation_value'])
            
            elif part['observation_code'] == '1117':
                "Место приобретения яда PlacePoison"
                DF.loc[i, 'place_poison'] =  Dict_Place_Poison .get(part['observation_value'])            
            
            
    return DF

def generate_xml(DF):
    global XML
    for i in range(len (DF)):
        part = f"""     <r>
     <v f="2">{DF.at[i, 'history_number']}</v>
     <v f="3">***</v>
     <v f="4">{DF.at[i, 'gender'].replace('female','200').replace('male', '100')}</v>
     <v f="5">{DF.at[i,'age'] + '0000'}</v>
     <v f="8"></v>
     <v f="9">{DF.at[i, 'place_incident'].split(';')[0]}</v>
     <v f="10">{DF.at[i, 'place_incident_name']}</v>
     <v f="11">{DF.at[i, 'data_poison']}</v>
     <v f="12">{DF.at[i, 'date_first_recourse']}</v>
     <v f="13">{DF.at[i, 'date_aff_first']}</v>
     <v f="14">{DF.at[i, 'diagnosis'].split(';')[0]}</v>
     <v f="15">{DF.at[i, 'boolean_alc'].split(';')[0]}</v>
     <v f="16">{DF.at[i, 'set_diagnosis'].split(';')[0]}</v>
     <v f="17">{DF.at[i, 'medical_help'].split(';')[0]}</v>
     <v f="18"></v>
     <v f="20">{DF.at[i, 'type_poison'].split(';')[0]}</v>
     <v f="21">1</v>
     <v f="22">{DF.at[i, 'aim_poison'].split(';')[0]}</v>
     <v f="24">{DF.at[i, 'place_poison'].split(';')[0]}</v>
     <v f="37">{DF.at[i, 'street']}</v>
     <v f="38">{DF.at[i, 'house']}</v>
     <v f="39">{DF.at[i, 'flat']}</v>
     <v f="42">{DF.at[i, 'medical_help_name'].replace('НИИ СП', 'НИИ СП Джанелидзе')}</v>
    </r>"""
        XML += part
        
    XML +="""
    </data>
    </dataset>
    </package>"""
    
    return XML


def toxic_genarate_xml(DATE_GLOBAL):
    """Для ЦГиЭ случаи отравления"""

    DATE_END   =  datetime.strptime(DATE_GLOBAL, '%d-%m-%Y').strftime('%Y-%m-%d')
    DATE_START = (datetime.strptime(DATE_GLOBAL, '%d-%m-%Y') - timedelta(days=30)).strftime("%Y-%m-%d")

    df = get_cases(DATE_START, DATE_END)
    
    df.to_excel('temp/toxic.xlsx')

    df ['address'] = get_address_multi(df)

    df = parsing_address(df)

    df = get_observation(DATE_START, DATE_END, df)

    df['date_aff_first'] = pd.to_datetime(df['date_aff_first'], format = '%Y-%m-%d', errors='coerce')
    df['data_poison'] = pd.to_datetime(df['data_poison'], format = '%d.%m.%Y', errors='coerce')

    df['date_first_recourse'] = pd.to_datetime(df['date_first_recourse'], format = '%d.%m.%Y', errors='coerce')

    df['date_aff_first'] = df['date_aff_first'].dt.strftime('%Y%m%d')

    df['data_poison'].loc[~df['data_poison'].isnull()] = df['data_poison'].loc[~df['data_poison'].isnull()].dt.strftime('%Y%m%d')
    df['date_first_recourse'].loc[~df['date_first_recourse'].isnull()] = df['date_first_recourse'].loc[~df['date_first_recourse'].isnull()].dt.strftime('%Y%m%d')
    df = df.fillna('')

    XML = generate_xml(df)

    NAME = f'/tmp/toxic_{DATE_START}_{DATE_END}.xml'

    with open(NAME, 'w') as f:
        f.write(XML)

    return NAME
