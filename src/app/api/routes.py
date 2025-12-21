from fastapi import APIRouter, Header
from src.app.services.spotify_service import analyze_track
from src.app.services.usage_service import check_and_increment

router = APIRouter()


@router.get("/analyze/{track_id}")
def analyze(track_id: str, x_api_key: str = Header(...)):
    check_and_increment(x_api_key)
    return analyze_track(track_id)
