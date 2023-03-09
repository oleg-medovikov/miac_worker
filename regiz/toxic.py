import pandas as pd
from datetime import datetime, timedelta

from system import return_mounth

from .dict_toxic import Dict_Aim_Poison, Dict_Boolean_Alc, \
    Dict_Place_Incident, Dict_Place_Poison, \
    Dict_MKB, Dict_Type_Poison, Dict_Medical_Help, \
    Dict_Set_Diagnosis, Dict_district, XML, Dict_soch_polojenie, \
    Dict_sex

from .toxic_get_cases import toxic_get_cases
from .toxic_checker import toxic_checker
from system import write_styling_excel_file


class my_except(Exception):
    pass


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


def generate_row(row: dict) -> str:
    LIST = (
        '\n<r>',
        '\n\t<v f="2">', row['history_number'], '</v>',  # номер ИБ
        '\n\t<v f="3">***</v>',  # вместо ФИО звездочки
        '\n\t<v f="4">', row['gender'],  '</v>',  # пол
        '\n\t<v f="5">', row['age'],  '0000</v>',  # возраст
        '\n\t<v f="6">', row['soch_polojenie'].split(';')[0], '</v>',
        '\n\t<v f="7">', row['c_district'].split(';')[0], '</v>',
        '\n\t<v f="8">',
        '\n\t<v f="9">', row['place_incident'].split(';')[0], '</v>',
        '\n\t<v f="10">', row['place_incident_name'], '</v>',
        '\n\t<v f="11">', row['date_poison'], '</v>',
        '\n\t<v f="12">', row['date_first_recourse'], '</v>',
        '\n\t<v f="13">', row['date_aff_first'], '</v>',
        '\n\t<v f="14">', row['diagnosis'].split(';')[0], '</v>',
        '\n\t<v f="15">', row['boolean_alc'].split(';')[0], '</v>',
        '\n\t<v f="16">', row['set_diagnosis'].split(';')[0], '</v>',
        '\n\t<v f="17">', row['medical_help'].split(';')[0], '</v>',
        '\n\t<v f="18"></v>',
        '\n\t<v f="20">', row['type_poison'].split(';')[0], '</v>',
        '\n\t<v f="21">1</v>',
        '\n\t<v f="22">', row['aim_poison'].split(';')[0], '</v>',
        '\n\t<v f="24">', row['place_poison'].split(';')[0], '</v>',
        '\n\t<v f="26">', row['date_document'], '</v>',  # дата date_aff_first
        '\n\t<v f="37">', row['street'], '</v>',
        '\n\t<v f="38">', row['house'], '</v>',
        '\n\t<v f="39">', row['flat'], '</v>',
        '\n\t<v f="42">',
        row['medical_help_name'].replace('НИИ СП', 'НИИ СП Джанелидзе'),
        '</v>',
        '\n</r>'
        )
    return ''.join(str(x) for x in LIST)


def generate_xml(DF: 'pd.DataFrame', XML: str) -> str:
    "генерация выходного шаблона для импорта в АИС ГЗ"
    STRING = XML
    for row in DF.to_dict('records'):
        try:
            STRING += generate_row(row)
        except:
            continue

    STRING += """
    </data>
    </dataset>
    </package>"""

    return STRING


def toxic_genarate_xml(DATE_START: str, DATE_END: str) -> str:
    """Для ЦГиЭ случаи отравления"""

    df = toxic_get_cases(DATE_START, DATE_END)
    NAME_3 = 'temp/initial_data.xlsx'
    df.to_excel(NAME_3)

    if len(df) == 0:
        raise my_except(
            f'Нет случаев отравления за период с {DATE_START} по {DATE_END}'
            )
    # проверяем данные
    error = toxic_checker(df)

    if len(error):
        df = df.loc[~df['history_number'].isin(error['history_number'])]
        NAME_4 = f'temp/toxic_error_{DATE_START}_{DATE_END}.xlsx'
        write_styling_excel_file(NAME_4, error, 'errors')

    # дербаним адрес на составляющие
    df['adress'] = df['1102']
    df = df.fillna({'adress': ''})

    for i in df.index:
        df.loc[i, 'street'] = find_street(df.at[i, 'adress'])
        df.loc[i, 'house'] = find_dom(df.at[i, 'adress'])
        df.loc[i, 'flat'] = find_kv(df.at[i, 'adress'])

    for i in df.index:
        "Пол"
        df.loc[i, 'gender'] = Dict_sex.get(df.at[i, 'gender'])

        "Диагноз"
        df.loc[i, 'diagnosis'] = Dict_MKB.get(df.at[i, 'diagnosis'], '') \
            + ';' + df.at[i, 'diagnosis']

        "место происшествия Place_Incident"
        df.loc[i, 'place_incident'] = Dict_Place_Incident.get(df.at[i, '1101'])

        "наименование места происшествия  Place_Incident_Name"
        df.loc[i, 'place_incident_name'] = df.at[i, '1103']

        "Дата создания документа"
        df.loc[i, 'date_document'] = df.at[i, '303']

        "Дата отравления DatePoison"
        df.loc[i, 'date_poison'] = df.at[i, '1104']

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

    NAME_2 = f'temp/toxic_{DATE_START}_{DATE_END}.xlsx'
    df.to_excel(NAME_2)
    df['date_document'] = pd.to_datetime(
        df['date_document'],
        format='%d.%m.%Y',
        errors='coerce'
        )

    df['date_poison'] = pd.to_datetime(
        df['date_poison'],
        format='%d.%m.%Y',
        errors='coerce'
        )

    df['date_first_recourse'] = pd.to_datetime(
        df['date_first_recourse'],
        format='%Y-%m-%d %H:%M:%S',
        errors='coerce'
        )

    df['date_document'] = df['date_document'].dt.strftime('%Y%m%d')

    df['date_aff_first'] = df['date_aff_first'].dt.strftime('%Y%m%d')

    df['date_poison'].loc[
        ~df['date_poison'].isnull()
        ] = df['date_poison'].loc[
            ~df['date_poison'].isnull()
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

    string = generate_xml(df, XML)

    df.to_excel(NAME_2)
    with open(NAME_1, 'w') as f:
        f.write(string)

    if len(error):
        return NAME_1 + ';' + NAME_2 + ';' + NAME_3 + ';' + NAME_4

    return NAME_1 + ';' + NAME_2 + ';' + NAME_3


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
