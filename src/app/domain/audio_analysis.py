def analyze_audio_features(features: dict) -> dict:
    """
    Pure domain logic.
    """
    return {
        "danceability": features.get("danceability"),
        "energy": features.get("energy"),
        "tempo": features.get("tempo"),
        "valence": features.get("valence"),
    }
