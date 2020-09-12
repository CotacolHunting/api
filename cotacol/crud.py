from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from sqlalchemy.sql import func  # type: ignore
from typing import Optional

from . import models, schemas


def _patch(obj, d):
    for key, value in d.items():
        if hasattr(obj, key):
            setattr(obj, key, list(value) if type(value) is set else value)


def create_user_for_provider(db: Session, res: dict, provider: str = "strava") -> Optional[models.User]:
    if provider == "strava":
        uid, username = str(res["athlete"]["id"]), str(res["athlete"]["username"])
    else:
        return None

    try:
        account = get_social_account(db, provider, uid)
        account.last_login = func.now()
        account.user.username = username
        account.extra_data = res
    except NoResultFound:
        account = None
        db.add(
            models.SocialAccount(
                user=models.User(username=username), provider=provider, uid=uid, extra_data=res, last_login=func.now(),
            )
        )

    db.flush()
    db.commit()

    if not account:
        account = get_social_account(db, provider, uid)

    return account.user


def update_user(db: Session, user_id: int, data: schemas.UserUpdate):
    user = get_user(db, user_id)
    _patch(user, data.dict(exclude_unset=True))
    db.flush()
    db.commit()
    return user


def get_social_account(db: Session, provider: str, uid: str):
    return (
        db.query(models.SocialAccount)
        .filter(models.SocialAccount.provider == provider, models.SocialAccount.uid == uid)
        .one()
    )


def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)


def get_climb(db: Session, climb_id: int):
    return db.query(models.Climb).get(climb_id)


def get_climbs(db: Session):
    return db.query(models.Climb).all()
