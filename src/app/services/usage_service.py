from datetime import date
from sqlalchemy.orm import Session

from src.app.core.config import settings
from src.app.core.errors import UsageLimitExceeded
from src.app.core.db.session import SessionLocal
from src.app.core.db.models import ApiUsage


def check_and_increment(api_key: str):
    db: Session = SessionLocal()
    today = date.today()

    usage = (
        db.query(ApiUsage)
        .filter(ApiUsage.api_key == api_key, ApiUsage.date == today)
        .first()
    )

    if not usage:
        usage = ApiUsage(api_key=api_key, date=today, count=0)
        db.add(usage)

    if usage.count >= settings.daily_free_limit:
        db.close()
        raise UsageLimitExceeded()

    usage.count += 1
    db.commit()
    db.close()
