from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship


from app.models.ModelBase import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(Base):
    # uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(String(128), nullable=False)
    userName = Column(String(128), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
