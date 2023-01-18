from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import relationship

from app.db.BaseClass import Base


class PostMedia(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    postId = Column(Integer, ForeignKey("post.id"))
    path = Column(String(64), nullable=False)
    mediaType = Column(String(8), nullable=False)   # image, video, audio, ...
    post = relationship("Post", back_populates="images")
