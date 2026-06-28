import spotipy
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.dependencies import get_spotify_client
from app.services.data_collector import SpotifyDataCollector
from app.services.mood_analyzer import MoodAnalyzer

router = APIRouter()

SPOTIFY_RESTRICTED_MSG = {"detail": "Spotify did not return audio feature data. This endpoint requires the audio_features API which is restricted for apps created after November 2024."}


def _build_mood_dataset(sp: spotipy.Spotify):
    collector = SpotifyDataCollector(sp)
    analyzer = MoodAnalyzer()
    try:
        dataset = collector.collect_full_dataset()
    except Exception:
        return None, None
    return analyzer.analyze_dataset(dataset), analyzer


@router.get("/summary")
async def get_mood_summary(sp: spotipy.Spotify = Depends(get_spotify_client)):
    dataset, analyzer = _build_mood_dataset(sp)
    if dataset is None:
        return JSONResponse(status_code=503, content=SPOTIFY_RESTRICTED_MSG)
    return analyzer.get_mood_summary(dataset)


@router.get("/daily")
async def get_daily_mood(sp: spotipy.Spotify = Depends(get_spotify_client)):
    dataset, analyzer = _build_mood_dataset(sp)
    if dataset is None:
        return JSONResponse(status_code=503, content=SPOTIFY_RESTRICTED_MSG)
    daily = analyzer.get_daily_mood(dataset)
    daily["date"] = daily["date"].astype(str)
    return daily.to_dict("records")
