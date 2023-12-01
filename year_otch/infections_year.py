from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop._05_infections_1 import infections_1


def infections_year():
    """традиционные инфекции"""
    dict_ = {
        "не роддома ОКИ": df_processing(infections_1),
    }
    write_excel(infections_1.name(), dict_)
    return infections_1.name()
