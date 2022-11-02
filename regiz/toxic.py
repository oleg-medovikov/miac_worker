import pandas as pd
import requests
from datetime import datetime, timedelta

from conf import REGIZ_AUTH

from .dict_toxic import Dict_Aim_Poison, Dict_Boolean_Alc, \
                        Dict_Place_Incident, Dict_Place_Poison, \
                        Dict_MKB, Dict_Type_Poison, Dict_Medical_Help, \
                        Dict_Set_Diagnosis, district, XML, Dict_soch_polojenie


class my_except(Exception):
    pass


def get_cases(START, END):
    """Получаем начальную выборку"""
    URL = f" https://regiz.gorzdrav.spb.ru/N3.BI/getDData?id=1127&args={START},{END}&auth={REGIZ_AUTH}"
    
    try:
        df = pd.DataFrame( data = requests.get(URL).json() )
    except:
        raise my_except(URL)
    
    if len(df) == 0:
        raise my_except('нет случаев!')

    df['date_aff_first'] = pd.to_datetime(df['date_aff_first'], format='%Y-%m-%d')
    df.sort_values(by=['date_aff_first'], inplace=True )
    df.drop_duplicates(subset=df.columns.drop('date_aff_first'), keep='last', inplace=True )
    df.index = range(len(df))
    
    obs = df.pivot_table(index=['luid'], columns=['s.observation_code'],values=['s.observation_value'],aggfunc='first').stack(0)
    DF = df.copy()
    
    del DF ['s.observation_code']
    del DF ['s.observation_value']

    DF = DF.drop_duplicates()
    DF = DF.merge(obs, how='left', on=['luid'])
    DF.index = range(len(DF))

    return DF

def find_district(STRING):
    for key,value in district.items():
        if key in STRING.lower():
            return value
    return district['не указан район']

def find_street(STRING):
    for part in STRING.split(','):
        for key in ['проспект', 'пр.', 'бульвар','аллея','улица','переулок','дорога','шоссе','набережная','наб.','пер.','ул.','ал.','бул.' ]:
            if key in part.lower():
                return part
    return ''

def find_dom(STRING):
    for part in STRING.split(','):
        for key in ['д.', 'дом']:
            if key in part.lower():
                return part
    return ''

def find_kv(STRING):
    for part in STRING.split(','):
        for key in ['кв.', 'квартира']:
            if key in part.lower():
                return part
    return ''

def generate_xml(DF, XML):
    STRING = XML
    for i in range(len (DF)):
        part = f"""
    <r>
     <v f="2">{DF.at[i, 'history_number']}</v>
     <v f="3">***</v>
     <v f="4">{DF.at[i, 'gender'].replace('female','200').replace('male', '100')}</v>
     <v f="5">{DF.at[i,'age'] + '0000'}</v>
     <v f="6">{DF.at[i,'soch_polojenie'].split(';')[0]}</v>
     <v f="7">{round(DF.at[i,'district'])}</v>
     <v f="8"></v>
     <v f="9">{DF.at[i,  'place_incident'].split(';')[0]}</v>
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
        STRING += part
        
    STRING +="""
    </data>
    </dataset>
    </package>"""
    
    return STRING


def toxic_genarate_xml(DATE_GLOBAL):
    """Для ЦГиЭ случаи отравления"""

    DATE_END   =  datetime.strptime(DATE_GLOBAL, '%d-%m-%Y').strftime('%Y-%m-%d')
    DATE_START = (datetime.strptime(DATE_GLOBAL, '%d-%m-%Y') - timedelta(days=30)).strftime("%Y-%m-%d")

    df = get_cases(DATE_START, DATE_END)
    
    if len(df) == 0:
        raise my_except(f'Нет случаев отравления за период с {DATE_START} по {DATE_END}')

    df.to_excel('temp/toxic.xlsx')

    # дербаним адрес на составляющие

    for i in range(len(df)):
        df.loc[i,'district'] = find_district(df.at[i,'adress'])
        df.loc[i,'street']   = find_street(df.at[i,'adress'])
        df.loc[i,'house']    = find_dom(df.at[i,'adress'])
        df.loc[i,'flat']     = find_kv(df.at[i,'adress'])

    
    # исправляем значения кейжев на коды аис гз 
    
    CASE_CODES = ['1101','1102','1104', '1105','1108', '1109', '1110','1113','1115','1117','1119' ]

    for CASE in CASE_CODES:
        if CASE not in df.columns:
            df[CASE] = ''
    
    for i in range(len(df)):

        "Диагноз"
        df.loc[i, 'diagnosis'] = Dict_MKB.get(df.at[i, 'diagnosis'] ) + ';' + df.at[i, 'diagnosis']

        "место происшествия Place_Incident"
        df.loc[i, 'place_incident'] = Dict_Place_Incident.get( df.at[i,'1101'] )
        
        "наименование места происшествия  Place_Incident_Name"
        df.loc[i, 'place_incident_name'] = df.at[i,'1102']

        "Дата отравления DataPoison"
        df.loc[i, 'data_poison'] = df.at[i, '1104']

        "Дата первичного обращения DateFirstRecourse"
        df.loc[i, 'date_first_recourse'] = df.at[i, '1105']

        "Сочетание с алкоголем BooleanAlc"
        df.loc[i, 'boolean_alc'] = Dict_Boolean_Alc.get(df.at[i, '1108'] )

        "Лицо установившее диагноз SetDiagnosis"
        df.loc[i, 'set_diagnosis'] = Dict_Set_Diagnosis.get( df.at[i, '1109'] )

        "Оказана медицинская помощь MedicalHelp"
        df.loc[i, 'medical_help'] =  Dict_Medical_Help.get(  df.at[i, '1110'] )

        "характер отравления TypePoison"
        df.loc[i, 'type_poison'] =  Dict_Type_Poison.get( df.at[i, '1113'] )

        "Обстоятельство отравления AimPoison"
        df.loc[i, 'aim_poison'] =  Dict_Aim_Poison.get( df.at[i, '1115'] )

        "Место приобретения яда PlacePoison"
        df.loc[i, 'place_poison'] =  Dict_Place_Poison.get( df.at[i, '1117'] )
        
        "Социальное положение"
        df.loc[i, 'soch_polojenie'] =  Dict_soch_polojenie.get( df.at[i, '1119'] )

    df['date_aff_first'] = pd.to_datetime(df['date_aff_first'], format = '%Y-%m-%d', errors='coerce')
    df['data_poison'] = pd.to_datetime(df['data_poison'], format = '%d.%m.%Y', errors='coerce')

    df['date_first_recourse'] = pd.to_datetime(df['date_first_recourse'], format = '%d.%m.%Y', errors='coerce')

    df['date_aff_first'] = df['date_aff_first'].dt.strftime('%Y%m%d')

    df['data_poison'].loc[~df['data_poison'].isnull()] = df['data_poison'].loc[~df['data_poison'].isnull()].dt.strftime('%Y%m%d')
    df['date_first_recourse'].loc[~df['date_first_recourse'].isnull()] = df['date_first_recourse'].loc[~df['date_first_recourse'].isnull()].dt.strftime('%Y%m%d')
    df = df.fillna('')

    string = generate_xml(df, XML)

    NAME = f'/tmp/toxic_{DATE_START}_{DATE_END}.xml'

    with open(NAME, 'w') as f:
        f.write(string)

    return NAME
