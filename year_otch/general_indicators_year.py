from base import parus_sql
from clas import SQL_otchet
from pandas import DataFrame

from system import write_excel
from year_otch.dop.info_NRD import info_NRD
from year_otch.dop.pap_NRD import pap_NRD
from year_otch.dop.staf_GEN import staf_GEN
from year_otch.dop.operation_count_GEN import operation_count_GEN
from year_otch.dop.risk_factor_GEN import risk_factor_GEN


def _df_processing(otchet: "SQL_otchet") -> "DataFrame":
    otchet.update_sql()
    df = parus_sql(otchet.sql)
    df.POKAZATEL = df.POKAZATEL.map(otchet.pokazatel)
    df = df.pivot_table(**otchet.pivot).stack(0)
    df = df.reset_index()
    for col in otchet.del_col:
        try:
            del df[col]
        except KeyError:
            continue
    return df


def general_indicators_year():
    """"""
    files = []

    dict_ = {  # Инфконтроль НРД
        "показатели НРД": _df_processing(info_NRD),
        "пап НРД": _df_processing(pap_NRD),
    }
    write_excel(info_NRD.name(), dict_)
    files.append(info_NRD.name())
    dict_ = {  # Инфоконтроль Общий
        "штат": _df_processing(staf_GEN),
        "количество операций": _df_processing(operation_count_GEN),
        "факторы риска": _df_processing(risk_factor_GEN),
    }
    write_excel(staf_GEN.name(), dict_)
    files.append(staf_GEN.name())

    return "".join(_ + ";" for _ in files)
