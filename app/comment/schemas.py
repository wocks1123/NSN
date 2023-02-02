from datetime import datetime

from app.models import NSNBase
from app.auth.schemas import UserCardResponse


class CommentBase(NSNBase):
    author_id: str
    post_id: int
    content: str


class CommentCreate(CommentBase):
    author_id: str
    post_id: int
    content: str


class CommentUpdate(NSNBase):
    content: str


class CommentResponse(CommentBase):
    id: int
    author_id: str
    post_id: int
    content: str
    created_at: datetime
    author: UserCardResponse
    liked_count: int


class CommentCard(CommentBase):
    id: int
    author_id: str
    post_id: int
    content: str
    created_at: datetime
    author: UserCardResponse
    liked_count: int
    is_liked: bool
