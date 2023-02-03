from sqlalchemy.orm import Session

from .models import PostLike, CommentLike
from .schemas import (
    PostLikeCreate,
    PostLikeDelete,
    CommentLikeCreate,
    CommentLikeDelete
)


def create_post_like(
    *,
    db_session: Session,
    post_like_in: PostLikeCreate,
) -> PostLike:
    post_like = PostLike(
        **post_like_in.dict()
    )
    db_session.add(post_like)
    db_session.commit()
    db_session.refresh(post_like)
    return post_like


def delete_post_like(
    *,
    db_session: Session,
    post_like_in: PostLikeDelete,
) -> PostLike:
    post_like = db_session.query(PostLike)\
        .filter(
            PostLike.post_id == post_like_in.post_id,
            PostLike.user_id == post_like_in.user_id
        ).one_or_none()
    db_session.delete(post_like)
    db_session.commit()
    return post_like


def create_comment_like(
    *,
    db_session: Session,
    comment_like_in: CommentLikeCreate,
) -> CommentLike:
    comment_like = CommentLike(
        **comment_like_in.dict()
    )
    db_session.add(comment_like)
    db_session.commit()
    db_session.refresh(comment_like)
    return comment_like


def delete_comment_like(
    *,
    db_session: Session,
    comment_like_in: CommentLikeDelete,
) -> CommentLike:
    comment_like = db_session.query(CommentLike)\
        .filter(
            CommentLike.comment_id == comment_like_in.comment_id,
            CommentLike.user_id == comment_like_in.user_id
        ).one_or_none()
    db_session.delete(comment_like)
    db_session.commit()
    return comment_like
