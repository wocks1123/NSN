from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.deps import get_db
from app.schemas.CommentGood import CommentGoodCreate
from app.schemas.PostGood import PostGoodCreate


router = APIRouter(prefix="/goods")


@router.post("/comment")
def create_comment_good(comment_good: CommentGoodCreate, db: Session = Depends(get_db)):
    return crud.comment_good.create(db=db, obj_in=comment_good)


@router.post("/post")
def create_comment_good(post_good: PostGoodCreate, db: Session = Depends(get_db)):
    return crud.post_good.create(db=db, obj_in=post_good)
