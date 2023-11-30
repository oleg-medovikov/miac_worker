# работа с Парусом
from .parus import parus_sql

# Работа с COVID
from .covid import covid_sql, covid_exec, covid_insert

# Работа с NsiBase
from .nsibase import nsi_sql

# Работа с MIAC_ds
from .miac_ds import miac_ds_sql, miac_ds_insert

# Работа с NCRN
from .ncrnbase import ncrn_sql, ncrn_exec, ncrn_insert

# Работа с Dn_122
from .dn122base import dn122_sql, dn122_exec, dn122_insert

from .base_ps import ps_sql

__all__ = [
    "parus_sql",
    "covid_sql",
    "covid_exec",
    "covid_insert",
    "nsi_sql",
    "miac_ds_sql",
    "miac_ds_insert",
    "ncrn_sql",
    "ncrn_exec",
    "ncrn_insert",
    "dn122_sql",
    "dn122_exec",
    "dn122_insert",
    "ps_sql",
]
