import os
from datetime import datetime, timedelta

from .get_ogranizations_dict import get_organizations_dict
from .get_patient_replica import get_patient_replica
from .process_gir_vu_data import process_gir_vu_data


def gir_vu_vs1():
    mapping_dict = get_organizations_dict()

    # Путь к корневой директории
    root = "/mnt/gir_vu/vs_1"
    dir_name = (datetime.today() - timedelta(days=3)).strftime("%Y-%m-%d")
    full_path = os.path.join(root, dir_name)

    df = get_patient_replica(dir_name)

    # подставляем oid организаций
    try:
        df["mo_oid"] = df["org_key_to_oid"].astype(str).map(mapping_dict)  # type: ignore
        del df["org_key_to_oid"]  # type: ignore
    except Exception as e:
        return str(e)

    saved_files = process_gir_vu_data(df, full_path)

    mess = "Результат:"
    for file_path in saved_files:
        mess += f"\n - {os.path.basename(file_path)}"

    return mess
