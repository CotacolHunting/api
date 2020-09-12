from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.sessions import SessionMiddleware

from . import settings
from .db import Base, engine
from .routers import auth, climbs, users


Base.metadata.create_all(bind=engine)

app = FastAPI(title="COTACOL", version="0.1.0", docs_url=None, redoc_url="/docs/", debug=settings.DEBUG)

# register middlewares

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)
app.add_middleware(GZipMiddleware)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

if not settings.DEBUG:
    app.add_middleware(HTTPSRedirectMiddleware)

# register routers

app.include_router(auth.router, prefix="/auth", tags=["Authorization"])
app.include_router(climbs.router, prefix="/v1/climbs", tags=["Climbs"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
