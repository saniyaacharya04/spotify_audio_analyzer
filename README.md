# Spotify Audio Analyzer

[![CI](https://github.com/saniyaacharya04/spotify_audio_analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/saniyaacharya04/spotify_audio_analyzer/actions)

A **backend-first, SaaS-style Spotify analysis service** built with **FastAPI**, **SQLAlchemy**, and **Spotify Web API**.
The system demonstrates **real API integration**, **API key authentication**, **usage-based rate limiting**, **premium feature gating**, and **end-to-end CI validation**.

This project is designed to be **recruiter-reviewable**, **interview-defendable**, and **production-realistic**.

---

## Key Capabilities

### 1. Real Spotify Data Integration

* Uses Spotify **Client Credentials Flow**
* Fetches real track metadata from Spotify Web API
* No mock data in production paths

### 2. SaaS-Style API Authentication

* API-key based access control
* Free and Premium plans
* Invalid key handling with proper HTTP semantics

### 3. Usage-Based Rate Limiting

* Daily request limits for free users
* Persistent usage tracking via database
* Clean error signaling when limits are exceeded

### 4. Premium Feature Gating

* Premium-only endpoints protected at API layer
* Audio features endpoint intentionally gated
* Placeholder clearly documents OAuth Authorization Code requirement

### 5. Clean Architecture

* Layered structure: API → Services → Integrations → Domain
* Clear separation of concerns
* Testable, maintainable modules

### 6. Full CI Discipline

* Unit tests with isolated in-memory database
* End-to-end API tests using real HTTP calls
* GitHub Actions pipeline with Python version matrix
* CI badge reflecting repository health

---

## Tech Stack

* Python 3.9 – 3.11
* FastAPI
* SQLAlchemy
* SQLite
* Spotify Web API
* Pytest
* GitHub Actions
* Docker

---

## Project Structure

```
spotify_audio_analyzer/
├── src/
│   ├── app/
│   │   ├── api/            # FastAPI routes
│   │   ├── services/       # Business logic
│   │   ├── integrations/   # Spotify API client
│   │   ├── core/           # Config, DB, errors
│   │   └── domain/         # Domain logic
│   └── main.py             # App entrypoint
├── tests/
│   ├── unit/               # Fast unit tests (in-memory DB)
│   └── e2e/                # API-level integration tests
├── scripts/
│   └── e2e.sh              # Full end-to-end test script
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .github/workflows/ci.yml
├── Makefile
├── requirements.txt
├── LICENSE
└── README.md
```

---

## API Overview

### Health Check

```
GET /health
```

### Track Metadata (Free)

```
GET /analyze/{track_id}
Header: X-API-Key
```

Returns:

* Track name
* Artist
* Album
* Popularity
* Duration
* Explicit flag

### Premium Audio Features (Gated)

```
POST /premium/audio-features/{track_id}
Header: X-API-Key
```

* Free users receive `402 Payment Required`
* Premium users receive a documented placeholder response
* Designed for OAuth Authorization Code flow extension

---

## Environment Variables

Create a `.env` file (not committed):

```
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
```

---

## Local Development

### Setup

```
conda create -n spotify-audio-analyzer python=3.10
conda activate spotify-audio-analyzer
pip install -r requirements.txt
```

### Run API

```
uvicorn src.main:app --reload
```

### Run Unit Tests

```
pytest tests/unit -v
```

### Run Full End-to-End Tests

```
chmod +x scripts/e2e.sh
./scripts/e2e.sh
```

---

## CI Pipeline

The GitHub Actions workflow performs:

1. Python syntax validation
2. Unit tests with in-memory SQLite
3. End-to-end API tests
4. Multi-version Python validation (3.9, 3.10, 3.11)

All checks must pass before merge.

---

## Design Decisions (Intentional)

* Audio features endpoint gated to reflect real Spotify OAuth constraints
* Client Credentials used only where allowed by Spotify policy
* In-memory DB for unit tests to ensure speed and isolation
* File-based DB only used in runtime/E2E paths
* Explicit SaaS-style error handling instead of silent failures

---

## License

MIT License

---

## Author

Saniya Acharya
B.Tech Computer Science Engineering
Backend / Systems / API Engineering Focus


