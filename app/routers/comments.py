from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from typing import List

from app import crud
from app.deps import get_db
from app.schemas.Comment import CommentCreate, CommentInPost


router = APIRouter(prefix="/comments")


@router.get("/", response_model=List[CommentInPost])
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    comments = crud.comment.get_multi(db, skip=skip, limit=limit)
    return comments


@router.post("/")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = crud.comment.create(db, obj_in=comment)
    return db_comment
