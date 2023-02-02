from typing import List, Optional

from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.core import get_db

from .schemas import (
    PostCreate,
    PostUpdate,
    PostDelete,
    PostCreateResponse,
    PostResponse,
    PostOneResponse,
    PostCardResponse
)
from .service import (
    create,
    get,
    get_one_by_post_id,
    get_multi_by_user_id,
    get_followers_posts,
    get_scrapped_posts,
    update,
    delete
)

post_router = APIRouter()


@post_router.post("/", response_model=PostCreateResponse)
async def create_post(
    post_in: PostCreate = Depends(PostCreate),
    in_files: List[UploadFile] = File(...),
    db_session: Session = Depends(get_db),
):
    return await create(db_session=db_session, post_in=post_in, media=in_files)


@post_router.get("/followers", response_model=List[PostResponse])
def read_followers_posts(
    reader: str,
    cursor: int = 0,
    db_session: Session = Depends(get_db)
):
    posts = get_followers_posts(db_session=db_session, cursor=cursor, user_id=reader)
    return posts


@post_router.get("/scraps", response_model=List[PostCardResponse])
def read_scrapped_posts(
    user_id: str,
    cursor: int = 0,
    db_session: Session = Depends(get_db)
):
    posts = get_scrapped_posts(db_session=db_session, cursor=cursor, user_id=user_id)
    return posts


@post_router.get("/users/{author_id}", response_model=List[PostCardResponse])
def read_posts_by_author(
    author_id: Optional[str] = None,
    cursor: int = 0,
    db_session: Session = Depends(get_db)
):
    return get_multi_by_user_id(db_session=db_session, cursor=cursor, author=author_id)


@post_router.get("/{post_id}", response_model=PostOneResponse)
def read_post(post_id: int, reader: str = None, db_session: Session = Depends(get_db)):
    post = get(db_session=db_session, post_id=post_id, reader=reader)
    return post


@post_router.put("/{post_id}", response_model=PostOneResponse)
def update_post(post_id: int, post_in: PostUpdate, db_session: Session = Depends(get_db)):
    post = get_one_by_post_id(db_session=db_session, post_id=post_id)
    post = update(db_session=db_session, post=post, post_in=post_in)
    return post


@post_router.delete("/{post_id}", response_model=PostOneResponse)
def delete_post(post_in: PostDelete, db_session: Session = Depends(get_db)):
    post = delete(db_session=db_session, post_in=post_in)
    return post
