from typing import Optional, List

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.core.enums import PostScope
from app.media_file import service as media_file_service
from app.follow.models import Follow
from app.scrap.models import Scrap

from app.comment import service as comment_service

from .models import (
    Post,
    PostMedia
)
from .schemas import (
    PostCreate,
    PostUpdate,
    PostDelete
)


async def create(
    *,
    db_session: Session,
    post_in: PostCreate,
    media: List[UploadFile]
) -> Post:
    media_files = await media_file_service.handle_file_upload(
        db_session=db_session,
        in_file=media
    )

    post = Post(
        **post_in.dict()
    )

    db_session.add(post)
    db_session.flush()

    post_media = []
    files = media_files if isinstance(media_files, List) else [media_files]
    for media_file in files:
        post_media.append(
            PostMedia(
                post_id=post.id,
                identifier=media_file.identifier,
                media_type=media_file.file_type
            )
        )
    db_session.bulk_save_objects(post_media)
    db_session.commit()
    db_session.refresh(post)
    return post


def get(
    *,
    db_session: Session,
    post_id: int,
    reader: str = None
) -> Optional[Post]:
    post = db_session.query(Post).filter(Post.id == post_id).one_or_none()
    comments = comment_service.get_multi_by_post_id(
        db_session=db_session,
        cursor=0,
        post_id=post_id,
        reader=reader
    )
    is_liked = False
    scrapped = False
    if reader:
        is_liked = post.get_liked(reader)
        scrapped = post.get_scrapped(reader)

    post.is_liked = is_liked
    post.scrapped = scrapped
    post.comments = comments
    return post


def get_one_by_post_id(
    *,
    db_session: Session,
    post_id: int,
) -> Optional[Post]:
    post = db_session.query(Post).filter(Post.id == post_id).one_or_none()
    return post


def get_multi_by_user_id(
    *,
    db_session: Session,
    cursor: int,
    author: Optional[str] = None
) -> List[Optional[Post]]:
    if author:
        if cursor == 0:
            posts = db_session.query(Post) \
                .order_by(Post.created_at.desc()) \
                .filter(Post.author_id == author).limit(9).all()

        else:
            posts = db_session.query(Post) \
                .order_by(Post.created_at.desc()) \
                .filter(Post.id < cursor) \
                .filter(Post.author_id == author).limit(6).all()
    else:
        if cursor == 0:
            posts = db_session.query(Post) \
                .order_by(Post.created_at.desc()) \
                .limit(6).all()

        else:
            posts = db_session.query(Post) \
                .order_by(Post.created_at.desc()) \
                .filter(Post.id < cursor) \
                .limit(6).all()

    return posts


def get_followers_posts(
    *,
    db_session: Session,
    cursor: int,
    user_id: str
) -> List[Post]:
    if cursor == 0:
        posts = db_session.query(Post) \
            .join(Follow, Post.author_id == Follow.to_user_id) \
            .filter(Follow.from_user_id == user_id) \
            .filter((Post.post_scope == PostScope.ALL) | (Post.post_scope == PostScope.FOLLOW)) \
            .order_by(Post.created_at.desc()) \
            .all()
    else:
        posts = db_session.query(Post) \
            .join(Follow, Post.author_id == Follow.to_user_id) \
            .filter(Follow.from_user_id == user_id) \
            .filter(Post.id < cursor) \
            .filter((Post.post_scope == PostScope.ALL) | (Post.post_scope == PostScope.FOLLOW)) \
            .order_by(Post.created_at.desc()) \
            .all()

    for post in posts:
        post.is_liked = post.get_liked(user_id)
        post.scrapped = post.get_scrapped(user_id)
    return posts


def get_scrapped_posts(
    *,
    db_session: Session,
    cursor: int, user_id: str
) -> List[Post]:
    if cursor == 0:
        posts = db_session.query(Post) \
            .join(Scrap, Post.id == Scrap.post_id) \
            .filter(Scrap.user_id == user_id) \
            .order_by(Scrap.created_at.desc()) \
            .all()
    else:
        posts = db_session.query(Post) \
            .join(Scrap, Post.id == Scrap.post_id) \
            .filter(Scrap.user_id == user_id) \
            .filter(Post.id < cursor) \
            .order_by(Scrap.created_at.desc()) \
            .all()

    for post in posts:
        post.is_liked = post.get_liked(user_id)
        post.scrapped = post.get_scrapped(user_id)
    return posts


def update(
    *,
    db_session: Session,
    post: Post,
    post_in: PostUpdate
) -> Post:
    post_data = jsonable_encoder(post)
    update_data = post_in.dict(exclude_unset=True)
    for field in post_data:
        if field in update_data:
            setattr(post, field, update_data[field])

    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post


def delete(
    *,
    db_session: Session,
    post_in: PostDelete
) -> Post:
    post = db_session.query(Post) \
        .filter(Post.id == post_in.id).one_or_none()
    db_session.delete(post)
    db_session.commit()
    return post
