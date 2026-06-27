from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta, timezone

from app.db import get_db
from app.models.user import User
from app.auth import (
    get_spotify_auth_url,
    exchange_code_for_tokens,
    get_spotify_profile,
    create_jwt,
)

router = APIRouter()


@router.get("/login")
async def login():
    """Redirect the user to Spotify's authorization page."""
    return RedirectResponse(url=get_spotify_auth_url())


@router.get("/callback")
async def callback(code: str, db: AsyncSession = Depends(get_db)):
    """Spotify redirects here after the user grants access."""
    try:
        tokens = await exchange_code_for_tokens(code)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to exchange authorization code")

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]
    token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=tokens["expires_in"])

    try:
        profile = await get_spotify_profile(access_token)
    except Exception:
        raise HTTPException(status_code=400, detail="Failed to fetch Spotify profile")

    spotify_id = profile["id"]

    result = await db.execute(select(User).where(User.spotify_id == spotify_id))
    user = result.scalar_one_or_none()

    if user:
        user.access_token = access_token
        user.refresh_token = refresh_token
        user.token_expires_at = token_expires_at
        user.display_name = profile.get("display_name")
        user.email = profile.get("email")
    else:
        user = User(
            spotify_id=spotify_id,
            display_name=profile.get("display_name"),
            email=profile.get("email"),
            access_token=access_token,
            refresh_token=refresh_token,
            token_expires_at=token_expires_at,
        )
        db.add(user)

    await db.commit()

    jwt_token = create_jwt(spotify_id)
    return {
        "access_token": jwt_token,
        "token_type": "bearer",
        "user": profile.get("display_name"),
        "spotify_id": spotify_id,
    }


@router.get("/me")
async def me(db: AsyncSession = Depends(get_db)):
    """Health check placeholder — secured routes use get_current_user dependency."""
    return {"message": "Use the Bearer token from /auth/callback on secured endpoints"}
