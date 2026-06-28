import spotipy
from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_spotify_client
from app.schemas import DailyMood, MoodEntry
from app.services.data_collector import SpotifyDataCollector
from app.services.mood_analyzer import MoodAnalyzer

router = APIRouter()

AUDIO_FEATURES_UNAVAILABLE = "Spotify did not return audio feature data. This endpoint requires the audio_features API which is restricted for apps created after November 2024."


def _build_mood_dataset(sp: spotipy.Spotify):
    try:
        collector = SpotifyDataCollector(sp)
        analyzer = MoodAnalyzer()
        dataset = collector.collect_full_dataset()
        return analyzer.analyze_dataset(dataset), analyzer
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=AUDIO_FEATURES_UNAVAILABLE,
        )


@router.get("/summary", response_model=dict[str, MoodEntry])
async def get_mood_summary(sp: spotipy.Spotify = Depends(get_spotify_client)):
    dataset, analyzer = _build_mood_dataset(sp)
    return analyzer.get_mood_summary(dataset)


@router.get("/daily", response_model=list[DailyMood])
async def get_daily_mood(sp: spotipy.Spotify = Depends(get_spotify_client)):
    dataset, analyzer = _build_mood_dataset(sp)
    daily = analyzer.get_daily_mood(dataset)
    daily["date"] = daily["date"].astype(str)
    return daily.to_dict("records")
