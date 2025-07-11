import re

from base import replica_sql, replica_exec
from conf import MASTER
from system import bot_send_text


def get_patient_replica(dir_name):
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
    bot_send_text(mess, MASTER)

    for col in [
        "lastname",
        "firstname",
        "middlename",
        "medic_lastname",
        "medic_firstname",
        "medic_middlename",
    ]:
        df[col] = df[col].fillna("").str.replace(r"[^а-яА-ЯёЁ\s]", "", regex=True)

    return df
