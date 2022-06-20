from .system.write_styling_excel_file import write_styling_excel_file
from .system.table_one_column         import table_one_column
from .system.send_message             import bot_send_text, bot_send_file


from .admin.check_robot            import check_robot

## Парус!

from .parus.svod_4_2_covid_19      import svod_4_2_covid_19
from .parus.svod_4_3_covid_19      import svod_4_3_covid_19
from .parus.svod_26_covid_19       import svod_26_covid_19
from .parus.svod_27_covid_19       import svod_27_covid_19
from .parus.svod_27_covid_19_regiz import svod_27_covid_19_regiz
from .parus.svod_27_covid_small    import svod_27_covid_small
from .parus.svod_28_covid_19       import svod_28_covid_19
from .parus.svod_29_covid_19       import svod_29_covid_19
from .parus.svod_33_covid_19       import svod_33_covid_19
from .parus.svod_36_covid_19       import svod_36_covid_19
from .parus.svod_37_covid_19       import svod_37_covid_19
from .parus.svod_38_covid_19       import svod_38_covid_19
from .parus.svod_40_covid_19       import svod_40_covid_19
from .parus.svod_40_covid_19_dates import svod_40_covid_19_dates
from .parus.svod_43_covid_19       import svod_43_covid_19
from .parus.svod_50_covid_19       import svod_50_covid_19
from .parus.svod_51_covid_19       import svod_51_covid_19
from .parus.svod_52_covid_19       import svod_52_covid_19
from .parus.svod_53_covid_19       import svod_53_covid_19
from .parus.svod_54_covid_19       import svod_54_covid_19
from .parus.extra_izv              import extra_izv
from .parus.distant_consult        import distant_consult

## Замечания министерства здравоохранения

from .zam_mz.delete_zam_mz        import delete_zam_mz
from .zam_mz.no_snils             import no_snils
from .zam_mz.bez_izhoda           import bez_izhoda 
from .zam_mz.bez_ambulat_level    import bez_ambulat_level
from .zam_mz.no_OMS               import no_OMS
from .zam_mz.neveren_vid_lechenia import neveren_vid_lechenia
from .zam_mz.no_lab               import no_lab
from .zam_mz.net_diagnoz_covid    import net_diagnoz_covid
from .zam_mz.no_pad               import no_pad
from .zam_mz.net_dnevnik          import net_dnevnik
from .zam_mz.zavishie_statusy     import zavishie_statusy
from .zam_mz.load_snils_comment   import load_snils_comment
from .zam_mz.ivl                  import IVL
from .zam_mz.zamechania           import zamechania
from .zam_mz.zamechania_file      import zamechania_file
## Загрузки отчётов

from .loader.report_guber      import report_guber
from .loader.report_vp_and_cv  import report_vp_and_cv

functions = {
        'check_robot'             : check_robot,
        'svod_4_2_covid_19'       : svod_4_2_covid_19,
        'svod_4_3_covid_19'       : svod_4_3_covid_19,
        'svod_26_covid_19'        : svod_26_covid_19,
        'svod_27_covid_19'        : svod_27_covid_19,
        'svod_27_covid_19_regiz'  : svod_27_covid_19_regiz,
        'svod_27_covid_small'     : svod_27_covid_small,
        'svod_28_covid_19'        : svod_28_covid_19,
        'svod_29_covid_19'        : svod_29_covid_19,
        'svod_33_covid_19'        : svod_33_covid_19,
        'svod_36_covid_19'        : svod_36_covid_19,
        'svod_37_covid_19'        : svod_37_covid_19,
        'svod_38_covid_19'        : svod_38_covid_19,
        'svod_40_covid_19'        : svod_40_covid_19,
        'svod_40_covid_19_dates'  : svod_40_covid_19_dates,
        'svod_43_covid_19'        : svod_43_covid_19,
        'svod_50_covid_19'        : svod_50_covid_19,
        'svod_51_covid_19'        : svod_51_covid_19,
        'svod_52_covid_19'        : svod_52_covid_19,
        'svod_53_covid_19'        : svod_53_covid_19,
        'svod_54_covid_19'        : svod_54_covid_19,
        'extra_izv'               : extra_izv,
        'distant_consult'         : distant_consult,

        'delete_zam_mz'           : delete_zam_mz,
        'no_snils'                : no_snils,
        'bez_izhoda'              : bez_izhoda,
        'bez_ambulat_level'       : bez_ambulat_level,
        'no_OMS'                  : no_OMS,
        'neveren_vid_lechenia'    : neveren_vid_lechenia,
        'no_lab'                  : no_lab,
        'net_diagnoz_covid'       : net_diagnoz_covid,
        'no_pad'                  : no_pad,
        'net_dnevnik'             : net_dnevnik,
        'zavishie_statusy'        : zavishie_statusy,
        'load_snils_comment'      : load_snils_comment,
        'IVL'                     : IVL,
        'zamechania'              : zamechania,
        'zamechania_file'         : zamechania_file,

        'report_guber'            : report_guber,
        'report_vp_and_cv'        : report_vp_and_cv,

        }

