from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Enum, func, select
)
from sqlalchemy.orm import relationship, column_property

from app.core.enums import PostScope
from app.db import Base

from app.comment.models import Comment
from app.like.models import PostLike
from app.scrap.models import Scrap


class Post(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(String(32), ForeignKey("user.user_id"))
    content = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    post_scope = Column(Enum(PostScope), nullable=False, default=PostScope.ALL)

    # Relationships
    author = relationship("User")
    liked_count = column_property(
        select([func.count(PostLike.post_id)]).filter(PostLike.post_id == id).scalar_subquery()
    )
    liked = relationship(
        "User",
        secondary="postlike",
        lazy="dynamic",
    )
    comment_count = column_property(
        select([func.count(Comment.id)]).filter(Comment.post_id == id).scalar_subquery()
    )
    media = relationship("PostMedia", back_populates="post")

    scrap = relationship(
        "User",
        secondary="scrap",
        lazy="dynamic",
    )

    def get_liked(self, reader):
        return bool(self.liked.filter(PostLike.user_id == reader).first())

    def get_scrapped(self, reader):
        return bool(self.scrap.filter(Scrap.user_id == reader).first())


class PostMedia(Base):
    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    identifier = Column(String(64), primary_key=True)
    media_type = Column(String(8), nullable=False)   # image, video, audio, ...
    post = relationship("Post", back_populates="media")
