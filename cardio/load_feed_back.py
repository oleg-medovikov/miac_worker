import glob
from datetime import datetime
import pandas as pd

from clas import Dir
from base import dn122_insert, dn122_exec

class my_except(Exception):
    pass


def load_feed_back(DATE):
    "загрузка ответа от 122 службы, кому они дозвонились"

    P = DATE.split('-')
    DATE = f"{P[2]}_{P[1]}_{P[0]}"
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

    DF.columns = ['md5_hash', 'FeedBackComment']

    DF['FeedBackId'] = DF['FeedBackComment'].str.replace(
        r"[^\d]",
        "",
        regex=True).astype(int)
    DF['FeedBackDate'] = datetime.strptime(DATE, '%Y_%m_%d')

    dn122_insert(
        DF,
        'feedback_122',
        'oleg',
        False,
        'replace'
            )
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

    return 'Готово!'
