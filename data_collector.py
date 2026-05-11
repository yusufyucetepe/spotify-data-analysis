import pandas as pd
from datetime import datetime, timedelta
import time

class SpotifyDataCollector:
    def __init__(self, spotify_client):
        self.sp = spotify_client
    
    def get_top_artists(self, time_range='medium_term', limit=20):
        results = self.sp.current_user_top_artists(time_range=time_range, limit=limit)
        
        artists = []
        for item in results['items']:
            artists.append({
                'name': item['name'],
                'genres': item['genres'],
                'popularity': item['popularity'],
                'followers': item['followers']['total']
            })
        
        return artists
    
def get_top_tracks(self, time_range='medium_term', limit=50):
        """
        Get user's top tracks
        
        Returns:
            list of dicts with track info
        """
        results = self.sp.current_user_top_tracks(time_range=time_range, limit=limit)
        
        tracks = []
        for item in results['items']:
            tracks.append({
                'id': item['id'],
                'name': item['name'],
                'artist': item['artists'][0]['name'],
                'album': item['album']['name'],
                'popularity': item['popularity']
            })
        
        return tracks

def get_recently_played(self, limit=50):
        all_tracks = []
        
        # Spotify API limits to 50 tracks per request
        # To get more history, we need to paginate using 'before' parameter
        results = self.sp.current_user_recently_played(limit=limit)
        
        for item in results['items']:
            track = item['track']
            all_tracks.append({
                'track_id': track['id'],
                'track_name': track['name'],
                'artist': track['artists'][0]['name'],
                'played_at': item['played_at'],
                'timestamp': datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
            })
        
        return pd.DataFrame(all_tracks)
    
def get_audio_features(self, track_ids):
        # API accepts max 100 tracks per request
        features_list = []
        
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            features = self.sp.audio_features(batch)
            features_list.extend([f for f in features if f is not None])
            time.sleep(0.1)  # Rate limiting
        
        return pd.DataFrame(features_list)
    
def collect_full_dataset(self, history_limit=50):
        print("Collecting listening history...")
        recent = self.get_recently_played(limit=history_limit)
        
        print(f"✅ Found {len(recent)} recently played tracks")
        
        print("🎵 Fetching audio features...")
        track_ids = recent['track_id'].tolist()
        features = self.get_audio_features(track_ids)
        
        # Merge tracks with audio features
        dataset = recent.merge(
            features, 
            left_on='track_id', 
            right_on='id',
            how='left'
        )
        
        print(f"Complete dataset ready: {len(dataset)} tracks with audio features")
        
        return dataset
    
def get_genre_distribution(self, time_range='medium_term'):
        artists = self.get_top_artists(time_range=time_range, limit=50)
        
        genre_counts = {}
        for artist in artists:
            for genre in artist['genres']:
                genre_counts[genre] = genre_counts.get(genre, 0) + 1
        
        # Sort by count
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_genres[:15])  # Top 15 genres
 
 
if __name__ == "__main__":
    from spotify_auth import get_spotify_client
    
    sp = get_spotify_client()
    collector = SpotifyDataCollector(sp)
    
    # Test data collection
    print("\nTop 5 Artists:")
    artists = collector.get_top_artists(limit=5)
    for i, artist in enumerate(artists, 1):
        print(f"{i}. {artist['name']} - {', '.join(artist['genres'][:3])}")
    
    print("\nTop 5 Genres:")
    genres = collector.get_genre_distribution()
    for genre, count in list(genres.items())[:5]:
        print(f"  {genre}: {count}")