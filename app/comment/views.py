from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.core import get_db

from .schemas import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentCard
)
from .service import (
    create,
    get_one_by_id,
    get_multi_by_post_id,
    update,
    delete_by_id
)


comment_router = APIRouter()


@comment_router.post("/", response_model=CommentResponse)
def create_comment(
    comment_in: CommentCreate,
    db_session: Session = Depends(get_db)
):
    return create(db_session=db_session, comment_in=comment_in)


@comment_router.get("/", response_model=List[CommentCard])
def read_comments(
    post_id: int,
    cursor: int = 0,
    reader: str = None,
    db_session: Session = Depends(get_db)
):
    return get_multi_by_post_id(db_session=db_session, cursor=cursor, post_id=post_id, reader=reader)


@comment_router.put("/", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    db_session: Session = Depends(get_db)
):
    comment = get_one_by_id(db_session=db_session, comment_id=comment_id)
    return update(db_session=db_session, comment=comment, comment_in=comment_in)


@comment_router.delete("/", response_model=CommentResponse)
def delete_comment(
    comment_id: int,
    db_session: Session = Depends(get_db)
):
    return delete_by_id(db_session=db_session, comment_id=comment_id)
