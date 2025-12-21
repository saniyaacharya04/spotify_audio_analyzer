from fastapi import HTTPException, status

# Hardcoded valid API keys for demo (SaaS-style)
VALID_API_KEYS = {
    "demo-key": "free",
    "premium-key": "premium",
}

def validate_api_key(api_key: str) -> str:
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    return VALID_API_KEYS[api_key]
