from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop._01_obstetrics_1 import obstetrics_1
from year_otch.dop._02_obstetrics_2 import obstetrics_2
from year_otch.dop._03_obstetrics_3 import obstetrics_3
from year_otch.dop._04_obstetrics_4 import obstetrics_4


def obstetrics_year():
    """родовспоможение"""
    dict_ = {
        "ДОПФ_роддома": df_processing(obstetrics_1),
        "ВБИ_роддома": df_processing(obstetrics_2),
        "ГСИ_детдома": df_processing(obstetrics_3),
        "ВУИ_детдома": df_processing(obstetrics_4),
    }
    write_excel(obstetrics_1.name(), dict_)
    return obstetrics_1.name()
