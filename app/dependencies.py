from datetime import datetime, timedelta, timezone

import spotipy
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import decode_jwt, refresh_spotify_token
from app.db import get_db
from app.models.user import User

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    spotify_id = decode_jwt(credentials.credentials)

    if not spotify_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.spotify_id == spotify_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_spotify_client(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> spotipy.Spotify:
    now = datetime.now(timezone.utc)
    access_token = user.access_token

    if user.token_expires_at <= now:
        token_data = await refresh_spotify_token(user.refresh_token)
        access_token = token_data["access_token"]
        new_expiry = now + timedelta(seconds=token_data["expires_in"])
        await db.execute(
            update(User)
            .where(User.spotify_id == user.spotify_id)
            .values(access_token=access_token, token_expires_at=new_expiry)
        )
        await db.commit()

    return spotipy.Spotify(auth=access_token)
