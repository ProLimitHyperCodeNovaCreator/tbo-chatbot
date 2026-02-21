# Personalization Agent

A production-ready ML-powered personalization service for travel booking platforms (TBO Hackathon).

---

## Project Structure

```
personaliaztion agent/
├── app/                      # Core application
│   ├── ml/
│   │   ├── ranker.py        # ML ranking
│   │   └── trainer.py       # Model training
│   ├── prisma/
│   │   └── schema.prisma    # DB schema
│   ├── cache.py
│   ├── config.py
│   ├── db.py
│   ├── exceptions.py
│   ├── features.py
│   ├── logger.py
│   ├── main.py
│   ├── metrics.py
│   ├── model.py
│   ├── routes.py
│   └── rules.py
│
├── mock_testing/             # Test without database
│   ├── config_mock.py
│   ├── mock_db.py
│   ├── trainer_mock.py
│   └── test_standalone.py
│
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── run.bat                   # Windows: setup / server / mock tests
├── run.sh                    # Linux/Mac runner
├── setup_db.py
└── test_api.py
```

---

## Features

- **ML-Based Ranking** — Learns from booking behavior to predict preferences
- **Rule-Based Scoring** — 5 tunable business rules applied instantly
- **Caching Layer** — In-memory cache with configurable TTL
- **Feedback Loop** — Continuous retraining from user interactions
- **Health Checks** — `/health` and `/metrics` endpoints for monitoring
- **Graceful Degradation** — Falls back to rules if ML model is unavailable

---

## Quick Start

### Option A — Test Without Database (Recommended for local dev)

No PostgreSQL needed. Runs entirely in-memory.

**Windows:**
```bat
run.bat
```
Choose **option 3 — Run Mock Tests**.

**Linux / Mac:**
```bash
chmod +x run.sh && ./run.sh
```
Choose **option 3 — Run Mock Tests**.

**Or run directly:**
```bash
cd mock_testing
python test_standalone.py
```

Mock test suite covers:
1. In-memory database
2. Rule-based scoring for 3 user profiles
3. ML model training (150 samples, ~1 second)
4. ML model scoring
5. Full personalization pipeline
6. Side-by-side user comparison

---

### Option B — Full Setup with PostgreSQL

**Windows:**
```bat
run.bat
```
Choose **option 1 — Setup**, then **option 2 — Start Server**.

**Manual steps:**
```bash
# 1. Copy env template and fill in DATABASE_URL
copy .env.example .env

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate Prisma client and push schema
prisma generate --schema=app/prisma/schema.prisma
prisma db push --schema=app/prisma/schema.prisma

# 4. Seed sample data (optional)
python setup_db.py

# 5. Start server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Docker (easiest full setup):**
```bash
docker-compose up -d
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check (DB + app) |
| POST | `/personalize` | Rank options for a user |
| POST | `/feedback` | Record acceptance/rejection |
| POST | `/train` | Trigger background retraining |
| GET | `/model/status` | ML model availability |
| GET | `/metrics` | Request counts, latency, cache stats |
| POST | `/cache/clear` | Flush in-memory cache |

### Example Request

```bash
curl -X POST http://localhost:8000/personalize \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-123",
    "options": [
      {
        "option_id": "hotel-1",
        "base_score": 0.85,
        "price_bucket": "mid",
        "distance_bucket": "near",
        "rating_bucket": "high",
        "supplier_id": "supplier-1",
        "refundable": true
      }
    ]
  }'
```

**Response:**
```json
{
  "user_id": "user-123",
  "total_options": 1,
  "ranked_options": [
    {
      "option_id": "hotel-1",
      "final_score": 1.516,
      "base_score": 0.85,
      "rule_score": 0.60,
      "ml_score": 0.066,
      "reasons": ["Matches budget preference", "Preferred supplier", "High rating match"]
    }
  ],
  "ml_available": true
}
```

---

## How Scoring Works

```
final_score = base_score + (rule_score x RULE_WEIGHT) + (ml_score x ML_WEIGHT)
```

**Business Rules** (`app/rules.py`):

| Rule | Boost | Condition |
|------|-------|-----------|
| Refundable preference | +0.20 | cancellation_rate > 30% AND option is refundable |
| Budget match | +0.15 | user.budget_pref == option.price_bucket |
| Preferred supplier | +0.25 | option.supplier_id in user.preferred_suppliers |
| High rating | +0.10 | user.refund_pref == "high" AND rating_bucket == "high" |
| Low conversion boost | +0.15 | agency conversion_rate < 10% AND price_bucket == "low" |

**ML Model** (`app/ml/`) — LogisticRegression trained on 5 features: price bucket, distance bucket, rating bucket, refundable flag, supplier ID.

---

## Configuration (`.env`)

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | required | PostgreSQL connection string |
| `DEBUG` | False | Enable debug mode |
| `LOG_LEVEL` | INFO | Logging level |
| `ENABLE_ML_SCORING` | True | Toggle ML scoring |
| `ENABLE_CACHING` | True | Toggle caching |
| `CACHE_TTL` | 300 | Cache TTL in seconds |
| `MAX_OPTIONS_PER_REQUEST` | 100 | Request size limit |
| `RULE_WEIGHT` | 1.0 | Multiplier for rule scores |
| `ML_WEIGHT` | 1.0 | Multiplier for ML scores |

Copy `.env.example` to `.env` to get started.

---

## Testing

**Without database:**
```bash
cd mock_testing && python test_standalone.py
```

**API integration tests (server must be running):**
```bash
python test_api.py
```

---

## Production Deployment

**Docker Compose** starts PostgreSQL + API on port 8000:
```bash
docker-compose up -d
```

**Production checklist:**
- [ ] `DEBUG=False` in `.env`
- [ ] Strong database password
- [ ] CORS origins restricted in `app/main.py`
- [ ] HTTPS enabled
- [ ] Rate limiting added
- [ ] Auth implemented
- [ ] `/health` wired to load balancer probes

---
