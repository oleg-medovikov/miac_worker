import re

from base import replica_sql, replica_exec
from conf import MASTER, OCSANA, ANNA
from system import bot_send_text


def get_patient_replica(dir_name):
    mess = f"Начинаю выполнять получение данных для ГИР ВУ SV1 на дату: { dir_name }"
    for name in [MASTER, OCSANA, ANNA]:
        bot_send_text(mess, name)

    with open("./gir_vu/sql.txt", "r", encoding="utf-8") as file:
        sql = file.read()

    sql = sql.replace("__DATE__", dir_name)
    sql = re.sub(r"--.*$", "", sql, flags=re.MULTILINE)  # Однострочные комментарии
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)  # Многострочные комментарии

    # --- Разделяем запросы по точке с запятой ---
    queries = [q.strip() for q in sql.split(";") if q.strip()]

    # --- Выполняем все запросы  ---
    for query in queries:
        try:
            if query:
                replica_exec(query)
        except Exception as e:
            print(
                f"Ошибка выполнения запроса:\n{query[:100]}...\nОшибка: {str(e)[:200]}"
            )
    try:
        df = replica_sql("SELECT * FROM tmp_gir_vu_final")
    except Exception as e:
        print(f"Ошибка в финальном запросе:... {str(e)[:200]}")
        df = []

    # --- Шаг 8: Выводим результат ---
    mess = f"Успешно получено строк:{ len(df) }"
    for name in [MASTER, OCSANA, ANNA]:
        bot_send_text(mess, name)

    for col in [
        "lastname",
        "firstname",
        "middlename",
        "medic_lastname",
        "medic_firstname",
        "medic_middlename",
        "diagnosis_description",
    ]:
        # Преобразование в строковый тип для надежности
        df[col] = df[col].astype(str)  # type: ignore

        # Замена пустых значений и специальных маркеров
        df[col] = df[col].replace(r"^(nan|NaN|None|\s*)$", "не указано", regex=True)  # type: ignore

        # Удаление не-кириллических символов
        df[col] = df[col].str.replace(r"[^а-яА-ЯёЁ\s]", "", regex=True)  # type: ignore

        # Схлопывание множественных пробелов в один
        df[col] = df[col].str.replace(r"\s+", " ", regex=True)  # type: ignore

        # Фильтрация оставшихся пустых значений
        df[col] = df[col].apply(lambda x: "не указано" if x.strip() == "" else x)  # type: ignore

    return df
