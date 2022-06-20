from base import covid_sql, covid_exec, covid_insert

SQL_NAMES = [
['net_diagnoz_covid.sql', 'Не стоит диагноз ковид' ],
['no_snils.sql', 'Без СНИЛСа'],
['no_OMS.sql', 'Нет сведений ОМС'],
['bez_ishod.sql', 'Без исхода заболевания больше 45 дней'],
['no_lab.sql', 'без лабораторного потверждения'],
['net_dnevnik.sql','Нет дневниковых записей'],
['net_pad.sql', 'Нет ПАД'],
['neverni_vid_lecenia.sql','Неверный вид лечения'],
['bez_ambulat_level.sql', 'Нет амбулаторного этапа'],
['bez_ambulat_level_amb.sql', 'Пациенты зависшие по МО'],
['bez_ambulat_level_noMO.sql', 'Пациенты зависшие без МО']
    ]

async def zamechania():
    SQL = """
    SELECT max([Дата изменения РЗ]) as 'дата отчета'
        from robo.v_FedReg
    """

    DATE = covid_sql(SQL).iloc[0,0]

    SQL = open('func/zam_mz/sql/kolichestvo.sql').read()

    DF = covid_sql( SQL )
    del DF ['Принадлежность']
    DF ['дата отчета'] = DATE

    for FILE,NAME in SQL_NAMES:
        SQL = open('func/zam_mz/sql/' + FILE, 'r').read()
        PART = covid_sql( SQL )
        PART = PART.groupby(
                by=["Медицинская организация"],
                as_index=False).size()

        PART.rename(columns={"size": NAME}, inplace=True)

    DF = DF.merge(
            PART,
            how='left',
            left_on='Медицинская организация',
            right_on='Медицинская организация')

    SQL = f"""
    DELETE from [robo].[cv_Zamechania_fr]
        WHERE [дата отчета] ='{DATE.strftime('%Y-%m-%d')}'
        """

    covid_exec( SQL )

    DF.fillna(0, inplace=True)

    covid_insert(
            DF,
            'cv_Zamechania_fr',
            'robo',
            False,
            'append')

    return 'Замечания сгенерированы'

