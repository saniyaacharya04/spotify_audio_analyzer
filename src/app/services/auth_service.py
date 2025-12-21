from fastapi import HTTPException, status

# Demo SaaS key registry
VALID_API_KEYS = {
    "demo-key": "free",
    "premium-key": "premium",
    "limit-test-key": "free",   # explicitly supported for E2E
}

def validate_api_key(api_key: str) -> str:
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return VALID_API_KEYS[api_key]
