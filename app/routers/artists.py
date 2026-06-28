import spotipy
from fastapi import APIRouter, Depends

from app.dependencies import get_spotify_client
from app.schemas import Artist
from app.services.data_collector import SpotifyDataCollector

router = APIRouter()


@router.get("/top", response_model=list[Artist])
async def get_top_artists(
    time_range: str = "medium_term",
    limit: int = 20,
    sp: spotipy.Spotify = Depends(get_spotify_client),
):
    collector = SpotifyDataCollector(sp)
    return collector.get_top_artists(time_range=time_range, limit=limit)
