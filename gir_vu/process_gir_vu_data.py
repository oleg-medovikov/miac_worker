import pandas as pd
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

from conf import MASTER, OCSANA, ANNA
from system import bot_send_text
from base import ncrn_sql, ncrn_insert

# Колонки для вставки в БД
insert_columns = [
    "local_gis_number",
    "diagnosis_mkb",
    "diagnosis_description",
    "diagnosis_type",
    "diagnosis_date",
    "medic_lastname",
    "medic_firstname",
    "medic_middlename",
    "medic_snils",
    "mo_oid",
]

# Колонки для анкетных данных
personal_columns = [
    "snils",
    "ern_id",
    "oms_number",
    "lastname",
    "firstname",
    "middlename",
    "gender",
    "birthdate",
    "document_type",
    "document_series",
    "document_number",
    "document_issue_date",
    "document_issue_name",
    "document_issue_code",
]


def truncate_data(row):
    # Обрезка до максимальной длины для каждого столбца
    row["diagnosis_description"] = str(row["diagnosis_description"])[:255]
    row["medic_firstname"] = str(row["medic_firstname"])[:50]
    row["medic_lastname"] = str(row["medic_lastname"])[:50]
    row["medic_middlename"] = str(row["medic_middlename"])[:50]
    row["diagnosis_mkb"] = str(row["diagnosis_mkb"])[:10]
    row["medic_snils"] = str(row["medic_snils"])[:12]
    return row


def process_group(args):
    """Обрабатывает одну группу независимо"""
    group, db_rows = args
    if db_rows.empty:
        # если в базе нет данных о пациенте - заливаем группу и в файл и в бд
        return group, group, len(group)

    to_save_group = pd.DataFrame()
    to_insert_group = pd.DataFrame()

    # иначе нужно разобраться с разницей

    existing_mkbs = set(db_rows["diagnosis_mkb"])
    new_mkbs = set(group["diagnosis_mkb"])

    # ищем наличие новых диагнозов
    diff_mkbs = new_mkbs - existing_mkbs
    if not diff_mkbs:
        # если нет новых диагнозов, то возвращаем ничего
        return pd.DataFrame(), pd.DataFrame(), 0

    # если есть новые диагнозы, то их нужно залить в бд
    new_rows = group.loc[group.diagnosis_mkb.isin(diff_mkbs)]
    to_insert_group = pd.concat([to_insert_group, new_rows], ignore_index=True)

    # теперь проверяем все ли диагнозы есть у пациента
    old_bd_mkbs = existing_mkbs - new_mkbs
    if old_bd_mkbs:
        # если есть, то нужно приделать им паспортные данные и добавить их к выгрузке
        old_rows = db_rows[db_rows.diagnosis_mkb.isin(old_bd_mkbs)].copy()
        sample_row = group.iloc[0]
        for col in personal_columns:
            old_rows[col] = sample_row[col]
        to_save_group = pd.concat([to_save_group, old_rows], ignore_index=True)

    # если до сих пор не вышли из функции, то в файл заливаем изначальную группу
    to_save_group = pd.concat([to_save_group, group], ignore_index=True)

    return to_save_group, to_insert_group, len(to_save_group)


def pack_groups(groups, max_rows=5000):
    """Улучшенный алгоритм упаковки с добиванием файлов мелкими группами"""
    # Разделяем группы на большие и маленькие
    big_groups = [(df, size) for df, size in groups if size > 25]
    small_groups = [(df, size) for df, size in groups if size <= 25]

    # Сортируем большие группы по убыванию, маленькие - по возрастанию
    big_groups.sort(key=lambda x: x[1], reverse=True)
    small_groups.sort(key=lambda x: x[1])

    packages = []
    current_package = []
    current_size = 0

    # Обрабатываем большие группы
    for df, size in big_groups:
        if current_size + size <= max_rows:
            current_package.append(df)
            current_size += size
        else:
            if current_package:
                packages.append(current_package)
            current_package = [df]
            current_size = size

    # "Добиваем" файлы мелкими группами
    for df, size in small_groups:
        added = False

        # Пытаемся добавить в существующие пакеты
        for i, package in enumerate(packages):
            pkg_size = sum(len(p) for p in package)
            if pkg_size + size <= max_rows:
                packages[i].append(df)
                added = True
                break

        # Если не поместилось ни в один существующий пакет
        if not added:
            if current_size + size <= max_rows:
                current_package.append(df)
                current_size += size
            else:
                packages.append(current_package)
                current_package = [df]
                current_size = size

    # Добавляем последний пакет
    if current_package:
        packages.append(current_package)

    return packages


def save_packages(packages, output_dir):
    """Сохраняет упакованные группы в CSV файлы с указанием размера в названии"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    dir_name = output_dir.rsplit("/", 1)[1]

    saved_files = []
    for i, package in enumerate(packages, 1):
        combined_df = pd.concat(package, ignore_index=True)
        num_rows = len(combined_df)
        # Форматируем номер файла с ведущими нулями
        file_idx = str(i).zfill(4)
        file_path = os.path.join(
            output_dir, f"{dir_name}_{file_idx}_{num_rows}rows.csv"
        )
        combined_df.to_csv(file_path, index=False, sep=";")
        saved_files.append(file_path)
        # print(f"Создан файл {file_path} ({num_rows} строк)")

    return saved_files


def process_gir_vu_data(df, output_dir="gir_vu_output"):
    if df.empty:
        return []

    mess = f"Начало обработки, человек: {df['local_gis_number'].nunique()}"
    for name in [MASTER, OCSANA, ANNA]:
        bot_send_text(mess, name)

    # Получаем уникальные local_gis_number
    unique_gis = df["local_gis_number"].unique().tolist()

    # Единый запрос для всех групп
    gis_list = ", ".join([f"'{gis}'" for gis in unique_gis])
    query = f"""
        SELECT DISTINCT 
            local_gis_number, diagnosis_mkb, diagnosis_description, diagnosis_type,
            diagnosis_date, medic_lastname, medic_firstname, medic_middlename,
            medic_snils, mo_oid
        FROM gir_vu 
        WHERE local_gis_number IN ({gis_list})
    """
    all_db_rows = ncrn_sql(query)
    mess = f"Получено {len(all_db_rows)} записей из БД"
    for name in [MASTER, OCSANA, ANNA]:
        bot_send_text(mess, name)

    # Создаем словарь с данными из БД
    db_dict = {}
    if not all_db_rows.empty:
        for gis, group in all_db_rows.groupby("local_gis_number"):
            db_dict[gis] = group
    else:
        db_dict = {gis: pd.DataFrame() for gis in unique_gis}

    # Подготовка аргументов для параллельной обработки
    tasks = []
    for local_gis, group in df.groupby("local_gis_number"):
        tasks.append((group, db_dict.get(local_gis, pd.DataFrame())))

    # Параллельная обработка групп
    to_save_groups = []
    to_insert_total = pd.DataFrame()

    # print("Параллельная обработка групп...")
    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(process_group, task) for task in tasks]

        for i, future in enumerate(as_completed(futures), 1):
            to_save_group, to_insert_group, group_size = future.result()

            if not to_save_group.empty:
                to_save_groups.append((to_save_group, group_size))

            if not to_insert_group.empty:
                to_insert_total = pd.concat(
                    [to_insert_total, to_insert_group], ignore_index=True
                )

            if i % 1000 == 0:
                mess = f"Обработано человек: {i}/{len(tasks)}"
                for name in [MASTER, OCSANA, ANNA]:
                    bot_send_text(mess, name)

    mess = f"Обработка завершена. Человек для сохранения: {len(to_save_groups)}"
    for name in [MASTER, OCSANA, ANNA]:
        bot_send_text(mess, name)

    # Вставка новых записей в БД
    if not to_insert_total.empty:
        to_insert_total = to_insert_total[insert_columns]
        to_insert_total = to_insert_total.apply(truncate_data, axis=1)
        ncrn_insert(
            DF=to_insert_total,
            TABLE="gir_vu",
            SCHEMA="dbo",
            INDEX=False,
            IF_EXISTS="append",
        )

    # Упаковка и сохранение групп
    if to_save_groups:
        # print("Начало упаковки групп в файлы...")
        packages = pack_groups(to_save_groups)
        # print(f"Сформировано {len(packages)} файлов для сохранения")
        saved_files = save_packages(packages, output_dir)
        # print(f"Сохранено {len(saved_files)} файлов")
        return saved_files

    # print("Нет данных для сохранения в файлы")
    return []
