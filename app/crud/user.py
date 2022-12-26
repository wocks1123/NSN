from sqlalchemy.orm import Session

from app.models.User import User
from app.schemas.User import UserResponse, UserCreate


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_user_id(db: Session, user_id: str):
    return db.query(User).filter(User.userId == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    # fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(
        userId=user.userId,
        userName=user.userName,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
