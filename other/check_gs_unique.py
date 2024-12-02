import pandas as pd
import glob
import os


def check_gs_unique():
    # Базовый путь к папкам организаций
    base_path = "/mnt/lab/2024 год/КИС ЕМИАС/ПРОФИЛЬ лабораторий/Ответы МО/02.12.2024_работа над ошибками_для МОЕ"

    # Получение списка папок организаций
    organizations = [
        d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))
    ]
    mess = ""
    # Проход по каждой организации
    for org in organizations:
        # Полный путь к папке организации
        org_path = os.path.join(base_path, org)

        # Поиск всех файлов в папке организации
        files = glob.glob(
            os.path.join(org_path, "*.xlsx")
        )  # Предполагается, что файлы в формате Excel

        # Словарь для хранения кодов ГС из каждого файла
        codes_dict = {}

        # Чтение каждого файла и извлечение кодов ГС
        for file in files:
            df = pd.read_excel(file)  # Предполагается, что файлы в формате Excel
            codes = df["Код ГС"].tolist()
            codes_dict[file] = codes

        # Создание множества для хранения всех кодов ГС
        all_codes = set()

        # Создание множества для хранения дубликатов
        duplicates = set()

        # Проверка на дубликаты
        for file, codes in codes_dict.items():
            for code in codes:
                if code in all_codes:
                    duplicates.add(code)
                else:
                    all_codes.add(code)

        # Формирование текстового сообщения для текущей организации
        mess += f"\nОрганизация {org} - найдено {len(duplicates)} не уникальных кодов."

        # Создание DataFrame для сохранения результатов
        if duplicates:
            result_df = pd.DataFrame({"Не уникальные коды ГС": list(duplicates)})
        else:
            result_df = pd.DataFrame({"Не уникальные коды ГС": []})

        # Сохранение результатов в файл Excel
        output_file = os.path.join(org_path, f"результаты_проверки_{org}.xlsx")
        result_df.to_excel(output_file, index=False)

    return mess
