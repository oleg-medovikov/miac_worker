from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop.info_NRD import info_NRD
from year_otch.dop.pap_NRD import pap_NRD
from year_otch.dop.staf_GEN import staf_GEN
from year_otch.dop.operation_count_GEN import operation_count_GEN
from year_otch.dop.risk_factor_GEN import risk_factor_GEN
from year_otch.dop.info_RD import info_RD
from year_otch.dop.pap_RD import pap_RD


def general_indicators_year():
    """"""
    files = []

    dict_ = {  # Инфконтроль НРД
        "показатели НРД": df_processing(info_NRD),
        "пап НРД": df_processing(pap_NRD),
    }
    write_excel(info_NRD.name(), dict_)
    files.append(info_NRD.name())
    dict_ = {  # Инфоконтроль Общий
        "штат": df_processing(staf_GEN),
        "количество операций": df_processing(operation_count_GEN),
        "факторы риска": df_processing(risk_factor_GEN),
    }
    write_excel(staf_GEN.name(), dict_)
    files.append(staf_GEN.name())
    dict_ = {  # Инфконтроль РД
        "показатели РД": df_processing(info_RD),
        "пап РД": df_processing(pap_RD),
    }
    write_excel(info_RD.name(), dict_)
    files.append(info_RD.name())

    return "".join(_ + ";" for _ in files)
