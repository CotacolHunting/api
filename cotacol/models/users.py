from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, JSON  # type: ignore
from sqlalchemy.orm import relationship  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from typing import Optional

from cotacol.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(128))
    bookmarks = Column(JSON, default=[])
    climbed = Column(JSON, default=[])
    date_joined = Column(DateTime(timezone=True), default=func.now())
    is_staff = Column(Boolean(), default=False)
    is_active = Column(Boolean(), default=True)

    social_accounts = relationship("SocialAccount", back_populates="user", lazy="joined")

    @property
    def full_name(self) -> Optional[str]:
        if not self.social_accounts:
            return None
        athlete = self.social_accounts[0].extra_data["athlete"]
        return f'{athlete["firstname"]} {athlete["lastname"]}'

    @property
    def profile_picture(self) -> Optional[str]:
        if not self.social_accounts:
            return None
        return self.social_accounts[0].extra_data["athlete"]["profile"]


class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    provider = Column(String(32))
    uid = Column(String(191))
    extra_data = Column(JSON)
    last_login = Column(DateTime(timezone=True), default=func.now())

    user = relationship("User", back_populates="social_accounts")
