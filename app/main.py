from fastapi import FastAPI
from app.routers import auth, tracks, artists, moods

app = FastAPI(title="Spotify Analyzer API", version="0.1.0")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tracks.router, prefix="/tracks", tags=["tracks"])
app.include_router(artists.router, prefix="/artists", tags=["artists"])
app.include_router(moods.router, prefix="/moods", tags=["moods"])


@app.get("/health")
async def health():
    return {"status": "ok"}
