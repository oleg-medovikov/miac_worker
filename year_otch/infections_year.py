from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop._05_infections_1 import infections_1
from year_otch.dop._06_infections_2 import infections_2
from year_otch.dop._07_infections_3 import infections_3
from year_otch.dop._08_infections_4 import infections_4


def infections_year():
    """традиционные инфекции"""
    dict_ = {
        "не роддома ОКИ": df_processing(infections_1),
        "не роддома ВКИ": df_processing(infections_2),
        "общ гепатит": df_processing(infections_3),
        "общ другие": df_processing(infections_4),
    }
    write_excel(infections_1.name(), dict_)
    return infections_1.name()
