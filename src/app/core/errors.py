from fastapi import HTTPException, status


class UsageLimitExceeded(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Daily free usage limit exceeded. Upgrade required.",
        )


class PremiumFeatureLocked(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Premium feature. Upgrade required.",
        )
class PremiumFeatureLocked(Exception):
    pass
