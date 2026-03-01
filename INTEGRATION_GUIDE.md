# TBO ChatBot Platform - Integrated Guide

## Overview
This is a centralized **Travel Booking Orchestrator** that links three main components:
1. **Orchestrator Agent** - LLM-powered query router with Phi4/Llama2
2. **Hotel Search Engine** - Real-world hotel inventory search
3. **TBO Vector DB** - Travel data with Qdrant RAG for intelligent retrieval

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT APPLICATION                       │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│         ORCHESTRATOR AGENT (FastAPI:8000)                   │
│  ├─ Query Processing (/query)                               │
│  ├─ JSON Input Processing (/json/process)                   │
│  ├─ RAG-Enhanced Queries (/rag/query)                        │
│  ├─ Hotel Search (/search/hotels)                           │
│  ├─ Flight Search (/search/flights)                         │
│  └─ Full Orchestration (/orchestrate)                       │
└┬───────────────────────────────────────────────────────────┬┘
 │                                                             │
 ├─────────────┐               ┌──────────────────┐           │
 │             │               │                  │           │
 ▼             ▼               ▼                  ▼           ▼
[Phi4]    [Llama2]      [Hotel Search]      [Qdrant]      [Redis]
[Ollama]  [Ollama]      [Flask:5000]        [VectorDB]    [Cache]
```

## Quick Start

### 1. Configure Environment
```bash
cd C:\Users\DELL\Desktop\pathway\tbo-chatbot
# Edit .env with your settings
```

### 2. Start All Services
```bash
docker-compose up --build
```

Services will start in order:
- Redis (6379) - Caching
- PostgreSQL (5432) - Database
- Qdrant (6333) - Vector DB
- Ollama (11434) - LLM Models
- Hotel Search (5000) - Hotel Engine
- Orchestrator (8000) - Main API

### 3. Verify Setup
```bash
# Health check
curl http://localhost:8000/health

# List available collections
curl http://localhost:6333/collections
```

## API Endpoints

### Hotel Search (Simple)
```bash
POST http://localhost:8000/search/hotels

{
  "location": "Athens, Greece",
  "check_in": "2026-03-15",
  "check_out": "2026-03-20",
  "guests": 2,
  "user_id": "user123"
}
```

### JSON Query Processing (Structured)
```bash
POST http://localhost:8000/json/process

{
  "query_type": "hotel",
  "location": "Paris, France",
  "check_in": "2026-03-10",
  "check_out": "2026-03-15",
  "guests": 2,
  "preferences": {
    "min_rating": 4.0,
    "max_price": 250
  },
  "user_id": "user123",
  "use_rag": true
}
```

### RAG Query (Advanced)
```bash
POST http://localhost:8000/rag/query

{
  "query_type": "travel_package",
  "destination": "Santorini",
  "departure_date": "2026-03-20",
  "return_date": "2026-03-27",
  "passengers": 2,
  "preferences": {
    "budget": "luxury",
    "interests": ["beaches", "culture"]
  },
  "user_id": "user123",
  "use_rag": true
}
```

### Natural Language Query
```bash
POST http://localhost:8000/query

{
  "query": "Find me a luxury 5-star hotel in Rome for 3 nights, departing March 15",
  "user_id": "user123",
  "context": {
    "check_in": "2026-03-15",
    "check_out": "2026-03-18",
    "guests": 2
  }
}
```

### Full Orchestration
```bash
POST http://localhost:8000/orchestrate

{
  "query": "I want to book a flight and hotel to Barcelona for 5 days starting March 20",
  "user_id": "user123",
  "context": {
    "origin": "Athens",
    "destination": "Barcelona",
    "location": "Barcelona",
    "departure_date": "2026-03-20",
    "return_date": "2026-03-25",
    "check_in": "2026-03-20",
    "check_out": "2026-03-25",
    "passengers": 2,
    "guests": 2
  }
}
```

## Data Flow

### RAG-Enhanced Query Flow
```
User Query (JSON)
      ↓
┌─────▼──────────────────────┐
│  Complexity Detection       │
│  (Simple vs Complex)        │
└─────┬──────────────────────┘
      ↓
┌─────▼──────────────────────┐
│  Hotel Search Engine        │ ──→ Real-world hotel data
│  (Flask API:5000)           │
└─────┬──────────────────────┘
      ↓
┌─────▼──────────────────────┐
│  Qdrant Vector DB           │ ──→ Travel packages, routes
│  (RAG Search)               │
└─────┬──────────────────────┘
      ↓
┌─────▼──────────────────────┐
│  Context Building           │
│  (Combine all sources)      │
└─────┬──────────────────────┘
      ↓
┌─────▼──────────────────────┐
│  LLM Analysis               │
│  (Phi4 or Llama2)           │
└─────┬──────────────────────┘
      ↓
┌─────▼──────────────────────┐
│  Personalization Ranking    │
│  (User preferences)         │
└─────┬──────────────────────┘
      ↓
  Response with:
  - Hotels (name, price, rating)
  - Travel packages
  - LLM Analysis
  - Personalized recommendations
```

## Component Details

### Orchestrator Agent (`/orchestrator-agent`)
**Role**: Main API hub, query routing, RAG orchestration

**Key Features**:
- Complexity detection (simple/complex queries)
- Dynamic agent routing
- RAG integration with Qdrant
- Hotel search integration
- LLM analysis (Phi4/Llama2)
- Personalization support

**Environment Variables**:
```
OLLAMA_HOST=http://ollama:11434
HOTEL_SEARCH_URL=http://hotel-search:5000
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

### Hotel Search Engine (`/hotel-search-engine`)
**Role**: Hotel inventory search

**Features**:
- Real-world hotel data search
- Price and rating filtering
- Multiple result formats
- Cost analysis

**API**: `POST /search`
```json
{
  "query": "5-star hotels in Athens",
  "num_results": 10
}
```

### TBO Vector DB (`/tbo`)
**Role**: Travel data storage and RAG retrieval

**Features**:
- Qdrant vector database
- Travel package embeddings
- Redis caching
- Data pipeline processing

**Collections**:
- `travel_data` - Travel packages, routes, destinations
- `flight_options` - Flight data with embeddings
- `hotel_inventory` - Hotel embeddings and metadata

## Troubleshooting

### Ollama Models Not Loading
```bash
# Check Ollama status
curl http://localhost:11434/api/tags

# Manual model pull
curl -X POST http://localhost:11434/api/pull \
  -H "Content-Type: application/json" \
  -d '{"name":"llama2:latest","stream":false}'
```

### Vector DB Not Available
```bash
# Check Qdrant health
curl http://localhost:6333/readyz

# View collections
curl http://localhost:6333/collections
```

### Hotel Search Service Down
```bash
# Check health
curl http://localhost:5000/health

# Logs
docker logs tbo-hotel-search
```

### Database Connection Issues
```bash
# Check PostgreSQL
docker logs tbo-postgres

# Use adminer UI
http://localhost:8080
```

## Configuration Reference

### Model Selection
Edit orchestrator-agent config to switch models:
```python
# In app/config.py
phi4_model: str = "phi4:latest"      # Fast, lightweight
llama_model: str = "llama2:latest"   # Powerful, detailed
complexity_threshold: float = 0.6    # Threshold for complex queries
```

### Vector DB Settings
```python
qdrant_host: str = "qdrant"
qdrant_port: int = 6333
qdrant_api_key: str = ""  # For SaaS deployments
```

### Complexity Detection
```python
# Queries below threshold use Phi4
# Queries above threshold use Llama2
complexity_threshold: float = 0.6
```

## Monitoring

### Logs
```bash
# Orchestrator
docker logs tbo-orchestrator -f

# Hotel Search
docker logs tbo-hotel-search -f

# TBO Pipeline
docker logs tbo-pipeline -f

# Ollama
docker logs tbo-ollama -f
```

### Metrics
- Query latency: Check Orchestrator logs
- RAG retrieval time: Monitor Qdrant queries
- Hotel search performance: Check Flask logs

### DB Management
Access adminer UI: http://localhost:8080
- Database: orchestrator
- User: user
- Password: password

## Development

### Running Individually
```bash
# Orchestrator only
cd orchestrator-agent
python -m uvicorn app.main:app --reload --port 8000

# Hotel Search
cd hotel-search-engine
python app.py

# TBO Pipeline
cd tbo
python kafka_consumer.py
```

### Testing RAG Pipeline
```bash
# From orchestrator-agent
python quick_test.py

# Custom test
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query_type": "hotel",
    "location": "Barcelona",
    "check_in": "2026-03-20",
    "check_out": "2026-03-25",
    "guests": 2,
    "use_rag": true
  }'
```

## Architecture Decisions

### Why This Setup?
1. **Ollama (Phi4 + Llama2)** - Open source, self-hosted LLM execution
2. **Qdrant** - Purpose-built vector DB for RAG
3. **Redis** - Fast caching and message queue
4. **Hotel Search as Service** - Isolated, testable module
5. **PostgreSQL** - Persistent state and query history

### JSON Input Format
All endpoints accept JSON for:
- Type-safe input validation
- Structured data analysis by LLMs
- Easy integration with frontend applications
- Clear separation of concerns

### RAG Integration
1. Query → Hotel Search (real-time)
2. Query → Vector DB (historical/patterns)
3. Combine → LLM Analysis
4. Output → Personalized recommendations

## Performance Tips

1. **Cache frequently searched cities** in Redis
2. **Batch vector DB queries** for similar destinations
3. **Use Phi4** for simple, fast queries (< 100ms)
4. **Use Llama2** for complex analysis (< 5s)
5. **Monitor Qdrant index size** for optimal search speed

## Success Metrics

- Orchestrator response: < 2 seconds
- Hotel search: < 500ms
- RAG retrieval: < 1 second
- LLM analysis: < 5 seconds
- End-to-end: < 8 seconds

---

**Status**: Production Ready 🚀
**Last Updated**: March 1, 2026
