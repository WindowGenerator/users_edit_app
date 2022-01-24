from typing import Optional, List
from enum import Enum

from pydantic import BaseModel


class Permissions(str, Enum):
    view: str = 'right:view'
    full: str = 'right:full'


class User(BaseModel):
    username: str
    email: str
    bio: str = ""


class UserInLogin(BaseModel):
    username: str
    password: str


class UserInCreate(User):
    password: str
    permission: Permissions


class UserInUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    permission: Permissions = None
    bio: Optional[str] = None


class UserWithToken(BaseModel):
    user: User
    access_token: str


class UserInDB(User):
    hashed_password: str
