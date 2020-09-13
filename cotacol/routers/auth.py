from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session  # type: ignore
from urllib.parse import urlencode

from cotacol import crud, schemas
from cotacol.db import get_db
from cotacol.extensions import oauth
from cotacol.security import generate_access_token


router = APIRouter()


@router.get("/login/{provider}/")
async def login(provider: schemas.Provider, redirect_uri: str, request: Request):
    oauth_client = oauth.create_client(provider)
    redirect_url = f'{request.url_for("authorize", provider=provider)}?{urlencode({"redirect_uri": redirect_uri})}'
    return await oauth_client.authorize_redirect(request, redirect_url)


@router.get("/authorize/{provider}/")
async def authorize(provider: schemas.Provider, redirect_uri: str, request: Request, db: Session = Depends(get_db)):
    oauth_client = oauth.create_client(provider)
    token = await oauth_client.authorize_access_token(request)
    # user = await oauth_client.parse_id_token(request, token)
    user = crud.create_user_for_provider(db, token)
    access_token, expires_at, scopes = generate_access_token(user)
    data = {
        "access_token": access_token,
        "refresh_token": token["refresh_token"],
        "expires_at": expires_at,
        "scopes": scopes
    }

    return RedirectResponse(f"{redirect_uri}?{urlencode(data)}")
