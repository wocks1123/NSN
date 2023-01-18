from sqlalchemy import (
    Column, Integer, String, ForeignKey
)

from app.db.BaseClass import Base


class CommentGood(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    commentId = Column(Integer, ForeignKey("comment.id"), index=True)
    userId = Column(String(64), ForeignKey("user.userId"))  # FK added
