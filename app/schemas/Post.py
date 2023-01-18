from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List
import json

from app.schemas.User import UserInPost
from app.schemas.Comment import CommentInPost
from app.schemas.PostMedia import PostMediaInPost


class PostBase(BaseModel):
    content: str
    goodCount: int
    commentCount: int
    created_at: datetime


class PostCreate(BaseModel):
    author_id: str
    content: str
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PostUpdate(PostBase):
    content: str


class PostInDBBase(PostBase):
    id: int
    author_id: str

    class Config:
        orm_mode = True


class Post(PostInDBBase):
    author: UserInPost
    comments: List[CommentInPost]
    images: List[PostMediaInPost]


class PostSearchResults(BaseModel):
    results: Sequence[Post]
