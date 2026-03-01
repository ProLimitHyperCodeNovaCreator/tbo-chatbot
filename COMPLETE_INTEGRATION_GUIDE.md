# Complete System Integration Guide - Travel Recommendation Platform

## System Overview

This guide explains how all three components (Orchestrator Agent, Hotel Search Engine, and TBO Vector DB) are linked together to provide intelligent travel recommendations with LLM analysis.

### Architecture Diagram

```
User Request (with detailed profile)
        ↓
┌──────────────────────────────────────────────────────────┐
│         ORCHESTRATOR AGENT (FastAPI - Port 8000)          │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ STEP 1: Receive User Request                        │ │
│  │ - Origin, destination, dates, budget                │ │
│  │ - User preferences, travel style                    │ │
│  │ - Business rules and profit constraints             │ │
│  └────────────┬────────────────────────────────────────┘ │
│               ↓                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ STEP 2: Hotel Search (Parallel Request)             │ │
│  │ → Calls Hotel Search Engine (Port 5000)             │ │
│  │ ← Returns: 5-8 hotel options with details           │ │
│  └────────────┬────────────────────────────────────────┘ │
│               ↓                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ STEP 3: Travel Data Search (Parallel Request)       │ │
│  │ → Queries Qdrant Vector DB (Port 6333)              │ │
│  │ ← Returns: Flight options, travel packages          │ │
│  └────────────┬────────────────────────────────────────┘ │
│               ↓                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ STEP 4: Package Combinations                        │ │
│  │ - Creates multiple combos of hotels + flights       │ │
│  │ - Calculates profit for each combination            │ │
│  │ - Selects top 5 combinations                        │ │
│  └────────────┬────────────────────────────────────────┘ │
│               ↓                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ STEP 5: LLM Analysis (Complex Reasoning)            │ │
│  │ → Sends all 5 options to Ollama (Port 11434)        │ │
│  │ ← LLM analyzes and selects BEST option              │ │
│  └────────────┬────────────────────────────────────────┘ │
│               ↓                                            │
│  ┌─────────────────────────────────────────────────────┐ │
│  │ STEP 6: Response Compilation                        │ │
│  │ - All 5 recommendations with rankings               │ │
│  │ - Best choice highlighted with reasoning            │ │
│  │ - Profit metrics and comparison summary             │ │
│  │ - Complete journey itinerary                        │ │
│  └────────────┬────────────────────────────────────────┘ │
│               ↓                                            │
└────────────────────────────────────────────────────────┘
        ↓
   JSON Response (with all options + best choice)
```

---

## Component Integration Details

### 1. ORCHESTRATOR AGENT (Port 8000)

**Role**: Central hub that orchestrates the entire recommendation flow

**Key Files**:
- `app/main.py` - Main FastAPI application with endpoints
- `app/ml/rag_engine.py` - Vector DB integration
- `app/integrations/hotel_search_integration.py` - Hotel search API wrapper
- `app/ml/model_router.py` - Routes queries to appropriate LLM

**Endpoints**:
```
GET  /health                          # Service health check
POST /recommend/travel-plan           # Main recommendation endpoint
POST /query                           # Standard query processing
POST /json/process                    # JSON-formatted queries
```

**Request Example**:
```json
{
  "origin": "New York (JFK)",
  "destination": "Paris, France",
  "check_in": "2026-04-15",
  "check_out": "2026-04-22",
  "passengers": 1,
  "budget": 5000,
  "user_id": "user_123",
  "travel_style": "luxury",
  "user_preferences": {
    "hotel_rating_min": 4.5,
    "amenities": ["spa", "fine dining"]
  },
  "profit_priority": true,
  "business_rules": {
    "markup_percentage": 20,
    "bundle_discount": 5
  }
}
```

### 2. HOTEL SEARCH ENGINE (Port 5000)

**Role**: Provides real-time hotel inventory and search functionality

**Technology**: Flask + Search AI

**Key Files**:
- `app.py` - Flask application
- `search_engine.py` - Search logic
- `requirements.txt` - Dependencies

**Endpoints**:
```
GET  /health                          # Service health check
POST /search                          # Hotel search query
```

**Request/Response Example**:
```json
REQUEST:
{
  "query": "5 star hotels in Paris",
  "num_results": 5
}

RESPONSE:
{
  "status": "success",
  "results": [
    {
      "id": "hotel_001",
      "name": "The Ritz-Carlton Paris",
      "rating": 4.8,
      "price_per_night": 450,
      "location": "Place Vendôme",
      "amenities": ["spa", "restaurants"]
    },
    ...
  ]
}
```

### 3. QDRANT VECTOR DATABASE (Port 6333)

**Role**: Semantic search for travel packages, routes, and historical data

**Technology**: Qdrant - Vector similarity search

**Key Files**:
- `connect.py` - Connection configuration
- `qdrant_ingest.py` - Data ingestion script
- Collections: travel_data, flight_options, hotel_inventory

**Data Structure**:
- Travel packages (destination, duration, inclusions)
- Flight routes (origin, destination, airlines)
- Hotel inventory (names, ratings, locations)

**Endpoints**:
```
GET  /health                          # Service health check
POST /search                          # Vector similarity search
```

**RAG Integration** (in Orchestrator):
```python
# Semantic search for travel packages
travel_packages = await rag_engine.search_travel_data(
    query="flights from New York to Paris April 2026",
    collection="travel_data",
    limit=5
)
```

### 4. OLLAMA LLM SERVICE (Port 11434)

**Role**: Intelligent analysis and recommendation selection

**Technology**: Ollama (runs locally)
- Model: phi4 (lightweight for simple queries)
- Model: llama2 (for complex analysis)

**Usage in Orchestrator**:
```python
# Complex analysis routed to Llama2
llm_response = await model_router.route_query(
    query=context_with_all_options,
    complexity_level="complex"
)
```

---

## Integration Flow - Step by Step

### Step 1: User Submits Detailed Request
```
POST http://localhost:8000/recommend/travel-plan
Content-Type: application/json

{
  "origin": "New York (JFK)",
  "destination": "Paris, France",
  "check_in": "2026-04-15",
  "check_out": "2026-04-22",
  "passengers": 1,
  "budget": 5000,
  "user_name": "James Anderson",
  "travel_style": "luxury",
  "user_preferences": {
    "hotel_rating_min": 4.5,
    "amenities": ["spa", "fine dining"]
  }
}
```

### Step 2: Orchestrator Searches Hotels
```python
# In orchestrator/app/main.py line ~195
hotel_results = await hotel_search_integration.search_hotels(
    query="Paris, France 2026-04-15 to 2026-04-22",
    num_results=8
)

# Makes HTTP request to:
POST http://localhost:5000/search
{
  "query": "Paris hotels",
  "num_results": 8
}

# Returns 8 hotels with ratings, prices, locations
```

### Step 3: Orchestrator Searches Vector DB
```python
# In orchestrator/app/main.py line ~210
travel_packages = await rag_engine.search_travel_data(
    query="flights New York to Paris April 2026",
    collection="travel_data",
    limit=5
)

# Internally:
# 1. Converts text to embeddings → similarity search in Qdrant
# 2. Returns semantically similar travel packages
```

### Step 4: Create Package Combinations
```python
# In orchestrator/app/main.py line ~265
# For each hotel × each flight → create package combinations
all_package_combinations = []
for hotel in top_4_hotels:
    for flight in top_3_flights:
        package = {
            "hotel": hotel,
            "flight": flight,
            "total_cost": hotel_cost + flight_cost,
            "profit_metrics": {...}  # Calculated
        }
        all_package_combinations.append(package)

# Result: 4 × 3 = 12 combinations, ranked by profit → top 5 selected
```

### Step 5: LLM Analyzes All Options
```python
# In orchestrator/app/main.py line ~290

# Build comprehensive prompt with all 5 options
llm_context = """
INTELLIGENT TRAVEL RECOMMENDATION - MULTI-OPTION ANALYSIS

USER REQUEST:
- Origin: New York (JFK)
- Destination: Paris, France
- Travel Dates: 2026-04-15 to 2026-04-22
- Travel Style: luxury
- Budget: $5000

TOP 5 RECOMMENDED PACKAGES:

OPTION 1:
Hotel: The Ritz-Carlton Paris (4.8/5)
Flight: Air France $450
Package Total: $3,700
Platform Profit: $555 (Margin: 15%)

OPTION 2:
...

[All 5 options presented]

YOUR TASK: Select and explain the BEST option
"""

# Send to Ollama LLM
llm_response = await model_router.route_query(
    query=llm_context,
    complexity_level="complex"  # Uses Llama2
)

# LLM analyzes and selects best option based on:
# 1. User preferences match
# 2. Hotel ratings/amenities
# 3. Platform profit maximization
# 4. Budget alignment
```

### Step 6: Return Comprehensive Response
```python
# In orchestrator/app/main.py line ~370

return TravelRecommendationResponse(
    status="success",
    all_recommendations=[
        # All 5 ranked options with full details
        {
            "rank": 1,
            "hotel": {...},
            "flight": {...},
            "total_cost": 3700,
            "profit_metrics": {...}
        },
        ...
    ],
    recommendation={
        # Best choice selected by LLM
        "rank": 1,
        "hotel": {...},
        "flight": {...},
        "platform_profit": 555
    },
    analysis="LLM's detailed analysis text",
    reasoning="Why this is the best option",
    comparison_summary="Side-by-side comparison of all 5",
    profit_metrics={...},
    roi_analysis={...},
    complete_journey={...}
)
```

---

## Data Flow Summary

| Step | Component | Operation | Input | Output |
|------|-----------|-----------|-------|--------|
| 1 | Orchestrator | Parse request | User details | Validated profile |
| 2 | Hotel Search | Search hotels | Query string | 8 hotels ranked by relevance |
| 3 | Qdrant | Semantic search | Destination/dates | 5 travel packages/flights |
| 4 | Orchestrator | Combine options | Hotels × Flights | 12 combinations → top 5 |
| 5 | Orchestrator | Calculate profit | Each combination | Commission, margins calculated |
| 6 | Ollama/LLM | Analyze & select | All 5 options | Best choice + reasoning |
| 7 | Orchestrator | Compile response | Analysis + options | JSON response (7 sections) |

---

## Key Integration Points

### 1. Hotel Search Integration
**File**: `orchestrator-agent/app/integrations/hotel_search_integration.py`

```python
class HotelSearchIntegration:
    async def search_hotels(self, query: str, num_results: int, preferences: Dict):
        # Makes HTTP request to Hotel Search Engine
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{HOTEL_SEARCH_URL}/search",
                json={"query": query, "num_results": num_results},
                timeout=10
            )
        return response.json()
```

### 2. RAG Engine Integration
**File**: `orchestrator-agent/app/ml/rag_engine.py`

```python
class RAGEngine:
    async def search_travel_data(self, query: str, collection: str, limit: int):
        # Semantic search in Qdrant vector database
        # Converts text query to embedding
        # Finds similar travel packages/flights
        # Returns relevant results
```

### 3. LLM Model Routing
**File**: `orchestrator-agent/app/ml/model_router.py`

```python
class ModelRouter:
    async def route_query(self, query: str, complexity_level: str):
        # Routes to Phi4 (simple, fast) or Llama2 (complex, accurate)
        # For recommendations: always uses Llama2
        # Calls Ollama on port 11434
```

---

## Testing the Integration

### Option 1: Run Comprehensive Test Suite
```bash
cd c:\Users\DELL\Desktop\pathway\tbo-chatbot
python comprehensive_integration_test.py
```

This runs:
- **Phase 1**: Health checks on all 4 services
- **Phase 2**: Individual component tests
- **Phase 3**: Full integration with 4 realistic user profiles
  - Luxury business traveler
  - Family vacation
  - Adventure traveler
  - Corporate retreat
- **Phase 4**: Data quality validation
  - Response structure
  - Profit calculations
  - LLM analysis quality

### Option 2: Manual Testing
```powershell
# Test travel recommendation with realistic profile
curl -X POST http://localhost:8000/recommend/travel-plan `
  -H "Content-Type: application/json" `
  -d '{
    "origin": "New York (JFK)",
    "destination": "Paris, France",
    "check_in": "2026-04-15",
    "check_out": "2026-04-22",
    "passengers": 1,
    "budget": 5000,
    "user_name": "John Traveler",
    "travel_style": "luxury",
    "profit_priority": true
  }' `
  --max-time 120
```

### Option 3: Python Test Script
```python
import requests
import json

response = requests.post(
    "http://localhost:8000/recommend/travel-plan",
    json={
        "origin": "London (LHR)",
        "destination": "Barcelona, Spain",
        "check_in": "2026-07-01",
        "check_out": "2026-07-08",
        "passengers": 4,
        "budget": 3000,
        "travel_style": "budget",
        "profit_priority": False
    },
    timeout=120
)

data = response.json()

# Display top 3 options
for rec in data["all_recommendations"][:3]:
    print(f"\nOption {rec['rank']}: {rec['hotel']['name']}")
    print(f"  Hotel: ${rec['hotel']['price_per_night']}/night")
    print(f"  Flight: {rec['flight']['airline']} ${rec['flight']['price']}")
    print(f"  Total Cost: ${rec['total_cost']:.2f}")
    print(f"  Platform Profit: ${rec['profit_metrics']['total_profit']:.2f}")

# Display best choice
best = data["recommendation"]
print(f"\n✨ BEST CHOICE: {best['hotel']['name']}")
print(f"   Reasoning: {data['reasoning']}")
```

---

## Response Structure

### Complete JSON Response Fields

```json
{
  "status": "success",
  "user_id": "user_123",
  
  "hotel_options": [ ... ],        // All searched hotels (top 5)
  "flight_options": [ ... ],       // All found flights (top 3)
  "travel_packages": [ ... ],      // Vector DB results (top 3)
  
  "all_recommendations": [         // TOP 5 COMBINATIONS
    {
      "rank": 1,                   // Highest profit
      "option_number": 1,
      "hotel": {
        "name": "The Ritz-Carlton Paris",
        "rating": 4.8,
        "price_per_night": 450,
        "location": "Place Vendôme",
        "amenities": [...]
      },
      "flight": {
        "airline": "Air France",
        "price": 450,
        "duration": "8 hours",
        "stops": 0
      },
      "total_cost": 3700,
      "profit_metrics": {
        "base_revenue": 3700,
        "commission": 555,
        "bundle_bonus": 185,
        "total_profit": 740,
        "margin": 20.0
      },
      "suitability_score": 95
    },
    ...  // 4 more options
  ],
  
  "recommendation": {              // BEST CHOICE (LLM Selected)
    "rank": 1,
    "hotel": {...},
    "flight": {...},
    "total_user_cost": 3700,
    "platform_profit": 740
  },
  
  "analysis": "Detailed LLM analysis text...",
  "reasoning": "Why this option was selected...",
  "comparison_summary": "Side-by-side comparison table...",
  
  "profit_metrics": {
    "total_revenue": 3700,
    "platform_profit": 740,
    "profit_margin_percentage": 20.0
  },
  
  "roi_analysis": {
    "total_revenue": 3700,
    "platform_profit": 740,
    "profit_margin": 20.0,
    "customer_satisfaction": "high",
    "roi_percentage": 20.0
  },
  
  "complete_journey": {
    "destination": "Paris, France",
    "duration_days": 7,
    "hotel": "The Ritz-Carlton Paris",
    "flight": "Air France",
    "estimated_total_cost": 3700,
    "itinerary": {
      "day_1": "Arrive at CDG, check in...",
      ...
    }
  }
}
```

---

## Troubleshooting Integration

### Issue: Hotels returning empty
**Cause**: Hotel Search Engine not running or unreachable
**Fix**:
```bash
docker logs hotel-search
docker-compose restart hotel-search
```

### Issue: No travel packages from Qdrant
**Cause**: Collections not populated or empty
**Fix**:
```bash
# Ingest data into Qdrant
python tbo/qdrant_ingest.py
# Check collections
curl http://localhost:6333/collections
```

### Issue: LLM analysis not detailed
**Cause**: Ollama models not loaded
**Fix**:
```bash
# Check available models
curl http://localhost:11434/api/tags

# Manually pull models if needed
ollama pull llama2
ollama pull phi4
```

### Issue: Timeout on recommendation endpoint
**Cause**: LLM is slow on first request
**Fix**: Set timeout to 120+ seconds, first request slower due to model loading

---

## Performance Expectations

| Phase | Component | Duration |
|-------|-----------|----------|
| Hotel Search | Hotel Search Engine | 1-2 seconds |
| Vector Search | Qdrant | 1-2 seconds |
| Package Generation | Orchestrator | <1 second |
| LLM Analysis | Ollama/Llama2 | 3-10 seconds |
| Response Compilation | Orchestrator | <1 second |
| **Total** | **All Services** | **8-20 seconds** |

First request slower (10-30s) due to LLM model initialization.

---

## Success Metrics

✅ **All Components Integrated When**:
1. Orchestrator receives request on port 8000
2. Hotel Search returns hotels on port 5000
3. Qdrant returns packages on port 6333
4. Ollama provides analysis on port 11434
5. Response includes ALL 5 options + best choice
6. LLM reasoning explains selection criteria
7. Profit calculations validated across options

---

## Next Steps for Production

1. **Load test** with parallel requests
2. **Cache responses** in Redis for common queries
3. **Monitor performance** and adjust timeouts
4. **Track conversions** to measure LLM recommendation quality
5. **A/B test** different recommendation algorithms
6. **Fine-tune** LLM prompts based on user feedback

---

**Status**: Full Integration Complete ✅  
**Date**: March 1, 2026  
**All Components Linked and Operational**
