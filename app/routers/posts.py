from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from typing import List, Union

from app import crud
from app.auth import get_current_user
from app.deps import get_db
from app.schemas.Post import Post, PostCreate
from app.schemas.PostMedia import PostMediaCreate


router = APIRouter(prefix="/posts")


@router.get("/", response_model=List[Post])
def read_posts(cursor: int = 0, db: Session = Depends(get_db)):
    posts = crud.post.get_multi_date_desc(db, cursor=cursor)
    return posts


@router.get("/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.post.get(db, post_id)
    return post


@router.post("/")
def create_post(
    content: str = Form(...),
    in_files: Union[List[UploadFile], None] = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_user_id(db, user_id=user.get("user_id"))
    if not db_user:
        raise HTTPException(status_code=422, detail="Email already registered")

    post_create = PostCreate(author_id=db_user.userId, content=content)
    db_post = crud.post.create(db, obj_in=post_create)
    if in_files:
        file_objs = crud.media_file.create_with_file(db, in_files)

        schms = []
        for obj in file_objs:
            schms.append(PostMediaCreate(postId=db_post.id, path=obj.path, mediaType=obj.fileType))
        crud.post_media.create_bulk(db, schms)

    return db_post
