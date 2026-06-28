import pandas as pd
from datetime import datetime
import time


class SpotifyDataCollector:
    def __init__(self, spotify_client):
        self.sp = spotify_client

    def get_top_artists(self, time_range='medium_term', limit=20):
        results = self.sp.current_user_top_artists(time_range=time_range, limit=limit)

        artists = []
        for item in results.get('items', []):
            artists.append({
                'name': item.get('name'),
                'genres': item.get('genres') or [],
                'popularity': item.get('popularity'),
                'followers': (item.get('followers') or {}).get('total'),
            })

        return artists

    def get_top_tracks(self, time_range='medium_term', limit=50):
        results = self.sp.current_user_top_tracks(time_range=time_range, limit=limit)

        tracks = []
        for item in results['items']:
            artists = item.get('artists') or []
            tracks.append({
                'id': item.get('id'),
                'name': item.get('name'),
                'artist': artists[0]['name'] if artists else None,
                'album': (item.get('album') or {}).get('name'),
                'popularity': item.get('popularity'),
            })

        return tracks

    def get_recently_played(self, limit=50):
        results = self.sp.current_user_recently_played(limit=limit)

        all_tracks = []
        for item in results['items']:
            track = item.get('track') or {}
            artists = track.get('artists') or []
            played_at = item.get('played_at', '')
            all_tracks.append({
                'track_id': track.get('id'),
                'track_name': track.get('name'),
                'artist': artists[0]['name'] if artists else None,
                'played_at': played_at,
                'timestamp': datetime.fromisoformat(played_at.replace('Z', '+00:00')) if played_at else None,
            })

        return pd.DataFrame(all_tracks)

    def get_audio_features(self, track_ids):
        features_list = []

        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i + 100]
            features = self.sp.audio_features(batch)
            features_list.extend([f for f in features if f is not None])
            time.sleep(0.1)

        return pd.DataFrame(features_list)

    def collect_full_dataset(self, history_limit=50):
        print("Collecting listening history...")
        recent = self.get_recently_played(limit=history_limit)
        print(f"Found {len(recent)} recently played tracks")

        print("Fetching audio features...")
        track_ids = recent['track_id'].tolist()
        features = self.get_audio_features(track_ids)

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

        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_genres[:15])
