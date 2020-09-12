from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Set

from .climbs import CotacolId


class UserBase(BaseModel):
    bookmarks: Set[CotacolId] = {}
    climbed: Set[CotacolId] = {}


class UserUpdate(UserBase):
    pass


class User(UserBase):
    username: str
    full_name: str
    profile_picture: str
    date_joined: Optional[datetime]
    is_staff: bool

    class Config:
        orm_mode = True
