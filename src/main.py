from fastapi import FastAPI
from src.app.api.routes import router
from src.app.core.logging import setup_logging
from src.app.core.config import settings
from src.app.core.db.session import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
