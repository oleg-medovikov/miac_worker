from starlette.config import Config

config = Config("../.config/bot/.conf")

TELEGRAM_API = config("TELEGRAM_API", cast=str)
MIAC_API_URL = config("MIAC_API_URL", cast=str)
TOKEN = config("TOKEN", cast=str)

DATABASE_PARUS = config("DATABASE_PARUS", cast=str)
ORACLE_HOME = config("ORACLE_HOME", cast=str)
LD_LIBRARY_PATH = config("LD_LIBRARY_PATH", cast=str)

DATABASE_COVID = config("DATABASE_COVID", cast=str)
DATABASE_MIAC_DS = config("DATABASE_MIAC_DS", cast=str)
DATABASE_NSI = config("DATABASE_NSI", cast=str)
DATABASE_NCRN = config("DATABASE_NCRN", cast=str)
DATABASE_DN122 = config("DATABASE_DN122", cast=str)

DATABASE_PS = config("DATABASE_POSTGRESS", cast=str)

URL_870 = config("URL_870", cast=str)
REGIZ_AUTH = config("REGIZ_AUTH", cast=str)
NSIUI_URL = config("NSIUI_URL", cast=str)

DADATA_TOKEN = config("dadata_token", cast=str)
DADATA_SECRET = config("dadata_secret", cast=str)

MASTER = config("MASTER", cast=int)
