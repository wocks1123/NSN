from sqlalchemy import (
    Column, Integer, String, ForeignKey
)

from app.db import Base


class PostLike(Base):
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String(32), ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)


class CommentLike(Base):
    comment_id = Column(Integer, ForeignKey("comment.id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(String(32), ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True)
