from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = 'NSN'

    # DB SETTING
    DB_USER: str = "root"
    DB_PASSWORD: str = "qwe123"
    DB_HOST: str = "localhost:3306"
    DB_NAME: str = "nsn"
    AUTO_COMMIT = False
    DB_ECHO = True

    # AUTH
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    CORS_ALLOW_ORIGIN = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:4000",
     ]

    PORT: int = 8000
    DEBUG: bool = True
    HOST: str = 'localhost'

    MEDIA_ROOT_PATH = "/mnt/d/data/img"


settings = Settings()
