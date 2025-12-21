import pytest
from src.app.services.usage_service import check_and_increment
from src.app.core.config import settings
from src.app.core.errors import UsageLimitExceeded

def test_usage_limit_exceeded():
    api_key = "limit-test-key"

    for _ in range(settings.daily_free_limit):
        check_and_increment(api_key)

    with pytest.raises(UsageLimitExceeded):
        check_and_increment(api_key)
