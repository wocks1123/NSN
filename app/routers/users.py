from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session

from typing import List

from app import crud
from app.auth import get_current_user
from app.deps import get_db
from app.schemas.User import UserResponse, UserCreate


router = APIRouter(prefix="/users")


@router.post("/")
def create_user(
    user_id: str = Form(...),
    password: str = Form(...),
    user_name: str = Form(...),
    email: str = Form(...),
    image_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_user = crud.user.get_by_user_id(db, user_id=user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="User ID already registered")

    file_obj = crud.media_file.create_with_file(db, image_file)[0]
    user = UserCreate(
        userId=user_id,
        password=password,
        userName=user_name,
        email=email,
        profileMessage="",
        profileImagePath=file_obj.path,
    )

    return crud.user.create(db=db, obj_in=user)


@router.get("/search/")
def search_user(
    keyword: str,
    db: Session = Depends(get_db)
):
    res = crud.user.get_search_result(db, keyword=keyword)
    return res


@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users
