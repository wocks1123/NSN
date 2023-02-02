from typing import Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .models import Comment
from .schemas import (
    CommentCreate,
    CommentUpdate
)


def create(
    *,
    db_session: Session,
    comment_in: CommentCreate,
) -> Comment:
    comment = Comment(
        **comment_in.dict()
    )
    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment


def get_one_by_id(
    *,
    db_session: Session,
    comment_id: int,
) -> Optional[Comment]:
    return db_session.query(Comment).filter(Comment.id == comment_id).one_or_none()


def get_multi_by_post_id(
    *,
    db_session: Session,
    post_id: int,
    cursor: int = 0,
    reader: str = None
) -> List[Comment]:
    if cursor == 0:
        comments = db_session.query(Comment)\
                .filter(Comment.post_id == post_id) \
                .filter(Comment.post_id == post_id) \
                .order_by(Comment.created_at.desc()) \
                .limit(5).all()
    else:
        comments = db_session.query(Comment) \
            .filter(Comment.post_id == post_id) \
            .filter(Comment.post_id == post_id) \
            .filter(Comment.id < cursor) \
            .order_by(Comment.created_at.desc()) \
            .limit(5).all()

    if reader:
        for c in comments:
            c.is_liked = c.get_liked(reader)
    else:
        for c in comments:
            c.is_liked = False

    return comments


def update(
    *,
    db_session: Session,
    comment: Comment,
    comment_in: CommentUpdate,
) -> Comment:
    comment_data = jsonable_encoder(comment)
    update_data = comment_in.dict(exclude_unset=True)
    for field in comment_data:
        if field in update_data:
            setattr(comment, field, update_data[field])

    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment


def delete_by_id(
    *,
    db_session: Session,
    comment_id: int,
) -> Comment:
    comment = db_session.query(Comment).filter(Comment.id == comment_id).one_or_none()
    db_session.delete(comment)
    db_session.commit()
    return comment
