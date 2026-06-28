import os
import httpx
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv(override=True)

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 7

SPOTIFY_SCOPE = "user-top-read user-read-recently-played user-library-read user-read-email"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


def get_spotify_auth_url(state: str) -> str:
    params = "&".join([
        f"client_id={CLIENT_ID}",
        "response_type=code",
        f"redirect_uri={REDIRECT_URI}",
        f"scope={SPOTIFY_SCOPE.replace(' ', '%20')}",
        f"state={state}",
    ])
    return f"{SPOTIFY_AUTH_URL}?{params}"


async def exchange_code_for_tokens(code: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        response.raise_for_status()
        return response.json()


async def refresh_spotify_token(refresh_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SPOTIFY_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            auth=(CLIENT_ID, CLIENT_SECRET),
        )
        response.raise_for_status()
        return response.json()


async def get_spotify_profile(access_token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.spotify.com/v1/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()


def create_jwt(spotify_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": spotify_id, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
