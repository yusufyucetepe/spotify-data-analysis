import pandas as pd
from datetime import datetime, timedelta
import time

class SpotifyDataCollector:
    def __init__(self, spotify_client):
        self.sp = spotify_client
    
    def get_top_artists(self, time_range='medium_term', limit=20):
        """
        Get user's top artists
        
        Args:
            time_range: 'short_term' (~4 weeks), 'medium_term' (~6 months), 'long_term' (years)
            limit: Number of artists to return (max 50)
        
        Returns:
            list of dicts with artist info
        """
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