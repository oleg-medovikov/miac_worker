from datetime import datetime, timedelta


def return_weekday(date: 'datetime', weekday: int) -> str:
    """возвращает дату ближайшей среды или другого дня недели в виде строки"""
    day = date + timedelta(days=(weekday - date.weekday()))
    return day.strftime('%d.%m.%Y')
