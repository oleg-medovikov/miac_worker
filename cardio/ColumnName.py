class ColumnName:
    name: str
    keys: set

    def __init__(self, name, keys):
        self.name = name
        self.keys = set(keys)

    @staticmethod
    def all_names(NAMES):
        list_ = []
        for NAME in NAMES:
            list_.append(NAME.name)
        list_.append('Пол')
        return set(list_)


NAMES = [
    ColumnName(**{
        'name': 'Краткое наименование юр. лица МО',
        'keys': ['наименов', 'лица'],
    }),
    ColumnName(**{
        'name': 'Наименования подразделения МО',
        'keys': ['наименов', 'подразд'],
    }),
    ColumnName(**{
        'name': 'OID',
        'keys': ['o', 'i', 'd'],
    }),
    ColumnName(**{
        'name': 'Идентификатор пациента в МИС',
        'keys': ['дентификат', 'пациент'],
    }),
    ColumnName(**{
        'name': 'Принадлежность адреса пациента к участку',
        'keys': [' адрес',  'участ'],
    }),
    ColumnName(**{
        'name': 'Локальный ID участка в МИС',
        'keys': ['id',  'участ'],
    }),
    ColumnName(**{
        'name': 'Фамилия',
        'keys': ['амилия'],
    }),
    ColumnName(**{
        'name': 'Фамилия',
        'keys': ['second', 'name'],
    }),
    ColumnName(**{
        'name': 'Имя',
        'keys': ['имя'],
    }),
    ColumnName(**{
        'name': 'Имя',
        'keys': ['name'],
    }),
    ColumnName(**{
        'name': 'Отчество',
        'keys': ['тчество'],
    }),
    ColumnName(**{
        'name': 'Отчество',
        'keys': ['middle', 'name'],
    }),
    ColumnName(**{
        'name': 'Отчество',
        'keys': ['middle', 'name'],
    }),
    ColumnName(**{
     'name': 'Дата рождения',
     'keys': ['дата', 'рожд'],
    }),
    ColumnName(**{
        'name': 'Дата рождения',
        'keys': ['др.'],
    }),
    ColumnName(**{
        'name': 'Дата рождения',
        'keys': ['birthday'],
    }),
    ColumnName(**{
        'name': 'Номер СНИЛС',
        'keys': ['снилс'],
    }),
    ColumnName(**{
        'name': 'Телефон пациента (мобильный)',
        'keys': ['телефон', 'моб'],
    }),
    ColumnName(**{
        'name': 'Телефон пациента (мобильный)',
        'keys': ['контакт', '1'],
    }),
    ColumnName(**{
        'name': 'Телефон пациента (домашний)',
        'keys': ['телефон', 'домаш'],
    }),
    ColumnName(**{
        'name': 'Телефон пациента (домашний)',
        'keys': ['контакт', '2'],
    }),
    ColumnName(**{
        'name': 'Адрес пациента',
        'keys': ['адрес пациента'],
    }),
    ColumnName(**{
        'name': 'Серия паспорта',
        'keys': ['серия', 'паспор'],
    }),
    ColumnName(**{
        'name': 'Номер паспорта',
        'keys': ['номер', 'паспор'],
    }),
    ColumnName(**{
        'name': 'Серия полиса ОМС',
        'keys': ['серия', 'полис'],
    }),
    ColumnName(**{
        'name': 'Номер полиса ОМС',
        'keys': ['номер', 'полис'],
    }),
    ColumnName(**{
        'name': 'Идентификатор врача, осуществляющего ДН',
        'keys': ['дентификатор', 'врача', ],
    }),
    ColumnName(**{
        'name': 'Наименование специальности врача, осуществляющего ДН',
        'keys': ['наименование', 'специал', 'врача'],
    }),
    ColumnName(**{
        'name': 'Идентификация специальности врача, осуществляющего ДН',
        'keys': ['дентификация', 'специал', 'врача'],
    }),
    ColumnName(**{
        'name': 'GUID структурного подразделения врача, осуществляющего ДН',
        'keys': ['guid', 'подразд', 'врача'],
    }),
    ColumnName(**{
        'name': 'Дата необходимой записи на приём (месяц и год)',
        'keys': ['дата', 'записи'],
    }),
]
