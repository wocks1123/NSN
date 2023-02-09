from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from app.core.config import settings


DATABASE = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8' % (
    settings.DB_USER,
    settings.DB_PASSWORD,
    settings.DB_HOST,
    settings.DB_NAME,
)

engine = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=settings.DB_ECHO
)

SessionLocal = scoped_session(
    sessionmaker(
        autocommit=settings.AUTO_COMMIT,
        autoflush=False,
        bind=engine
    )
)
