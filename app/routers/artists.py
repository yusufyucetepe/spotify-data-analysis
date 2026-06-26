from fastapi import APIRouter

router = APIRouter()


@router.get("/top")
async def get_top_artists(time_range: str = "medium_term", limit: int = 20):
    # Will fetch user's top artists from Spotify and persist to DB
    return {"message": "top artists — not yet implemented"}


@router.get("/genres")
async def get_genre_distribution(time_range: str = "medium_term"):
    # Will return genre distribution from user's top artists
    return {"message": "genre distribution — not yet implemented"}
