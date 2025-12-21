import os
import sys
from pathlib import Path

# Force in-memory DB for unit tests
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))
