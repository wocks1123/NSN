from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Enum, func, select
)
from sqlalchemy.orm import relationship, column_property
import datetime

from app.common.enums import PostScope
from app.db.BaseClass import Base
from app.models.Comment import Comment
from app.models.PostGood import PostGood


class Post(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    author_id = Column(String(64), ForeignKey("user.userId"))  # FK added
    content = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    post_scope = Column(Enum(PostScope), nullable=False, default=PostScope.ALL)

    # Relationships
    author = relationship("User")
    goodCount = column_property(
        select([func.count(PostGood.id)]).filter(PostGood.postId == id).scalar_subquery()
    )
    commentCount = column_property(
        select([func.count(Comment.id)]).filter(Comment.postId == id).scalar_subquery()
    )
    comments = relationship(
        "Comment",
        back_populates="post",
        order_by="desc(Comment.created_at)",

    )
    images = relationship("PostMedia", back_populates="post")
