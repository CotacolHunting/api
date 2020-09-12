from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session  # type: ignore

from cotacol import crud, schemas
from cotacol.db import get_db
from cotacol.providers import get_provider
from cotacol.security import generate_access_token


router = APIRouter()


@router.get("/token/", response_model=schemas.Token, summary="Generate a JWT token")
def validate(provider: schemas.Provider, token: str, request: Request, db: Session = Depends(get_db)):
    """
    Exchange a (provider) token for a COTACOL specific JWT access_token.
    """
    token_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate token",)

    try:
        res = get_provider(provider).validate(token)
    except Exception:
        raise token_exception

    user = crud.create_user_for_provider(db, res, provider)

    if not user:
        raise token_exception

    access_token, expires_at, scopes = generate_access_token(user)

    return {"token_type": "Bearer", "access_token": access_token, "expires_at": expires_at, "scopes": scopes}
