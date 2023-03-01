import pandas as pd
import requests
from datetime import datetime, timedelta

from system import return_mounth
from conf import REGIZ_AUTH

from .dict_toxic import Dict_Aim_Poison, Dict_Boolean_Alc, \
    Dict_Place_Incident, Dict_Place_Poison, \
    Dict_MKB, Dict_Type_Poison, Dict_Medical_Help, \
    Dict_Set_Diagnosis, Dict_district, XML, Dict_soch_polojenie


class my_except(Exception):
    pass


NAME_3 = 'temp/initial_data.xlsx'
NAME_4 = 'temp/toxic_raw.xlsx'


def get_cases(START: str, END: str) -> 'pd.DataFrame':
    """Получаем начальную выборку"""
    URL = " https://regiz.gorzdrav.spb.ru/N3.BI/getDData" \
        + f"?id=1127&args={START},{END}&auth={REGIZ_AUTH}"

    try:
        df = pd.DataFrame(data=requests.get(URL).json())
    except requests.Timeout:
        raise my_except('Недоступен сервер нетрики, попробуйте позже')
    except requests.ConnectionError:
        raise my_except('Недоступен сервер нетрики, попробуйте позже')

    df.to_excel(NAME_4, index=False)
    if len(df) == 0:
        raise my_except('нет случаев!')

    df['date_aff_first'] = pd.to_datetime(
        df['date_aff_first'],
        format='%Y-%m-%d'
        )

    df.sort_values(by=['date_aff_first'], inplace=True)
    df.drop_duplicates(
        subset=df.columns.drop('date_aff_first'),
        keep='last',
        inplace=True
        )
    df.index = range(len(df))

    obs = df.pivot_table(
        index=['luid'],
        columns=['observation_code'],
        values=['observation_value'],
        aggfunc='first'
        ).stack(0)
    DF = df.copy()

    del DF['observation_code']
    del DF['observation_value']

    DF = DF.drop_duplicates()
    DF = DF.merge(obs, how='left', on=['luid'])
    DF.index = range(len(DF))

    DF.to_excel(NAME_3)
    return DF

#def find_district(STRING):
#    for key,value in district.items():
#        if key in STRING.lower():
#            return value
#    return district['не указан район']


def find_street(STRING: str) -> str:
    list_ = [
        'проспект', 'пр.', 'бульвар',
        'аллея', 'улица', 'переулок', 'дорога',
        'шоссе', 'набережная', 'наб.', 'пер.', 'ул.',
        'ал.', 'бул.', 'площадь', 'пр-т', 'ул '
        ]
    for part in STRING.replace(';', ',').split(','):
        for key in list_:
            if key in part.lower():
                return part
    return STRING


def find_dom(STRING: str) -> str:
    for part in STRING.split(','):
        for key in ['д.', 'дом']:
            if key in part.lower():
                return part
    return ''


def find_kv(STRING: str) -> str:
    for part in STRING.split(','):
        for key in ['кв.', 'квартира']:
            if key in part.lower():
                return part
    return ''


def generate_xml(DF: 'pd.DataFrame', XML: str) -> tuple[str, 'pd.DataFrame']:
    "генерация выходного шаблона для импорта в АИС ГЗ"
    STRING = XML
    for i in range(len(DF)):
        part = f"""
    <r>
     <v f="2">{DF.at[i, 'history_number']}</v>
     <v f="3">***</v>
     <v f="4">{DF.at[i, 'gender'].replace('female','200').replace('male', '100')}</v>
     <v f="5">{DF.at[i,'age'] + '0000'}</v>
     <v f="6">{DF.at[i,'soch_polojenie'].split(';')[0]}</v>
     <v f="7">{DF.at[i,'c_district'].split(';')[0]}</v>
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
     <v f="26">{DF.at[i, 'meddoc_creation_date']}</v>
     <v f="37">{DF.at[i, 'street']}</v>
     <v f="38">{DF.at[i, 'house']}</v>
     <v f="39">{DF.at[i, 'flat']}</v>
     <v f="42">{DF.at[i, 'medical_help_name'].replace('НИИ СП', 'НИИ СП Джанелидзе')}</v>
    </r>"""
        try:
            STRING += part
        except Exception as e:
            DF.loc[i, 'comment'] = f'не попало в xml  {str(e)}'

    STRING += """
    </data>
    </dataset>
    </package>"""

    return STRING, DF


def toxic_genarate_xml(DATE_START: str, DATE_END: str) -> str:
    """Для ЦГиЭ случаи отравления"""

    df = get_cases(DATE_START, DATE_END)

    if len(df) == 0:
        raise my_except(f'Нет случаев отравления за период с {DATE_START} по {DATE_END}')

    # исправляем значения кейжев на коды аис гз
    CASE_CODES = [
        '303', '1101', '1102', '1103',
        '1104', '1105', '1108', '1109',
        '1110', '1113', '1115', '1117',
        '1119', '1123'
        ]

    for CASE in CASE_CODES:
        if CASE not in df.columns:
            df[CASE] = ''

    # дербаним адрес на составляющие
    df['adress'] = df['1102']
    df = df.fillna({'adress': ''})

    for i in range(len(df)):
        df.loc[i, 'street'] = find_street(df.at[i, 'adress'])
        df.loc[i, 'house'] = find_dom(df.at[i, 'adress'])
        df.loc[i, 'flat'] = find_kv(df.at[i, 'adress'])

    for i in range(len(df)):

        "Диагноз"
        df.loc[i, 'diagnosis'] = Dict_MKB.get(df.at[i, 'diagnosis'], '') \
            + ';' + df.at[i, 'diagnosis']

        "место происшествия Place_Incident"
        df.loc[i, 'place_incident'] = Dict_Place_Incident.get(df.at[i, '1101'])

        "наименование места происшествия  Place_Incident_Name"
        df.loc[i, 'place_incident_name'] = df.at[i, '1103']

        "Дата отравления DataPoison"
        df.loc[i, 'data_poison'] = df.at[i, '1104']

        "Дата первичного обращения DateFirstRecourse"
        df.loc[i, 'date_first_recourse'] = df.at[i, '1105']

        "Сочетание с алкоголем BooleanAlc"
        df.loc[i, 'boolean_alc'] = Dict_Boolean_Alc.get(df.at[i, '1108'])

        "Лицо установившее диагноз SetDiagnosis"
        df.loc[i, 'set_diagnosis'] = Dict_Set_Diagnosis.get(df.at[i, '1109'])

        "Оказана медицинская помощь MedicalHelp"
        df.loc[i, 'medical_help'] = Dict_Medical_Help.get(df.at[i, '1110'])

        "характер отравления TypePoison"
        df.loc[i, 'type_poison'] = Dict_Type_Poison.get(df.at[i, '1113'])

        "Обстоятельство отравления AimPoison"
        df.loc[i, 'aim_poison'] = Dict_Aim_Poison.get(df.at[i, '1115'])

        "Место приобретения яда PlacePoison"
        df.loc[i, 'place_poison'] = Dict_Place_Poison.get(df.at[i, '1117'])

        "Социальное положение"
        df.loc[i, 'soch_polojenie'] = Dict_soch_polojenie.get(df.at[i, '1119'])

        "Район места отравления"
        df.loc[i, 'c_district'] = Dict_district.get(df.at[i, '1123'])


    #df['date_aff_first'] = pd.to_datetime(df['date_aff_first'], format = '%Y-%m-%d', errors='coerce')

    df['data_poison'] = pd.to_datetime(
        df['data_poison'],
        format='%d.%m.%Y',
        errors='coerce'
        )

    df['date_first_recourse'] = pd.to_datetime(
        df['date_first_recourse'],
        format='%d.%m.%Y',
        errors='coerce'
        )

    df['date_aff_first'] = df['date_aff_first'].dt.strftime('%Y%m%d')

    df['data_poison'].loc[
        ~df['data_poison'].isnull()
        ] = df['data_poison'].loc[
            ~df['data_poison'].isnull()
                ].dt.strftime('%Y%m%d')

    df['date_first_recourse'].loc[
        ~df['date_first_recourse'].isnull()
        ] = df['date_first_recourse'].loc[
            ~df['date_first_recourse'].isnull()
            ].dt.strftime('%Y%m%d')

    df['meddoc_creation_date'] = pd.to_datetime(
        df['meddoc_creation_date'],
        errors='coerce'
        )

    df['meddoc_creation_date'].loc[
        ~df['meddoc_creation_date'].isnull()
        ] = df['meddoc_creation_date'].loc[
            ~df['meddoc_creation_date'].isnull()
            ].dt.strftime('%Y%m%d')

    # место приобретения яда пустые - приравниваем к другое
    df = df.fillna({
        'place_poison':   '50000;Другое',
        'place_incident': '70000;Другое',
        'c_district':     '0;Не указан район'})

    df = df.fillna('')

    NAME_1 = f'temp/toxic_{DATE_START}_{DATE_END}.xml'
    NAME_2 = f'temp/toxic_{DATE_START}_{DATE_END}.xlsx'

    string, df = generate_xml(df, XML)

    df.to_excel(NAME_2)
    with open(NAME_1, 'w') as f:
        f.write(string)

    return NAME_1 + ';' + NAME_2 + ';' + NAME_3 + ';' + NAME_4


def toxic_genarate_xml_mounth(DATE_GLOBAL):
    "сгенерировать за месяц"
    DATE = datetime.strptime(DATE_GLOBAL, '%d-%m-%Y')
    START, END = return_mounth(DATE)

    return toxic_genarate_xml(START, END)


def toxic_genarate_xml_week(DATE_GLOBAL):
    "сгенерировать за месяц"
    DATE_END = datetime.strptime(DATE_GLOBAL, '%d-%m-%Y').strftime('%Y-%m-%d')
    DATE_START = (
            datetime.strptime(DATE_GLOBAL, '%d-%m-%Y')
            - timedelta(days=7)
            ).strftime("%Y-%m-%d")

    return toxic_genarate_xml(DATE_START, DATE_END)


def toxic_genarate_xml_day(DATE_GLOBAL):
    "сгенерировать за месяц"
    DATE_END = datetime.strptime(DATE_GLOBAL, '%d-%m-%Y').strftime('%Y-%m-%d')
    DATE_START = (
            datetime.strptime(DATE_GLOBAL, '%d-%m-%Y')
            - timedelta(days=1)
            ).strftime("%Y-%m-%d")

    return toxic_genarate_xml(DATE_START, DATE_END)





