# app.py
import os
from dotenv import load_dotenv       # ✅ load environment variables
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans

# ---------------------------
# Load Spotify credentials from .env
# ---------------------------
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
    st.error("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in your environment variables (.env file).")
    st.stop()

# Spotify authentication
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# ---------------------------
# Streamlit page config
# ---------------------------
st.set_page_config(page_title="Spotify Audio Feature Analyzer", layout="wide")
st.title("Spotify Audio Feature Analyzer")

# ---------------------------
# Sidebar Controls
# ---------------------------
st.sidebar.header("Settings")

audio_features_options = [
    'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 
    'acousticness', 'instrumentalness', 'liveness', 'valence', 
    'tempo', 'duration_ms', 'time_signature'
]

num_clusters = st.sidebar.slider("Number of Clusters (KMeans)", min_value=2, max_value=10, value=3)
feature_x = st.sidebar.selectbox("X-axis Feature", options=audio_features_options, index=10)
feature_y = st.sidebar.selectbox("Y-axis Feature", options=audio_features_options, index=1)
feature_size = st.sidebar.selectbox("Bubble Size Feature", options=audio_features_options, index=0)
feature_color = st.sidebar.selectbox("Color Feature", options=audio_features_options, index=0)
clustering_features = st.sidebar.multiselect(
    "Select Features for Clustering",
    options=audio_features_options,
    default=['danceability','energy','tempo']
)
show_matplotlib = st.sidebar.checkbox("Show Matplotlib 2D Scatter", value=True)
show_plotly = st.sidebar.checkbox("Show Plotly 2D Scatter", value=True)
show_3d = st.sidebar.checkbox("Show Plotly 3D Clustering", value=True)

# ---------------------------
# Input Playlist
# ---------------------------
playlist_input = st.text_input("Enter Spotify Playlist ID or URL:")

if playlist_input:
    # Extract playlist ID
    if "playlist" in playlist_input:
        try:
            playlist_id = playlist_input.split("playlist/")[1].split("?")[0]
        except IndexError:
            st.error("Invalid Spotify playlist URL")
            st.stop()
    else:
        playlist_id = playlist_input

    st.info("Fetching playlist tracks...")

    tracks = []
    offset = 0
    while True:
        response = sp.playlist_tracks(playlist_id, limit=100, offset=offset)
        items = response['items']
        if not items:
            break
        tracks.extend(items)
        offset += len(items)

    if len(tracks) == 0:
        st.warning("No tracks found in the playlist.")
        st.stop()

    st.success(f"Fetched {len(tracks)} tracks!")

    track_ids = [track['track']['id'] for track in tracks if track['track'] is not None]
    track_names = [track['track']['name'] for track in tracks if track['track'] is not None]

    # ---------------------------
    # Fetch Audio Features
    # ---------------------------
    audio_features = sp.audio_features(track_ids)
    data = pd.DataFrame(audio_features)
    data['name'] = track_names

    # Keep all common Spotify audio features
    columns_to_keep = ['name'] + [f for f in audio_features_options if f in data.columns]
    data = data[columns_to_keep]

    st.subheader("Preview of Tracks and Features")
    st.dataframe(data.head(10))

    # ---------------------------
    # Tabs
    # ---------------------------
    tabs = st.tabs(["2D Scatter", "3D Clustering", "Cluster Summary & Radar", "Download Data"])

    # ---------------------------
    # 2D Scatter
    # ---------------------------
    with tabs[0]:
        st.subheader("2D Scatter Plots")
        if show_matplotlib:
            fig, ax = plt.subplots(figsize=(10,6))
            scatter = ax.scatter(
                data[feature_x], data[feature_y],
                c=data[feature_color],
                s=data[feature_size]*50,
                cmap='viridis',
                alpha=0.7
            )
            fig.colorbar(scatter, ax=ax, label=feature_color)
            ax.set_xlabel(feature_x.capitalize())
            ax.set_ylabel(feature_y.capitalize())
            ax.set_title(f"{feature_y.capitalize()} vs {feature_x.capitalize()} (Matplotlib)")
            st.pyplot(fig)

        if show_plotly:
            fig2 = px.scatter(
                data, x=feature_x, y=feature_y, size=feature_size, color=feature_color,
                hover_name='name', size_max=30, color_continuous_scale='Viridis',
                title=f"{feature_y.capitalize()} vs {feature_x.capitalize()} (Plotly Interactive)"
            )
            st.plotly_chart(fig2)

    # ---------------------------
    # 3D Clustering
    # ---------------------------
    with tabs[1]:
        st.subheader("Dynamic KMeans Clustering")
        if len(clustering_features) < 2:
            st.warning("Select at least 2 features for clustering")
        else:
            X = data[clustering_features]
            kmeans = KMeans(n_clusters=num_clusters, random_state=42).fit(X)
            data['cluster'] = kmeans.labels_

            if show_3d:
                if len(clustering_features) >= 3:
                    fig3d = px.scatter_3d(
                        data,
                        x=clustering_features[0],
                        y=clustering_features[1],
                        z=clustering_features[2],
                        color='cluster',
                        hover_name='name',
                        title=f"3D Clustering of Songs (K={num_clusters})"
                    )
                else:
                    fig3d = px.scatter(
                        data,
                        x=clustering_features[0],
                        y=clustering_features[1],
                        color='cluster',
                        hover_name='name',
                        title=f"2D Clustering of Songs (K={num_clusters})"
                    )
                st.plotly_chart(fig3d)

    # ---------------------------
    # Cluster Summary & Radar Charts
    # ---------------------------
    with tabs[2]:
        st.subheader("Cluster Summary & Radar Charts")
        if 'cluster' not in data.columns:
            st.info("Clusters not generated yet. Go to 3D Clustering tab first.")
        else:
            summary = data.groupby('cluster')[clustering_features].mean()
            summary['size'] = data['cluster'].value_counts().sort_index()
            st.dataframe(summary.style.background_gradient(subset=clustering_features, cmap='Greens').format("{:.2f}"))

            st.markdown("### Top Songs per Cluster")
            top_feature_for_sort = st.selectbox(
                "Select feature to sort top songs in each cluster",
                options=clustering_features,
                index=0
            )
            for cluster_num in range(num_clusters):
                cluster_data = data[data['cluster'] == cluster_num]
                cluster_top = cluster_data.sort_values(by=top_feature_for_sort, ascending=False)
                st.markdown(f"**Cluster {cluster_num}**")
                st.dataframe(cluster_top[['name'] + clustering_features].head(10))

            # Radar Chart
            st.markdown("### Feature Comparison Radar Chart per Cluster")
            radar_features = st.multiselect(
                "Select features for radar chart",
                options=clustering_features,
                default=clustering_features
            )
            if radar_features:
                fig_radar = go.Figure()
                for cluster_num in range(num_clusters):
                    cluster_means = summary.loc[cluster_num, radar_features].values
                    fig_radar.add_trace(go.Scatterpolar(
                        r=cluster_means,
                        theta=radar_features,
                        fill='toself',
                        name=f'Cluster {cluster_num}'
                    ))
                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True)),
                    showlegend=True,
                    title="Radar Chart: Average Feature Values per Cluster"
                )
                st.plotly_chart(fig_radar)

    # ---------------------------
    # Download Data
    # ---------------------------
    with tabs[3]:
        st.subheader("Download Audio Features Data")
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='spotify_audio_features.csv',
            mime='text/csv'
        )
