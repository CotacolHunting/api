from pydantic import BaseModel
from typing import List, Literal


Provider = Literal["strava"]

Scope = Literal["me", "read", "write"]


class Token(BaseModel):
    token_type: Literal["Bearer"] = "Bearer"
    access_token: str
    expires_at: int
    scopes: List[Scope] = []


class JST(BaseModel):
    scopes: List[Scope] = []
