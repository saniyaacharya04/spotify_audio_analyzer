from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_analyze_free_key():
    r = client.get("/analyze/123", headers={"X-API-Key": "demo-key"})
    assert r.status_code == 200
    assert "danceability" in r.json()

def test_invalid_api_key():
    r = client.get("/analyze/123", headers={"X-API-Key": "bad-key"})
    assert r.status_code == 401

def test_premium_feature_blocked():
    r = client.post("/premium/batch-analyze", headers={"X-API-Key": "demo-key"})
    assert r.status_code == 402

def test_premium_feature_allowed():
    r = client.post("/premium/batch-analyze", headers={"X-API-Key": "premium-key"})
    assert r.status_code == 200
