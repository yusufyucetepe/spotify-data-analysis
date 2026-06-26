from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
async def get_mood_summary():
    # Will run MoodAnalyzer on the user's recent listening history
    return {"message": "mood summary — not yet implemented"}


@router.get("/daily")
async def get_daily_mood():
    # Will return per-day mood breakdown
    return {"message": "daily mood — not yet implemented"}
