# analyzer.py
import os
from dotenv import load_dotenv        # ✅ import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.cluster import KMeans

# Load environment variables from .env
load_dotenv()   # ✅ now this works

# ---------------------------
# Spotify Authentication using environment variables
# ---------------------------
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    raise ValueError("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET as environment variables.")

auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ---------------------------
# Fetch Playlist Tracks (All Tracks)
# ---------------------------
playlist_input = input("Enter Spotify Playlist ID or URL: ").strip()

# Extract ID if a URL is provided
if "playlist" in playlist_input:
    try:
        playlist_id = playlist_input.split("playlist/")[1].split("?")[0]
    except IndexError:
        raise ValueError("Invalid Spotify playlist URL")
else:
    playlist_id = playlist_input

print("Fetching playlist tracks...")
tracks = []
offset = 0
while True:
    response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
    items = response['items']
    if not items:
        break
    tracks.extend(items)
    offset += len(items)

print(f"Total tracks fetched: {len(tracks)}")

track_ids = [track['track']['id'] for track in tracks if track['track'] is not None]
track_names = [track['track']['name'] for track in tracks if track['track'] is not None]

# ---------------------------
# Fetch Audio Features
# ---------------------------
audio_features = sp.audio_features(track_ids)
data = pd.DataFrame(audio_features)
data['name'] = track_names

# Keep all common Spotify audio features
columns_to_keep = [
    'name', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
    'duration_ms', 'time_signature'
]
data = data[[col for col in columns_to_keep if col in data.columns]]

print("\nFirst 5 tracks and features:")
print(data.head())

# ---------------------------
# Matplotlib Scatter Plot
# ---------------------------
plt.figure(figsize=(10,6))
scatter = plt.scatter(data['tempo'], data['energy'], c=data['danceability'], cmap='viridis', s=100)
plt.colorbar(scatter, label='Danceability')
plt.xlabel('Tempo')
plt.ylabel('Energy')
plt.title('Spotify Audio Features: Tempo vs Energy')
plt.show()

# ---------------------------
# Plotly Interactive Scatter
# ---------------------------
fig = px.scatter(
    data, x='tempo', y='energy', size='valence', color='danceability',
    hover_name='name', size_max=30, color_continuous_scale='Viridis',
    title='Interactive Spotify Audio Feature Visualization'
)
fig.show()

# ---------------------------
# KMeans Clustering
# ---------------------------
X = data[['danceability', 'energy', 'tempo']]
kmeans = KMeans(n_clusters=3, random_state=42).fit(X)
data['cluster'] = kmeans.labels_

fig3d = px.scatter_3d(
    data, x='tempo', y='energy', z='danceability', color='cluster',
    hover_name='name', title='3D Clustering of Songs'
)
fig3d.show()

print("\nData with clusters:")
print(data.head())
