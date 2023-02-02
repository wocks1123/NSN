import json

from pydantic import BaseSettings, validator


class GlobalSettings(BaseSettings):
    APP_ENV: str = 'dev'
    ENV_STATE: str = 'dev'

    @validator("*", pre=True)
    def evaluate_lazy_columns(cls, v):
        if isinstance(v, str) and v.startswith("["):
            return json.loads(v)
        return v

    class Config:
        env_file = '.env'


class DevSettings(GlobalSettings):
    PROJECT_NAME: str

    # DB SETTING
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    AUTO_COMMIT: bool = False
    DB_ECHO: bool = True

    # AUTH
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    CORS_ALLOW_ORIGIN: list | str

    PORT: int
    DEBUG: bool
    HOST: str

    MEDIA_ROOT_PATH: str

    class Config:
        env_file = '.dev.env'


class ProdSettings(GlobalSettings):
    PROJECT_NAME: str

    # DB SETTING
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    AUTO_COMMIT: bool = False
    DB_ECHO: bool = True

    # AUTH
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    CORS_ALLOW_ORIGIN: list | str

    PORT: int
    DEBUG: bool
    HOST: str

    MEDIA_ROOT_PATH: str

    class Config:
        env_file = '.prod.env'


class FactorySettings:
    @staticmethod
    def load():
        env_state = GlobalSettings().ENV_STATE
        if env_state == 'dev':
            return DevSettings()
        elif env_state == 'prod':
            return ProdSettings()


settings = FactorySettings.load()
