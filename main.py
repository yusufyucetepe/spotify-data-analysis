import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="user-read-recently-played",open_browser=False))

results = sp.current_user_recently_played(limit=5)

for item in results['items']:
    print(item['track']['name'])