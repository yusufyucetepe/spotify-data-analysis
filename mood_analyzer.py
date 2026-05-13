import pandas as pd
import numpy as np


class MoodAnalyzer:
    MOOD_COLORS = {
        'sad': '#4A90E2',
        'happy': '#FFD700',
        'energetic': '#FF6B6B',
        'calm': '#51CF66',
        'melancholic': '#9B59B6',
        'neutral': '#95A5A6'
    }
    
    def __init__(self):
        pass
    
    def classify_mood(self, valence, energy, danceability, acousticness):
        # Happy - high positivity and energy
        if valence > 0.6 and energy > 0.6:
            return 'happy'
        
        # Sad - low positivity and low energy
        elif valence < 0.4 and energy < 0.4:
            return 'sad'
        
        # Energetic - high energy and danceability
        elif energy > 0.7 and danceability > 0.6:
            return 'energetic'
        
        # Calm - low energy, high acousticness
        elif energy < 0.5 and acousticness > 0.5:
            return 'calm'
        
        # Melancholic - low valence but moderate energy
        elif valence < 0.4 and 0.4 <= energy <= 0.7:
            return 'melancholic'
        
        # Neutral - everything else
        else:
            return 'neutral'
    
    def analyze_dataset(self, df):
        if not all(col in df.columns for col in ['valence', 'energy', 'danceability', 'acousticness']):
            raise ValueError("DataFrame must contain: valence, energy, danceability, acousticness")
        
        # Classify mood for each track
        df['mood'] = df.apply(
            lambda row: self.classify_mood(
                row['valence'], 
                row['energy'], 
                row['danceability'], 
                row['acousticness']
            ),
            axis=1
        )
        
        df['mood_color'] = df['mood'].map(self.MOOD_COLORS)
        
        return df
    
    def get_mood_summary(self, df):
        mood_counts = df['mood'].value_counts()
        total = len(df)
        
        summary = {}
        for mood, count in mood_counts.items():
            summary[mood] = {
                'count': count,
                'percentage': round((count / total) * 100, 1),
                'color': self.MOOD_COLORS[mood]
            }
        
        return summary
    
    def get_daily_mood(self, df):
        # Extract date from timestamp
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        
        # Group by date and get most common mood
        daily_mood = df.groupby('date').agg({
            'mood': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'neutral',
            'valence': 'mean',
            'energy': 'mean'
        }).reset_index()
        
        # Add color
        daily_mood['mood_color'] = daily_mood['mood'].map(self.MOOD_COLORS)
        
        return daily_mood
    
    def get_mood_emoji(self, mood):
        emoji_map = {
            'sad': '😢',
            'happy': '😊',
            'energetic': '🔥',
            'calm': '😌',
            'melancholic': '😔',
            'neutral': '😐'
        }
        return emoji_map.get(mood, '❓')
    
    def print_mood_report(self, df):
        summary = self.get_mood_summary(df)
        
        print("\n" + "="*50)
        print("🎭 MOOD ANALYSIS REPORT")
        print("="*50)
        
        total_tracks = len(df)
        print(f"\n Total Tracks Analyzed: {total_tracks}")
        
        print("\n Mood Distribution:")
        for mood, data in sorted(summary.items(), key=lambda x: x[1]['count'], reverse=True):
            emoji = self.get_mood_emoji(mood)
            bar = "█" * int(data['percentage'] / 2)
            print(f"  {emoji} {mood.capitalize():12} | {bar} {data['percentage']}% ({data['count']} tracks)")
        
        # Calculate overall metrics
        avg_valence = df['valence'].mean()
        avg_energy = df['energy'].mean()
        
        print(f"\n Average Audio Features:")
        print(f"  Valence (Positivity): {avg_valence:.2f}/1.0")
        print(f"  Energy (Intensity):   {avg_energy:.2f}/1.0")
        
        # Overall mood interpretation
        if avg_valence > 0.6:
            overall = "Your listening has been quite positive! 😊"
        elif avg_valence < 0.4:
            overall = "Your listening has been more melancholic 😔"
        else:
            overall = "Your listening shows a balanced mood 😌"
        
        print(f"\n Overall: {overall}")
        print("="*50 + "\n")


if __name__ == "__main__":
    # Test mood classification
    analyzer = MoodAnalyzer()
    
    print("Testing mood classifications:\n")
    
    test_cases = [
        (0.9, 0.8, 0.7, 0.3, "happy"),
        (0.2, 0.2, 0.3, 0.4, "sad"),
        (0.5, 0.9, 0.8, 0.2, "energetic"),
        (0.5, 0.3, 0.4, 0.8, "calm"),
    ]
    
    for valence, energy, dance, acoustic, expected in test_cases:
        mood = analyzer.classify_mood(valence, energy, dance, acoustic)
        emoji = analyzer.get_mood_emoji(mood)
        print(f"{emoji} Valence={valence}, Energy={energy} → {mood}")