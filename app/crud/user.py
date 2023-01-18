from sqlalchemy.orm import Session

from typing import Optional

from app.models import User
from app.schemas.User import UserCreate, UserUpdate
from app.crud.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_user_id(self, db: Session, user_id: str):
        return db.query(User).filter(User.userId == user_id).first()

    def get_search_result(self, db: Session, keyword: str):
        return db.query(User)\
            .filter(User.userId.contains(keyword))\
            .all()


user = CRUDUser(User)
