from fastapi import APIRouter

router = APIRouter()


@router.get("/top")
async def get_top_tracks(time_range: str = "medium_term", limit: int = 50):
    # Will fetch user's top tracks from Spotify and persist to DB
    return {"message": "top tracks — not yet implemented"}


@router.get("/recently-played")
async def get_recently_played(limit: int = 50):
    # Will fetch recently played tracks from Spotify and persist to DB
    return {"message": "recently played — not yet implemented"}
