from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from cotacol import crud, models, schemas
from cotacol.db import get_db
from cotacol.security import get_user_from_token


router = APIRouter()


@router.get("/me/", response_model=schemas.User, summary="Retrieve user information")
async def get_current_user(current_user: models.User = Depends(get_user_from_token)):
    """
    Retrieves the details of the current user (authenticated).
    """
    return current_user


@router.patch("/me/", response_model=schemas.User, summary="Update user information")
async def update_user(
    user: schemas.UserUpdate, current_user: models.User = Depends(get_user_from_token), db: Session = Depends(get_db),
):
    """
    Updates some user information, like bookmarks or climbed climbs (authenticated).
    """
    updated_user = crud.update_user(db, current_user.id, user)
    return updated_user
