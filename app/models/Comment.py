from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, func, select
)
from sqlalchemy.orm import relationship, column_property

import datetime

from app.db.BaseClass import Base
from app.models.CommentGood import CommentGood


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    userId = Column(String(64), ForeignKey("user.userId"))  # FK added
    postId = Column(Integer, ForeignKey("post.id"), index=True)  # FK added
    content = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User")
    post = relationship("Post")
    goodCount = column_property(
        select([func.count(CommentGood.id)]).filter(CommentGood.commentId == id).scalar_subquery()
    )
