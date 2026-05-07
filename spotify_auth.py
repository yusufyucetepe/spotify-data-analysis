import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client():
    scope = "user-top-read user-read-recently-played user-library-read"
    
    if not all([
        os.getenv('SPOTIPY_CLIENT_ID'),
        os.getenv('SPOTIPY_CLIENT_SECRET'),
        os.getenv('SPOTIPY_REDIRECT_URI')
    ]):
        raise ValueError(
            "Missing Spotify credentials! Please set:\n"
            "- SPOTIPY_CLIENT_ID\n"
            "- SPOTIPY_CLIENT_SECRET\n"
            "- SPOTIPY_REDIRECT_URI\n"
            "in your .env file"
        )
    

    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope=scope,
        cache_path=".spotify_cache"
    )
    
    # Return authenticated client
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # Test authentication
    try:
        user = sp.current_user()
        print(f"✓ Authenticated as: {user['display_name']}")
        return sp
    except Exception as e:
        raise Exception(f"Authentication failed: {str(e)}")

if __name__ == "__main__":
    client = get_spotify_client()
    print("Authentication successful!")