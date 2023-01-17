import glob
import os
from datetime import datetime, timedelta
import pandas as pd

from clas import Dir
from base import dn122_insert, dn122_exec


class my_except(Exception):
    pass


def load_table_feedback(DF: 'pd.DataFrame', DATE: str):
    "загрузка фидбека"
    DF.columns = ['md5_hash', 'FeedBackComment']
    IDs = ('0', '1', '2', '4', '5', '6')
    DF = DF.loc[DF['FeedBackComment'].str.startswith(IDs)]

    DF['FeedBackId'] = DF['FeedBackComment'].str.replace(
        r"[^\d]",
        "",
        regex=True).astype(int)

    try:
        DATE = datetime.strptime(DATE, '%Y_%m_%d')
    except:
        DATE = datetime.strptime(DATE, '%Y-%m-%d')

    DF['FeedBackDate'] = DATE

    dn122_insert(
        DF,
        'feedback_122',
        'oleg',
        False,
        'append'
            )


def update_patient():
    "запуск update таблицы пациентов"
    SQL = """
        UPDATE  P
            SET P.FeedBackId = F.FeedBackId,
                P.FeedBackComment = F.FeedBackComment,
                P.FeedBackDate = F.FeedBackDate
            FROM oleg.Patient as p
                INNER JOIN oleg.feedback_122 as F
                    ON (P.md5_hash = F.md5_hash)
    """
    dn122_exec(SQL)


def load_feed_back(DATE):
    "загрузка ответа от 122 службы, кому они дозвонились"

    P = DATE.split('-')
    DATE = f"{P[2]}-{P[1]}-{P[0]}"
    MASK = Dir.get('CARDIO') + f'/ori.cardio.122/feedback_122/{DATE}*.xlsx'

    try:
        FILE = glob.glob(MASK)[0]
    except IndexError:
        raise my_except(f'Не найден файл ответа за данное число {DATE}')

    try:
        DF = pd.read_excel(
            FILE,
            usecols=['уникальный идентификатор', 'Код ответа 122 службы'],
            dtype=str
            )
    except Exception as e:
        raise my_except(f'Не смог прочесть файл {str(e)}')

    dn122_exec('TRUNCATE TABLE oleg.feedback_122')

    load_table_feedback(DF, DATE)

    update_patient()

    return 'Готово!'


def load_feed_back_auto():
    "загрузка ответа от 122 службы автоматическая"

    delta = datetime.now() - timedelta(days=1)
    MASK = Dir.get('CARDIO') \
        + '/ori.cardio.122/feedback_122/' \
        + '[0-2]0[0-3][0-9]*[0-9][0-9]*[0-9][0-9]*.xlsx'
    dn122_exec('TRUNCATE TABLE oleg.feedback_122')

    STAT = "Пробую загрузить новые файлы от 122 службы \n\n"
    COUNT = 0

    for FILE in glob.iglob(MASK):
        time = datetime.utcfromtimestamp(os.stat(FILE).st_ctime)
        if time < delta:
            # файл слишком старый
            continue

        NAME = FILE.rsplit('/', 1)[-1]
        DATE = NAME[0:10]
        STAT += NAME + '\n'

        try:
            DF = pd.read_excel(
                FILE,
                usecols=['уникальный идентификатор', 'Код ответа 122 службы'],
                dtype=str
                )
        except ValueError:
            STAT += "не смог прочесть файл, не нашёл колонки"
            continue

        try:
            load_table_feedback(DF, DATE)
        except Exception as e:
            STAT += f'не смог загрузить файл \n {str(e)}'
        COUNT += 1
        STAT += "загрузил файл"

    if COUNT:
        update_patient()
    else:
        STAT += "Нечего загружать!"

    return STAT
