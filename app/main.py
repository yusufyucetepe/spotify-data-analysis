from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db import engine, Base
from app.routers import auth, tracks, artists, moods
import app.models  # registers all models with Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="Spotify Analyzer API", version="0.1.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(tracks.router, prefix="/tracks", tags=["tracks"])
app.include_router(artists.router, prefix="/artists", tags=["artists"])
app.include_router(moods.router, prefix="/moods", tags=["moods"])


@app.get("/health")
async def health():
    return {"status": "ok"}
