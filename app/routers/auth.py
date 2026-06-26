from fastapi import APIRouter

router = APIRouter()


@router.get("/login")
async def login():
    # Will be implemented in Step 3: redirect user to Spotify OAuth
    return {"message": "Spotify OAuth login — not yet implemented"}


@router.get("/callback")
async def callback(code: str):
    # Will be implemented in Step 3: exchange code for token and store in DB
    return {"message": "Spotify OAuth callback — not yet implemented"}
