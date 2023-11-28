from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop._1_tuberculez_mp import tuberculez_mp
from year_otch.dop._2_gepatit_mp import gepatit_mp
from year_otch.dop._3_prevalent_mp import prevalent_mp
from year_otch.dop._4_inspection_gepB import inspection_gepB


def health_care_year():
    """"""
    dict_ = {
        "Туберкулез МП": df_processing(tuberculez_mp),
        "Гепатит МП": df_processing(gepatit_mp),
        "Превалентность": df_processing(prevalent_mp),
        "Обсл. Геп. Б": df_processing(inspection_gepB),
    }
    write_excel(tuberculez_mp.name(), dict_)
    return tuberculez_mp.name()
