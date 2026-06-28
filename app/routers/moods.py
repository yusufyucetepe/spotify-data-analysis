import spotipy
from fastapi import APIRouter, Depends

from app.dependencies import get_spotify_client
from app.services.data_collector import SpotifyDataCollector
from app.services.mood_analyzer import MoodAnalyzer

router = APIRouter()


def _build_mood_dataset(sp: spotipy.Spotify):
    collector = SpotifyDataCollector(sp)
    analyzer = MoodAnalyzer()
    dataset = collector.collect_full_dataset()
    return analyzer.analyze_dataset(dataset), analyzer


@router.get("/summary")
async def get_mood_summary(sp: spotipy.Spotify = Depends(get_spotify_client)):
    dataset, analyzer = _build_mood_dataset(sp)
    return analyzer.get_mood_summary(dataset)


@router.get("/daily")
async def get_daily_mood(sp: spotipy.Spotify = Depends(get_spotify_client)):
    dataset, analyzer = _build_mood_dataset(sp)
    daily = analyzer.get_daily_mood(dataset)
    daily["date"] = daily["date"].astype(str)
    return daily.to_dict("records")
