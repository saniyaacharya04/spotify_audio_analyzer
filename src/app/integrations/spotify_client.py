def fetch_audio_features(track_id: str) -> dict:
    """
    Mocked Spotify API client.
    Replace with real Spotify API later.
    """
    return {
        "danceability": 0.81,
        "energy": 0.72,
        "tempo": 120.5,
        "valence": 0.64,
    }
