from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Set

from .climbs import CotacolId


class UserBase(BaseModel):
    bookmarks: Set[CotacolId] = set()
    climbed: Set[CotacolId] = set()


class UserUpdate(UserBase):
    pass


class User(UserBase):
    username: str
    full_name: Optional[str]
    profile_picture: Optional[str]
    date_joined: Optional[datetime]
    is_staff: bool

    class Config:
        orm_mode = True
