from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


DB_USER = "root"
DB_PASSWORD = "qwe123"
DB_HOST = "localhost:3306"
DB_NAME = "nsn"

DATABASE = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME,
)

engine = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=True
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)
