from sqlalchemy import (
    Column, Integer, String
)

from app.db.BaseClass import Base


class MediaFile(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    path = Column(String(64), index=True, nullable=False)
    savedPath = Column(String(128), nullable=False)
    fileType = Column(String(8), nullable=False)
