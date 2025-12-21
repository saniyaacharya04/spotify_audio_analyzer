from src.app.core.config import settings
from src.app.core.errors import UsageLimitExceeded

_usage_counter = {}


def check_and_increment(api_key: str):
    count = _usage_counter.get(api_key, 0)

    if count >= settings.daily_free_limit:
        raise UsageLimitExceeded()

    _usage_counter[api_key] = count + 1
