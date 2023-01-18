from typing import List
from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    userId: str
    userName: str
    email: str


class UserCreate(UserBase):
    profileMessage: str
    profileImagePath: str
    password: str


class UserUpdate(UserBase):
    profileMessage: str
    profileImagePath: str
    password: str


class UserResponse(UserBase):
    profileMessage: str
    profileImagePath: str

    class Config:
        orm_mode = True


class UserInPost(BaseModel):
    userName: str
    email: str
    profileImagePath: str

    class Config:
        orm_mode = True
