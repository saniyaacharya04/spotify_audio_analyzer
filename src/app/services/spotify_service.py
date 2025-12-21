from src.app.integrations.spotify_client import fetch_track_metadata

def analyze_track(track_id: str) -> dict:
    track = fetch_track_metadata(track_id)

    return {
        "track_name": track["name"],
        "artist": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "popularity": track["popularity"],
        "duration_ms": track["duration_ms"],
        "explicit": track["explicit"],
    }
