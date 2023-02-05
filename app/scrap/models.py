import datetime

from sqlalchemy import (
    Column, Integer, String, ForeignKey, DateTime
)

from app.db import Base


class Scrap(Base):
    user_id = Column(String(32), ForeignKey("user.user_id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
