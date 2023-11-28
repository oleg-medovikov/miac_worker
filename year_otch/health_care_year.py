from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop._1_tuberculez_mp import tuberculez_mp
from year_otch.dop._2_gepatit_mp import gepatit_mp


def health_care_year():
    """"""
    files = []

    dict_ = {
        "Туберкулез МР": df_processing(tuberculez_mp),
        "Гепатит МР": df_processing(gepatit_mp),
    }
    write_excel(tuberculez_mp.name(), dict_)
    files.append(tuberculez_mp.name())

    return "".join(_ + ";" for _ in files)
