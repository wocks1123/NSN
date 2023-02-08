from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.core.enums import PostScope
from app.models import NSNBase, form_body
from app.auth.schemas import UserReadInPost
from app.comment.schemas import CommentCard


class PostBase(NSNBase):
    author_id: str
    content: str
    post_scope: PostScope


class PostMediaBase(NSNBase):
    post_id: int
    identifier: str
    media_type: str


@form_body
class PostCreate(BaseModel):
    author_id: str
    content: str
    post_scope: PostScope


class PostUpdate(BaseModel):
    id: int
    content: str
    post_scope: PostScope


class PostDelete(NSNBase):
    id: int


class PostCreateResponse(NSNBase):
    id: int
    author_id: str
    content: str
    created_at: datetime
    post_scope: PostScope
    media: List[PostMediaBase]


class PostResponse(NSNBase):
    id: int
    content: str
    post_scope: PostScope
    author: UserReadInPost
    liked_count: int
    is_liked: bool
    scrapped: bool
    comment_count: int
    media: List[PostMediaBase]


class PostOneResponse(NSNBase):
    id: int
    content: str
    post_scope: PostScope
    author: UserReadInPost
    liked_count: int
    is_liked: bool
    scrapped: bool
    comment_count: int
    comments: List[CommentCard]
    media: List[PostMediaBase]


class PostCardResponse(NSNBase):
    id: int
    content: str
    post_scope: PostScope
    author: UserReadInPost
    liked_count: int
    comment_count: int
    media: List[PostMediaBase]


class PostDeleteResponse(NSNBase):
    id: int
