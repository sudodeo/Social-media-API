from datetime import datetime
from pydantic import BaseModel, EmailStr, conint
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class CreateUser(UserBase):
    password: str


class ResponseUser(UserBase):
    created_at: datetime
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: Optional[str] = True  # type: ignore


class CreatePost(PostBase):
    pass


class ResponsePost(PostBase):
    created_at: datetime
    owner: ResponseUser
    id: int
    # the response is sent as a dictionary uin the class below
    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
