from pydantic import BaseModel, EmailStr, validator

from enum import Enum
from datetime import datetime


class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserBase(BaseModel):
    email: EmailStr
    password: str
    role: RoleEnum


class CreatePost(PostBase):
    pass


class CreateUser(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class Payload(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: int
    email: EmailStr
    role: RoleEnum


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    user: UserResponse
    created_at: datetime

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: int

    @validator("dir")
    def check_dir(cls, value):
        print(type(value))
        if value not in [0, 1]:
            raise ValueError("Invalid value for post direction!")
        return value
