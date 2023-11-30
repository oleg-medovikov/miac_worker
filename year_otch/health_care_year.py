from system import write_excel
from year_otch.df_processing import df_processing
from year_otch.dop._1_tuberculez_mp import tuberculez_mp
from year_otch.dop._2_gepatit_mp import gepatit_mp
from year_otch.dop._3_prevalent_mp import prevalent_mp
from year_otch.dop._4_inspection_gepB import inspection_gepB
from year_otch.dop._5_inspection_gepC import inspection_gepC
from year_otch.dop._6_gepB_mr import gepB_mr
from year_otch.dop._7_gepC_mr import gepC_mr
from year_otch.dop._8_travm_1 import travm_1
from year_otch.dop._9_travm_2 import travm_2


def health_care_year():
    """"""
    dict_ = {
        "Туберкулез МП": df_processing(tuberculez_mp),
        "Гепатит МП": df_processing(gepatit_mp),
        "Превалентность": df_processing(prevalent_mp),
        "Обсл. Геп. Б": df_processing(inspection_gepB),
        "Обсл. Геп. С": df_processing(inspection_gepC),
        "ГепБ МР": df_processing(gepB_mr),
        "ГепС МР": df_processing(gepC_mr),
        "Травмы 1": df_processing(travm_1),
        "Травмы 2": df_processing(travm_2),
    }
    write_excel(tuberculez_mp.name(), dict_)
    return tuberculez_mp.name()
