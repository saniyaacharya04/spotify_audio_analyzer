import os
import sys
from pathlib import Path
import pytest

# Force temp file DB for tests to share schema across connections
os.environ["DATABASE_URL"] = "sqlite:////tmp/test_spotify_db.sqlite"

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.app.core.db.session import engine, Base
import src.app.core.db.models  # noqa: F401

@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
