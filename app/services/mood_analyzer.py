import pandas as pd


class MoodAnalyzer:
    MOOD_COLORS = {
        'sad': '#4A90E2',
        'happy': '#FFD700',
        'energetic': '#FF6B6B',
        'calm': '#51CF66',
        'melancholic': '#9B59B6',
        'neutral': '#95A5A6'
    }

    MOOD_EMOJIS = {
        'sad': '😢',
        'happy': '😊',
        'energetic': '🔥',
        'calm': '😌',
        'melancholic': '😔',
        'neutral': '😐'
    }

    def __init__(self):
        pass

    def classify_mood(self, valence, energy, danceability, acousticness):
        if valence > 0.6 and energy > 0.6:
            return 'happy'
        elif valence < 0.4 and energy < 0.4:
            return 'sad'
        elif energy > 0.7 and danceability > 0.6:
            return 'energetic'
        elif energy < 0.5 and acousticness > 0.5:
            return 'calm'
        elif valence < 0.4 and 0.4 <= energy <= 0.7:
            return 'melancholic'
        else:
            return 'neutral'

    def analyze_dataset(self, df):
        required = ['valence', 'energy', 'danceability', 'acousticness']
        if not all(col in df.columns for col in required):
            raise ValueError(f"DataFrame must contain: {', '.join(required)}")

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

        return {
            mood: {
                'count': int(count),
                'percentage': round((count / total) * 100, 1),
                'color': self.MOOD_COLORS[mood]
            }
            for mood, count in mood_counts.items()
        }

    def get_daily_mood(self, df):
        df['date'] = pd.to_datetime(df['timestamp']).dt.date

        daily_mood = df.groupby('date').agg({
            'mood': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'neutral',
            'valence': 'mean',
            'energy': 'mean'
        }).reset_index()

        daily_mood['mood_color'] = daily_mood['mood'].map(self.MOOD_COLORS)
        return daily_mood

    def get_mood_emoji(self, mood):
        return self.MOOD_EMOJIS.get(mood, '❓')

    def print_mood_report(self, df):
        summary = self.get_mood_summary(df)

        print("\n" + "=" * 50)
        print("MOOD ANALYSIS REPORT")
        print("=" * 50)
        print(f"\nTotal Tracks Analyzed: {len(df)}")
        print("\nMood Distribution:")

        for mood, data in sorted(summary.items(), key=lambda x: x[1]['count'], reverse=True):
            emoji = self.get_mood_emoji(mood)
            bar = "█" * int(data['percentage'] / 2)
            print(f"  {emoji} {mood.capitalize():12} | {bar} {data['percentage']}% ({data['count']} tracks)")

        avg_valence = df['valence'].mean()
        avg_energy = df['energy'].mean()

        print(f"\nAverage Audio Features:")
        print(f"  Valence (Positivity): {avg_valence:.2f}/1.0")
        print(f"  Energy (Intensity):   {avg_energy:.2f}/1.0")

        if avg_valence > 0.6:
            overall = "Your listening has been quite positive!"
        elif avg_valence < 0.4:
            overall = "Your listening has been more melancholic."
        else:
            overall = "Your listening shows a balanced mood."

        print(f"\nOverall: {overall}")
        print("=" * 50 + "\n")
