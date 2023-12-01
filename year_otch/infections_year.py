from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop._05_infections_1 import infections_1
from year_otch.dop._06_infections_2 import infections_2


def infections_year():
    """традиционные инфекции"""
    dict_ = {
        "не роддома ОКИ": df_processing(infections_1),
        "не роддома ВКИ": df_processing(infections_2),
    }
    write_excel(infections_1.name(), dict_)
    return infections_1.name()
