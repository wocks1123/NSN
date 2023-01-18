from sqlalchemy import (
    Column, Integer, String, ForeignKey
)

from app.db.BaseClass import Base


class PostGood(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    postId = Column(Integer, ForeignKey("post.id"), index=True)
    userId = Column(String(64), ForeignKey("user.userId"))  # FK added
