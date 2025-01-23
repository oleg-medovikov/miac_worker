from base import parus_sql

medical_institutions_dict = {
    178564: 'СПб ГБУЗ "Центр по профилактике и борьбе со СПИД и инфекционными заболеваниями"',
    183964: 'СПб ГКУЗ "Городская психиатрическая больница №6 (стационар с диспансером)"',
    171868: 'СПб ГБУЗ "Городская туберкулезная больница №2"',
    174604: 'СПб ГКУЗ "Психиатрическая больница Святого Николая Чудотворца"',
    187276: 'СПб ГКУЗ "Городская психиатрическая больница №3 им.И.И.Скворцова-Степанова"',
    188716: 'СПб ГКУЗ "Хоспис №2"',
    173956: 'СПб ГКУЗ Центр восстановительного лечения "Детская психиатрия" имени С.С. Мнухина',
    731168: "ГБУ СПб НИИ СП им. И.И. Джанелидзе",
    731175: 'ФГБУ "Национальный медицинский исследовательский центр онкологии им. Н.Н. Петрова" Минздрава России',
    179212: 'СПБ ГБУЗ "Детский городской многопрофильный клинический специализированный центр высоких медицинских технологий"',
    175972: 'СПб ГБУЗ "Детская городская больница №17 Святителя Николая Чудотворца"',
    177916: 'СПБ ГБУЗ "ДГМКЦ ВМТ им. К.А. Раухфуса"',
    187996: 'СПб ГБУЗ "Туберкулезная больница №8"',
    184396: 'СПб ГБУЗ "ДГБ №2 святой Марии Магдалины"',
    178924: 'СПб ГБУЗ "Детская городская больница Святой Ольги"',
    172300: 'СПб ГБУЗ "Детская городская клиническая больница №5 имени Нила Федоровича Филатова"',
    177772: 'СПб ГБУЗ "Детская инфекционная больница №3"',
    182308: 'СПб ГБУЗ "Клиническая больница Святителя Луки"',
    185116: 'СПб ГБУЗ "Центр планирования семьи и репродукции"',
    185908: 'СПб ГБУЗ "Родильный дом №13"',
    178852: 'СПб ГБУЗ "Родильный дом №1 (специализированный)"',
    183172: 'СПб ГБУЗ "Родильный дом №10"',
    181084: 'СПб ГБУЗ "Родильный дом №17"',
    185836: 'СПб ГБУЗ "Родильный дом №6 им. проф. В.Ф.Снегирева"',
    182236: 'СПб ГБУЗ "Родильный дом №16"',
    186988: 'СПб ГБУЗ "Городской перинатальный центр №1"',
    174244: 'СПб ГБУЗ "Родильный дом №9"',
    171148: 'СПб ГБУЗ "Городская больница №9"',
    189004: 'СПб ГБУЗ "Городская Мариинская больница"',
    186700: 'СПб ГБУЗ "Городской клинический онкологический диспансер"',
    187348: 'СПб ГБУЗ "Городской противотуберкулезный диспансер"',
    731166: 'СПб ГБУЗ "Психиатрическая больница №1 им.П.П.Кащенко"',
    187780: 'СПб ГБУЗ "Городская психиатрическая больница №7 им.акад.И.П.Павлова"',
    174172: 'СПб ГБУЗ "Пушкинский противотуберкулезный диспансер"',
    184036: 'СПб ГБУЗ "Александровская больница"',
    187204: 'СПб ГБУЗ "Городская больница №28 "Максимилиановская"',
    171580: 'СПб ГБУЗ "Введенская больница"',
    170572: 'СПб ГБУЗ "Городская больница №14"',
    187420: 'СПб ГБУЗ "Городская больница №15"',
    172156: 'СПб ГБУЗ "Клиническая ревматологическая больница №25"',
    174748: 'СПб ГБУЗ "Городская больница №26"',
    171724: 'СПб ГБУЗ "Городская больница №38 им. Н.А.Семашко"',
    182884: 'СПб ГБУЗ "Городская больница Святой преподобномученицы Елизаветы"',
    178636: 'СПб ГБУЗ "Клиническая инфекционная больница им. С.П. Боткина"',
    177628: 'СПб ГБУЗ "Городская клиническая больница №31"',
    172732: 'СПб ГБУЗ "Городская многопрофильная больница №2"',
    183820: 'СПб ГБУЗ "Городская наркологическая больница"',
    170644: 'СПб ГБУЗ "Городская Покровская больница"',
    181948: 'СПб ГБУЗ "Городская больница Святого Великомученика Георгия"',
    184540: 'СПб ГБУЗ "Городской гериатрический медико-социальный центр"',
    185476: 'СПб ГБУЗ "Городской кожно-венерологический диспансер"',
    187852: 'СПб ГБУЗ "Госпиталь для ветеранов войн"',
    173884: 'СПб ГБУЗ "Городская больница №40"',
    186556: 'СПб ГАУЗ "Хоспис (детский)"',
    186916: 'СПб ГКУЗ "Хоспис №4"',
    176260: 'СПб ГБУЗ "Городская больница Святого Праведного Иоанна Кронштадтского"',
    171508: 'СПб ГБУЗ "Городская больница №20"',
    172804: 'СПб ГБУЗ "Гериатрическая больница №1"',
    179500: 'СПб ГБУЗ "Николаевская больница"',
    181300: 'СПб ГБУЗ "Детская городская больница №22"',
    185404: "Городская больница №33",
}


def dolg_rastvor():
    SQL = """
SELECT DISTINCT
    a.RN
FROM
    PARUS.BLREPORTS r
    INNER JOIN PARUS.AGNLIST a ON r.AGENT = a.RN
    INNER JOIN PARUS.BLREPFORMED rd ON r.BLREPFORMED = rd.RN
    INNER JOIN PARUS.BLREPFORM rf ON rd.PRN = rf.RN
WHERE
    rf.code = 'Растворинф'
    AND r.BDATE BETWEEN (CURRENT_TIMESTAMP - 3) AND (CURRENT_TIMESTAMP + 2)
"""

    DF = parus_sql(SQL)

    mess = (
        "Список должников: \n"
        + " - "
        + "\n - ".join(
            [
                v
                for k, v in medical_institutions_dict.items()
                if k not in DF["RN"].unique()
            ]
        )
    )

    return mess
