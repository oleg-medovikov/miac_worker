import pandas as pd
import requests
from datetime import datetime, timedelta

from conf import REGIZ_AUTH, DADATA_TOKEN, DADATA_SECRET

from .dict_toxic import Dict_Aim_Poison, Dict_Boolean_Alc, \
                        Dict_Place_Incident, Dict_Place_Poison, \
                        Dict_MKB, Dict_Type_Poison, Dict_Medical_Help, \
                        Dict_Set_Diagnosis


class my_except(Exception):
    pass

XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
 <package>
  <info>
   <GUID>{A4F6D1E0-909A-11D5-B08F-000021EF6307}</GUID>
   <versionStat>404072</versionStat>
   <version>404072</version>
  </info>
  <dataset id="CaptionDB">
   <fields>
    <f id="1" name="id" t="Integer"></f>
    <f id="2" name="NUMNOTICE" t="String" s="50"></f>
    <f id="3" name="NAME" t="String" s="50" r="True"></f>
    <f id="4" name="C_Gender" t="Integer"></f>
    <f id="5" name="Age" t="Integer"></f>
    <f id="6" name="C_Social" t="Integer"></f>
    <f id="7" name="C_Region" t="Integer"></f>
    <f id="8" name="Note" t="String" s="255"></f>
    <f id="9" name="C_PlaceIncident" t="Integer"></f>
    <f id="10" name="Note3" t="String" s="255"></f>
    <f id="11" name="DatePoison" t="Integer"></f>
    <f id="12" name="DateFirstRecourse" t="Integer"></f>
    <f id="13" name="DateAffFirst" t="Integer"></f>
    <f id="14" name="C_Diagnosis" t="Integer"></f>
    <f id="15" name="C_BooleanAlc" t="Integer"></f>
    <f id="16" name="C_SetDiagnosis" t="Integer"></f>
    <f id="17" name="C_MedicalHelp" t="Integer"></f>
    <f id="18" name="C_PlaceMortality" t="Integer"></f>
    <f id="19" name="Note5" t="String" s="255"></f>
    <f id="20" name="C_TypePoison" t="Integer"></f>
    <f id="21" name="ValPoison" t="Float"></f>
    <f id="22" name="C_AimPoison" t="Integer"></f>
    <f id="23" name="Note7" t="String" s="255"></f>
    <f id="24" name="C_PlacePoison" t="Integer"></f>
    <f id="25" name="Note8" t="String" s="255"></f>
    <f id="26" name="DateDocument" t="Integer"></f>
    <f id="27" name="NAMEPEOPLEGET" t="String" s="50"></f>
    <f id="28" name="CREATEUSER" t="String" s="50"></f>
    <f id="29" name="CREATEDATE" t="DateTime"></f>
    <f id="30" name="UPDATEUSER" t="String" s="50"></f>
    <f id="31" name="UPDATEDATE" t="DateTime"></f>
    <f id="32" name="FlagColor" t="Integer"></f>
    <f id="33" name="C_GSEN" t="Integer"></f>
    <f id="34" name="S_OBJECTMESS" t="Integer"></f>
    <f id="35" name="S_OBJECTMESSNAME" t="String" s="255"></f>
    <f id="36" name="S_STREET" t="Integer"></f>
    <f id="37" name="S_STREETNAME" t="String" s="255"></f>
    <f id="38" name="HOUSE" t="String" s="50"></f>
    <f id="39" name="FLAT" t="String" s="50"></f>
    <f id="40" name="DateLock" t="Integer"></f>
    <f id="41" name="S_ObjectMedicalHelp" t="Integer"></f>
    <f id="42" name="S_ObjectMedicalHelpName" t="String" s="50"></f>
    <f id="43" name="errorfontcolor" t="Integer"></f>
    <f id="44" name="errorfontstyle" t="Integer"></f>
    <f id="45" name="errorcolor" t="Integer"></f>
    <f id="46" name="errorcolfontcolor" t="Integer"></f>
    <f id="47" name="errorcolfontstyle" t="Integer"></f>
    <f id="48" name="errorcolcolor" t="Integer"></f>
    <f id="48" name="errortext" t="String" s="254"></f>
    <f id="50" name="errorcolumns" t="String" s="254"></f>
    <f id="51" name="CANREADONLY" t="SmallInt"></f>
    <f id="52" name="CANEDITONLY" t="SmallInt"></f>
    <f id="53" name="CANDELETEONLY" t="SmallInt"></f>
   </fields>
   <data>
"""


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
        return requests.get(URL).json()[0]['address']
    
    import hashlib
    from multiprocesspandas import applyparallel
    return DF['luid'].apply_parallel(func, num_processes=10 )


def parsing_address(DF):
    """Парсинг адреса на составные части"""
    
    from dadata import Dadata
    for i in range(len(DF)):
        with Dadata(DADATA_TOKEN, DADATA_SECRET) as dadata:
            s = dadata.clean(name="address", source=DF.at[i, 'address'])
        
        DF.loc[i, 'region']   = s['region']
        DF.loc[i, 'area']     = s['area']
        DF.loc[i, 'street']   = s['street']
        DF.loc[i, 'house']    = s['house']
        DF.loc[i, 'flat']     = s['flat']
    
    return DF


def get_observation(START, END, DF):  
    for i in range(len(DF)):
        URL = f"http://10.128.66.207/N3.BI/getDData?id=1118&args={START},{END},{DF.at[i,'luid']},{DF.at[i,'history_number']}&auth=9f9208b9-f7e1-4e17-8cfc-a6832e03a12f"
        req = requests.get(URL).json()
        
        try:
            DF.loc[i, 'diagnosis'] = Dict_MKB.get(DF.loc[i, 'diagnosis'] ) + ';' + DF.loc[i, 'diagnosis']
        except:
            pass
        
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
     <v f="2">{DF.at[i, 'history_number'] + '0000'}</v>
     <v f="3">***</v>
     <v f="4">{DF.at[i, 'gender'].replace('female','200').replace('male', '100')}</v>
     <v f="5">360000</v>
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
     <v f="21"></v>
     <v f="22">{DF.at[i, 'aim_poison'].split(';')[0]}</v>
     <v f="24">{DF.at[i, 'place_poison'].split(';')[0]}</v>
     <v f="37">{DF.at[i, 'street']}</v>
     <v f="38">{DF.at[i, 'house']}</v>
     <v f="39">{DF.at[i, 'flat']}</v>
     <v f="42">{DF.at[i, 'medical_help_name']}</v>
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
    DATE_START = (datetime.strptime(DATE_GLOBAL, '%d-%m-%Y') - timedelta(days=7)).strftime("%Y-%m-%d")

    df = get_cases(DATE_START, DATE_END)

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

    NAME = f'/tmp/toxic_{DATE_START}-{DATE_END}.xml'

    with open(NAME, 'w') as f:
        f.write(XML)

    return NAME
