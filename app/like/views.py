from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.core import get_db

from .schemas import (
    PostLikeCreate,
    PostLikeDelete,
    PostLikeRead,
    CommentLikeCreate,
    CommentLikeDelete,
    CommentLikeRead
)
from .service import (
    create_post_like,
    delete_post_like,
    create_comment_like,
    delete_comment_like
)


like_router = APIRouter()


@like_router.post("/post", response_model=PostLikeRead)
def add_post_like(post_like_in: PostLikeCreate, db_session: Session = Depends(get_db)):
    return create_post_like(db_session=db_session, post_like_in=post_like_in)


@like_router.delete("/post", response_model=PostLikeRead)
def remove_post_like(post_like_in: PostLikeDelete, db_session: Session = Depends(get_db)):
    return delete_post_like(db_session=db_session, post_like_in=post_like_in)


@like_router.post("/comment", response_model=CommentLikeRead)
def add_comment_like(comment_like_in: CommentLikeCreate, db_session: Session = Depends(get_db)):
    return create_comment_like(db_session=db_session, comment_like_in=comment_like_in)


@like_router.delete("/comment", response_model=CommentLikeRead)
def remove_comment_like(comment_like_in: CommentLikeDelete, db_session: Session = Depends(get_db)):
    return delete_comment_like(db_session=db_session, comment_like_in=comment_like_in)
