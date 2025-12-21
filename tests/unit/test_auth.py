import pytest
from fastapi import HTTPException
from src.app.services.auth_service import validate_api_key

def test_valid_free_key():
    assert validate_api_key("demo-key") == "free"

def test_valid_premium_key():
    assert validate_api_key("premium-key") == "premium"

def test_invalid_key_raises():
    with pytest.raises(HTTPException) as exc:
        validate_api_key("invalid-key")
    assert exc.value.status_code == 401
