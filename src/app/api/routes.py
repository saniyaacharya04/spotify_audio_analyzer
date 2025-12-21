from fastapi import APIRouter, Header, HTTPException, status
from src.app.services.spotify_service import analyze_track
from src.app.services.usage_service import check_and_increment
from src.app.services.auth_service import validate_api_key

router = APIRouter()


@router.get("/analyze/{track_id}")
def analyze(track_id: str, x_api_key: str = Header(...)):
    plan = validate_api_key(x_api_key)
    if plan == "free":
        check_and_increment(x_api_key)
    return analyze_track(track_id)


@router.post("/premium/batch-analyze")
def premium_batch_analyze(x_api_key: str = Header(...)):
    plan = validate_api_key(x_api_key)
    if plan != "premium":
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Premium feature. Upgrade required.",
        )
    return {"message": "Batch analysis placeholder"}


@router.post("/billing/upgrade")
def billing_upgrade():
    return {"message": "Billing upgrade placeholder"}


@router.post("/billing/webhook")
def billing_webhook():
    return {"message": "Billing webhook placeholder"}

from src.app.services.auth_service import validate_api_key
from src.app.core.errors import PremiumFeatureLocked


@router.post("/premium/audio-features/{track_id}")
def premium_audio_features(track_id: str, x_api_key: str = Header(...)):
    plan = validate_api_key(x_api_key)

    if plan != "premium":
        raise PremiumFeatureLocked()

    return {
        "message": "Premium Audio Features placeholder",
        "note": "Requires user-authorized Spotify OAuth flow (Authorization Code)."
    }
