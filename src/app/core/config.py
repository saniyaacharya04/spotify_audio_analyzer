from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Spotify Audio Analyzer"
    environment: str = os.getenv("ENVIRONMENT", "local")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    daily_free_limit: int = 20


settings = Settings()
