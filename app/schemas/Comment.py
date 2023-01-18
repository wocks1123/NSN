from pydantic import BaseModel
from datetime import datetime

from app.schemas.User import UserInPost


class CommentBase(BaseModel):
    userId: str
    postId: int
    content: str
    created_at: datetime


class CommentCreate(BaseModel):
    userId: str
    postId: int
    content: str


class CommentUpdate(CommentBase):
    ...


class CommentInPost(CommentBase):
    user: UserInPost
    goodCount: int

    class Config:
        orm_mode = True
