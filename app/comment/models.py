import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, func, select
)
from sqlalchemy.orm import relationship, column_property

from app.db import Base
from app.like.models import CommentLike


class Comment(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(String(32), ForeignKey("user.user_id"))
    post_id = Column(Integer, ForeignKey("post.id"), index=True)
    content = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)

    # Relationships
    author = relationship("User")
    liked_count = column_property(
        select([func.count(CommentLike.comment_id)]).filter(CommentLike.comment_id == id).scalar_subquery()
    )
    liked = relationship(
        "User",
        secondary="commentlike",
        lazy="dynamic",
    )

    def get_liked(self, reader):
        return bool(self.liked.filter(CommentLike.user_id == reader).first())
