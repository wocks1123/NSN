from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from pydantic.error_wrappers import ErrorWrapper, ValidationError

from app.db.core import get_db

from .schemas import (
    JWTUser,
    UserRead,
    UserLogin,
    UserLoginResponse,
    UserRegister,
    UserRegisterResponse,
    UserUpdate,
    PasswordUpdate,
    UserProfileResponse,
    UserCardResponse
)
from .service import (
    create,
    get_by_user_id,
    get_search_result,
    update,
    update_password
)
from .exeptions import (
    InvalidUsernameError,
    InvalidPasswordError,
    InvalidConfigurationError
)
from .security import get_current_user

from app.follow import service as follow_service
from app.follow.schemas import FollowRead


user_router = APIRouter()
auth_router = APIRouter()


@user_router.get("/me", response_model=UserRead)
def read_users(
    current_user: JWTUser = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    db_user = get_by_user_id(db_session=db_session, user_id=current_user.user_id)
    return db_user


@user_router.get("/search", response_model=List[UserCardResponse])
def search_user(
    keyword: str,
    db_session: Session = Depends(get_db)
):
    res = get_search_result(db_session=db_session, keyword=keyword)
    return res


@user_router.get("/{user_id}", response_model=UserProfileResponse)
def get_user(user_id: str, reader: str = None, db_session: Session = Depends(get_db)):
    user = get_by_user_id(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )
    followed = False
    if reader:
        follow_in = FollowRead(
            from_user_id=reader,
            to_user_id=user_id
        )
        followed = bool(follow_service.get(db_session=db_session, follow_in=follow_in))
    user.followed = followed
    return user


@user_router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    user_in: UserUpdate,
    # current_user: JWTUser = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    user = get_by_user_id(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )

    return update(db_session=db_session, user=user, user_in=user_in)


@user_router.put("/{user_id}/password", response_model=UserRead)
def change_password(
    user_id: str,
    user_in: PasswordUpdate,
    # current_user: JWTUser = Depends(get_current_user),
    db_session: Session = Depends(get_db)
):
    user = get_by_user_id(db_session=db_session, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A user with this id does not exist."}],
        )

    return update_password(db_session=db_session, user=user, user_in=user_in)


@auth_router.post("/login", response_model=UserLoginResponse)
def login_user(
    user_in: UserLogin,
    db_session: Session = Depends(get_db)
):
    user = get_by_user_id(db_session=db_session, user_id=user_in.user_id)
    if user and user.check_password(user_in.password):
        return {"access_token": user.token}
    raise ValidationError(
        [
            ErrorWrapper(
                InvalidUsernameError(msg="Invalid username."),
                loc="username",
            ),
            ErrorWrapper(
                InvalidPasswordError(msg="Invalid password."),
                loc="password",
            ),
        ],
        model=UserLogin,
    )


@auth_router.post("/register", response_model=UserRegisterResponse)
async def register_user(
    user_in: UserRegister = Depends(UserRegister),
    profile_image: UploadFile = File(None),
    db_session: Session = Depends(get_db),
):
    user = get_by_user_id(db_session=db_session, user_id=user_in.user_id)
    if user:
        raise ValidationError(
            [
                ErrorWrapper(
                    InvalidConfigurationError(msg="A user with this email already exists."),
                    loc="email",
                )
            ],
            model=UserRegister,
        )
    user = await create(db_session=db_session, user_in=user_in, profile_image=profile_image)
    return user
