from starlette.config import Config

config = Config('../.config/bot/.conf')

TELEGRAM_API   = config('TELEGRAM_API',   cast=str)
MIAC_API_URL = config('MIAC_API_URL', cast=str)
TOKEN = config('TOKEN', cast=str) 

DATABASE_PARUS  = config('DATABASE_PARUS',  cast=str)
ORACLE_HOME     = config('ORACLE_HOME',     cast=str)
LD_LIBRARY_PATH = config('LD_LIBRARY_PATH', cast=str)

DATABASE_COVID     = config('DATABASE_COVID',    cast=str)
DATABASE_MIAC_DS   = config('DATABASE_MIAC_DS',  cast=str)
DATABASE_NSI       = config('DATABASE_NSI',      cast=str)

URL_870 = config('URL_870', cast=str)
REGIZ_AUTH = config('REGIZ_AUTH', cast=str)
