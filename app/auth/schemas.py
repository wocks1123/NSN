import bcrypt
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator
from app.models import NSNBase, form_body


def hash_password(password: str) -> str:
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt).decode()


class UserBase(NSNBase):
    user_id: str


class UserRead(UserBase):
    user_name: str
    email: EmailStr
    profile_message: Optional[str]
    profile_image_path: str
    post_count: int
    following_count: int
    follower_count: int


class UserReadInPost(UserBase):
    user_name: str
    email: EmailStr
    profile_message: Optional[str]
    profile_image_path: str


class UserUpdate(NSNBase):
    user_name: Optional[str] = Field(None, nullable=True)
    email: Optional[str] = Field(None, nullable=True)
    password: Optional[str] = Field(None, nullable=True)
    profile_message: Optional[str] = Field(None, nullable=True)


class PasswordUpdate(NSNBase):
    password: str
    new_password: str
    new_password_again: str


class UserLogin(UserBase):
    password: str

    @validator("password")
    def password_required(cls, v):
        if not v:
            raise ValueError("Must not be empty string")
        return v


@form_body
class UserRegister(BaseModel):
    user_id: str
    user_name: str
    email: str
    password: str

    @validator("password", pre=True, always=True)
    def password_required(cls, v):
        return hash_password(v)


class JWTUser(NSNBase):
    user_id: str


class UserLoginResponse(NSNBase):
    access_token: Optional[str] = Field(None, nullable=True)
    token_type: str = "bearer"


class UserRegisterResponse(NSNBase):
    token: Optional[str] = Field(None, nullable=True)


class UserProfileResponse(UserBase):
    user_name: str
    email: EmailStr
    profile_message: Optional[str]
    profile_image_path: str
    post_count: int
    following_count: int
    follower_count: int
    followed: bool


class UserCardResponse(NSNBase):
    user_id: str
    user_name: str
    email: str
    profile_image_path: str
