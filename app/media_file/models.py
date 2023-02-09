from sqlalchemy import (
    Column, String
)

from app.db import Base
from app.models import NSNBase


class MediaFile(Base):
    identifier = Column(String(64), primary_key=True)
    saved_path = Column(String(128), nullable=False)
    file_type = Column(String(8), nullable=False)


class MediaFileBase(NSNBase):
    identifier: str
    saved_path: str
    file_type: str
