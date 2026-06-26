import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_SCOPE = "user-top-read user-read-recently-played user-library-read"


def get_spotify_client():
    if not all([
        os.getenv('SPOTIPY_CLIENT_ID'),
        os.getenv('SPOTIPY_CLIENT_SECRET'),
        os.getenv('SPOTIPY_REDIRECT_URI')
    ]):
        raise ValueError(
            "Missing Spotify credentials. Set SPOTIPY_CLIENT_ID, "
            "SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI in your .env file."
        )

    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope=SPOTIFY_SCOPE,
        cache_path=".spotify_cache"
    )

    sp = spotipy.Spotify(auth_manager=auth_manager)

    try:
        user = sp.current_user()
        print(f"Authenticated as: {user['display_name']}")
        return sp
    except Exception as e:
        raise Exception(f"Authentication failed: {e}")
