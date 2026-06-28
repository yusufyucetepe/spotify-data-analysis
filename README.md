# Spotify Analyzer API

A REST API that connects to your Spotify account and exposes your listening data — top tracks, top artists, and mood analysis based on audio features.

Built with FastAPI, PostgreSQL, and the Spotify Web API.

---

## Stack

- **FastAPI** — API framework
- **PostgreSQL** — user and token storage
- **Spotipy** — Spotify Web API client
- **SQLAlchemy** (async) — ORM
- **JWT** — session tokens

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/auth/login` | Redirects to Spotify OAuth |
| `GET` | `/auth/callback` | Handles OAuth callback, returns JWT |
| `GET` | `/auth/me` | Returns the current user's profile |
| `GET` | `/tracks/top` | Your top tracks (`time_range`, `limit`) |
| `GET` | `/tracks/recently-played` | Your recently played tracks (`limit`) |
| `GET` | `/artists/top` | Your top artists (`time_range`, `limit`) |
| `GET` | `/moods/summary` | Mood distribution of your recent listening |
| `GET` | `/moods/daily` | Per-day mood breakdown |

All endpoints except `/auth/*` require a `Bearer` token in the `Authorization` header.

> **Note:** `/moods/*` endpoints require the Spotify `audio_features` API, which is restricted for apps created after November 2024. These endpoints will return a `503` if your app does not have access.

---

## Getting Started

### 1. Clone and install dependencies

```bash
git clone <repo-url>
cd spotify-data-analysis
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Create a Spotify app

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Add `http://127.0.0.1:8000/auth/callback` as a Redirect URI

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8000/auth/callback
SECRET_KEY=your_secret_key
DATABASE_URL=postgresql+asyncpg://user:password@localhost/spotify_analyzer
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

The interactive API docs are available at `http://127.0.0.1:8000/docs`.

---

## Authentication Flow

1. Visit `/auth/login` — you will be redirected to Spotify
2. Authorize the app
3. You will be redirected back to `/auth/callback` with a JWT
4. Use the JWT as a `Bearer` token on all subsequent requests
