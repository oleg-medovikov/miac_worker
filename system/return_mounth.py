from datetime import datetime
from calendar import monthrange


def return_mounth(DATE: 'datetime'):
    "Получение дат начала и конца в виде строк"
    days = monthrange(DATE.year, DATE.month)[1]
    return f'{DATE.year}-{DATE.month}-1', f'{DATE.year}-{DATE.month}-{days}'
