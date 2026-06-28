from pydantic import BaseModel


class Track(BaseModel):
    id: str | None = None
    name: str | None = None
    artist: str | None = None
    album: str | None = None
    popularity: int | None = None


class RecentTrack(BaseModel):
    track_id: str | None = None
    track_name: str | None = None
    artist: str | None = None
    played_at: str
    timestamp: str


class Artist(BaseModel):
    name: str | None = None
    genres: list[str] = []
    popularity: int | None = None
    followers: int | None = None


class MoodEntry(BaseModel):
    count: int
    percentage: float
    color: str


class DailyMood(BaseModel):
    date: str
    mood: str
    valence: float
    energy: float
    mood_color: str | None = None
