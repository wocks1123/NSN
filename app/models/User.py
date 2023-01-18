from sqlalchemy import Column, Integer, String

from app.db.BaseClass import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(String(64), index=True, unique=True, nullable=False)
    userName = Column(String(64), nullable=False)
    password = Column(String(32), nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    profileMessage = Column(String(128), nullable=True)
    profileImagePath = Column(String(64), nullable=True)
