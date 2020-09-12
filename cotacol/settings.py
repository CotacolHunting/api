from starlette.config import Config
from starlette.datastructures import Secret


config = Config(".env")

DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", cast=Secret)

DATABASE_URL = config("DATABASE_URL", cast=str)

ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=150)

STRAVA_CLIENT_ID = config("STRAVA_CLIENT_ID", cast=int)
STRAVA_CLIENT_SECRET = config("STRAVA_CLIENT_SECRET", cast=str)
STRAVA_API_BASE_URL = "https://www.strava.com/api/v3"
