from typing import Optional

from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.media_file import service as media_file_service

from .models import (
    User
)
from .schemas import (
    UserRegister,
    UserUpdate,
    PasswordUpdate,
    hash_password
)


async def create(*, db_session: Session, user_in: UserRegister, profile_image: Optional[UploadFile]) -> User:
    profile_image_path = "default_profile"
    if profile_image:
        media_file = await media_file_service.handle_file_upload(
            db_session=db_session,
            in_file=profile_image
        )
        profile_image_path = media_file.identifier

    # create the user
    user = User(
        **user_in.dict(),
        profile_image_path=profile_image_path
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def get_by_user_id(*, db_session: Session, user_id: str) -> Optional[User]:
    return db_session.query(User).filter(User.user_id == user_id).one_or_none()


def get_search_result(*, db_session: Session, keyword: str):
    return db_session.query(User)\
        .filter(User.user_id.contains(keyword))\
        .all()


def update(*, db_session: Session, user: User, user_in: UserUpdate) -> User:
    user_data = jsonable_encoder(user)
    update_data = user_in.dict(
        exclude={"password"}, exclude_unset=True
    )
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def update_password(*, db_session: Session, user: User, user_in: PasswordUpdate) -> User:
    user.password = hash_password(user_in.password)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user
