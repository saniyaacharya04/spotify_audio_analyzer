from fastapi import FastAPI
from src.app.api.routes import router
from src.app.core.logging import setup_logging
from src.app.core.config import settings

setup_logging()

app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
