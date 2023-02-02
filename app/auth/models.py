from datetime import datetime, timedelta

import bcrypt
from jose import jwt
from sqlalchemy import Column, Integer, String, func, select
from sqlalchemy.orm import column_property, relationship

from app.core.config import settings
from app.db import Base
from app.follow.models import Follow
from app.post.models import Post


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(32), index=True, unique=True, nullable=False)
    user_name = Column(String(32), nullable=False)
    password = Column(String(64), nullable=False)
    email = Column(String(32), unique=True, nullable=False)
    profile_message = Column(String(128), nullable=False, default="")
    profile_image_path = Column(String(64), nullable=False, default="")
    post_count = column_property(
        select([func.count(Post.id)])
        .filter(Post.author_id == user_id)
        .scalar_subquery()
    )
    following_count = column_property(
        select([func.count(Follow.from_user_id)])
        .filter(Follow.from_user_id == user_id)
        .scalar_subquery()
    )
    follower_count = column_property(
        select([func.count(Follow.to_user_id)])
        .filter(Follow.to_user_id == user_id)
        .scalar_subquery()
    )

    scraps = relationship(
        "Post",
        secondary="scrap",
        lazy="dynamic",
    )

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode())

    @property
    def token(self):
        now = datetime.now()
        exp = (now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        data = {
            "exp": exp,
            "user_id": self.user_id,
        }
        return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
