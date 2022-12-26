from typing import List
from pydantic import BaseModel
from uuid import UUID


class UserBase(BaseModel):
    userId: str
    userName: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    # created_at: datetime
    # updated_at: datetime

    class Config:
        orm_mode = True
