from typing import Optional
from pydantic import BaseModel, conint
from datetime import datetime

from pydantic.networks import EmailStr


class PostIn(BaseModel):
    ''' set the schema to validate post requests, 
        to ensure that frontend sends the exact data that backend expects 
    '''
    title: str
    content: str
    published: bool = True
    rating: int


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int
    created_at: datetime
    owner: UserOut # pydentic model Type

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: Post
    votes: int


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)