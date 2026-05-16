# 🎵 Spotify Mood Analysis
 
Analyze your Spotify listening habits and visualize your musical moods over time with a beautiful GitHub-style activity calendar.
 
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Spotify](https://img.shields.io/badge/spotify-API-green.svg)

## ✨ Features
 
- **Top Artists & Genres** - See who you've been listening to most
- **Mood Detection** - Automatically classify tracks as happy, sad, energetic, calm, etc.
- **Visual Calendar** - GitHub-style heatmap showing your daily musical moods
- **Color-Coded** - Blue for sad days, yellow for joyful ones, and more

## 🚀 Quick Start
 
### 1. Install Dependencies
 
```bash
pip install -r requirements.txt
```
 
### 2. Get Spotify API Credentials
 
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **Create an App**
3. Copy your **Client ID** and **Client Secret**
4. Edit Settings → Add `http://localhost:8888/callback` to Redirect URIs

### 3. Configure Your App
 
Create a `.env` file in the project root:
 
```env
SPOTIPY_CLIENT_ID=your_client_id_here
SPOTIPY_CLIENT_SECRET=your_client_secret_here
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```
 
### 4. Run the Analysis
 
```bash
python main.py
```
 
 **First-time authentication:**
1. Enter the URL instructed to your browser
2. Click **Agree** to authorize the app
3. You'll be redirected to `http://localhost:8888/callback?code=...`
4. **The page will show "connection refused" - this is normal!**
5. Copy the entire URL from your browser and paste it in the terminal
6. Future runs will use cached credentials (no need to re-authorize)