import spotipy
from fastapi import APIRouter, Depends

from app.dependencies import get_spotify_client
from app.services.data_collector import SpotifyDataCollector

router = APIRouter()


@router.get("/top")
async def get_top_artists(
    time_range: str = "medium_term",
    limit: int = 20,
    sp: spotipy.Spotify = Depends(get_spotify_client),
):
    collector = SpotifyDataCollector(sp)
    return collector.get_top_artists(time_range=time_range, limit=limit)


@router.get("/genres")
async def get_genre_distribution(
    time_range: str = "medium_term",
    sp: spotipy.Spotify = Depends(get_spotify_client),
):
    collector = SpotifyDataCollector(sp)
    return collector.get_genre_distribution(time_range=time_range)
