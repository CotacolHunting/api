from datetime import datetime, timedelta
from jose import JWTError, jwt  # type: ignore
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes
from pydantic import ValidationError
from sqlalchemy.orm import Session  # type: ignore
from typing import List, Optional, Tuple

from cotacol import crud, schemas, settings
from cotacol.db import get_db
from cotacol.models import User


oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="[client]",
    tokenUrl="/auth/token/",
    scopes={"read": "Read COTACOL information.", "write": "Read or write COTACOL information.",},
)


def fake_decode_token(token):
    return User(username=token + "fakedecoded", full_name="John Doe")


def get_user_from_token(
    security_scopes: SecurityScopes, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    def raise_credentials_exception(msg: str = "Could not validate credentials"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=msg, headers={"WWW-Authenticate": authenticate_value},
        )

    try:
        payload = jwt.decode(token, str(settings.SECRET_KEY), algorithms=["HS256"])
        user_id = int(payload.get("sub").split(":")[-1])
        user = crud.get_user(db, user_id)
        token_scopes = payload.get("scopes", [])
        token_data = schemas.JST(scopes=token_scopes)
    except (JWTError, ValidationError):
        raise_credentials_exception()

    if user is None:
        raise_credentials_exception()

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise_credentials_exception("Not enough permissions")

    return user


def generate_access_token(user: User, expires_delta: Optional[timedelta] = None) -> Tuple[str, int, List[str]]:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    expires_at = int(expire.timestamp())
    scopes = ["write"] if user.is_staff else ["read"]
    to_encode = {
        "iss": "COTACOL",
        "sub": f"user:{user.id}",
        "exp": expires_at,
        "scopes": scopes,
    }

    return jwt.encode(to_encode, str(settings.SECRET_KEY), algorithm="HS256"), expires_at, scopes
