from sqlalchemy.orm import Session

from typing import Any, Dict, Optional, Union

from app.crud.base import CRUDBase
from app.models.Comment import Comment
from app.schemas.Comment import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):

    def get_recent_by_post_id(self, db: Session, *, post_id: int):
        return db.query(Comment).filter(Comment.postId == post_id).limit(5)


comment = CRUDComment(Comment)
