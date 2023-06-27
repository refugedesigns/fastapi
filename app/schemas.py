from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class UserBase(BaseModel):
    email: EmailStr
    password: str


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


class PostResponse(BaseModel):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
