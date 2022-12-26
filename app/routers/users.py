from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from typing import List

from app.database import get_db
from app.models.User import User
from app.schemas.User import UserResponse, UserCreate
import app.crud.user as UserSchema


router = APIRouter(prefix="/users")


@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserSchema.get_user_by_user_id(db, user_id=user.userId)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserSchema.create_user(db=db, user=user)


@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = UserSchema.get_users(db, skip=skip, limit=limit)
    return users
