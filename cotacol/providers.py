import httpx

from cotacol import settings


class OAuthProvider:
    code: str = ""
    base_url: str = ""
    access_token: str = ""

    def validate(self, refresh_token: str) -> dict:
        raise NotImplementedError


class Strava(OAuthProvider):
    code = "strava"
    base_url = settings.STRAVA_API_BASE_URL

    def validate(self, refresh_token: str) -> dict:
        res = httpx.post(
            f"{self.base_url}/oauth/token",
            data={
                "client_id": settings.STRAVA_CLIENT_ID,
                "client_secret": settings.STRAVA_CLIENT_SECRET,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
        ).json()

        self.access_token = res["access_token"]
        res["athlete"] = self.get("/athlete")
        return res

    def get(self, path: str):
        return httpx.get(f"{self.base_url}{path}", headers={"Authorization": f"Bearer {self.access_token}"}).json()


def get_provider(provider: str) -> OAuthProvider:
    return {Strava.code: Strava()}[provider]
