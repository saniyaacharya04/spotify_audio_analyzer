from src.app.integrations.spotify_client import fetch_audio_features
from src.app.domain.audio_analysis import analyze_audio_features


def analyze_track(track_id: str) -> dict:
    raw_features = fetch_audio_features(track_id)
    return analyze_audio_features(raw_features)
