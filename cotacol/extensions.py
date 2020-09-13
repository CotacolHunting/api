from authlib.integrations.starlette_client import OAuth

from cotacol.settings import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET


oauth = OAuth()
oauth.register(
    name='strava',
    client_id=STRAVA_CLIENT_ID,
    client_secret=STRAVA_CLIENT_SECRET,
    api_base_url="https://www.strava.com/api/v3/",
    access_token_url="https://www.strava.com/oauth/token",
    authorize_url="https://www.strava.com/oauth/authorize",
    client_kwargs={
        "response_type": "code",
        "scope": "read",
        "token_endpoint_auth_method": "client_secret_post",
    }
)
