# API Quick Reference - cURL Examples

## Prerequisites
- Services running on `localhost`
- Orchestrator on port 8000
- Hotel Search on port 5000

## Health Check
```bash
curl http://localhost:8000/health
```

## 1. Simple JSON Hotel Query

**Search for hotels in Barcelona:**
```bash
curl -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d '{
    "query_type": "hotel",
    "location": "Barcelona, Spain",
    "check_in": "2026-03-20",
    "check_out": "2026-03-25",
    "guests": 2,
    "preferences": {
      "min_rating": 4.0,
      "max_price": 250
    },
    "use_rag": true
  }'
```

**Save to file:**
```bash
curl -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d @request.json > response.json
```

## 2. RAG-Enhanced Query

**Travel package with complex preferences:**
```bash
curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{
    "query_type": "travel_package",
    "destination": "Santorini, Greece",
    "departure_date": "2026-04-01",
    "return_date": "2026-04-08",
    "passengers": 2,
    "preferences": {
      "budget": "luxury",
      "interests": ["beaches", "culture", "dining"]
    },
    "use_rag": true
  }'
```

## 3. Natural Language Query

**Conversational query:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Find me a 5-star hotel in Rome for 3 nights starting March 15, preferably near the Colosseum",
    "user_id": "user123",
    "context": {
      "location": "Rome",
      "check_in": "2026-03-15",
      "check_out": "2026-03-18",
      "guests": 2,
      "preferences": {
        "landmark": "Colosseum"
      }
    }
  }'
```

## 4. Flight Search

**Book flights with preferences:**
```bash
curl -X POST http://localhost:8000/search/flights \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "ATH",
    "destination": "BCN",
    "departure_date": "2026-03-20",
    "return_date": "2026-03-25",
    "passengers": 2,
    "user_id": "user123",
    "preferences": {
      "max_price": 500,
      "preferred_airline": "Air France"
    }
  }'
```

## 5. Hotel Search

**Direct hotel search:**
```bash
curl -X POST http://localhost:8000/search/hotels \
  -H "Content-Type: application/json" \
  -d '{
    "location": "Paris, France",
    "check_in": "2026-03-10",
    "check_out": "2026-03-15",
    "guests": 2,
    "user_id": "user123",
    "preferences": {
      "min_rating": 4.5,
      "max_price": 300,
      "amenities": ["pool", "gym", "wifi"]
    }
  }'
```

## 6. Complete Travel Package

**Book entire trip (flights + hotels):**
```bash
curl -X POST http://localhost:8000/search/packages \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "JFK",
    "destination": "LHR",
    "departure_date": "2026-04-01",
    "return_date": "2026-04-08",
    "passengers": 3,
    "user_id": "user456"
  }'
```

## 7. Full Orchestration

**Complex multi-step booking:**
```bash
curl -X POST http://localhost:8000/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I need a complete travel package: flights from Athens to Barcelona, 5 nights, for 2 people. Prefer luxury hotels and direct flights.",
    "user_id": "user789",
    "context": {
      "origin": "ATH",
      "destination": "BCN",
      "location": "Barcelona",
      "departure_date": "2026-03-20",
      "return_date": "2026-03-25",
      "check_in": "2026-03-20",
      "check_out": "2026-03-25",
      "passengers": 2,
      "guests": 2,
      "preferences": {
        "hotel_type": "luxury",
        "flight_type": "direct"
      }
    }
  }'
```

## 8. Advanced: Multiple Cities

**Multi-city travel package:**
```bash
curl -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d '{
    "query_type": "travel_package",
    "destination": "Greece",
    "departure_date": "2026-05-01",
    "return_date": "2026-05-15",
    "passengers": 4,
    "preferences": {
      "cities": ["Athens", "Mykonos", "Santorini"],
      "budget_per_night": 200,
      "activities": ["hiking", "beaches", "nightlife"]
    },
    "use_rag": true
  }'
```

## 9. Personalized Recommendations

**Query with personalization:**
```bash
curl -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d '{
    "query_type": "hotel",
    "location": "Miami, USA",
    "check_in": "2026-06-01",
    "check_out": "2026-06-08",
    "guests": 2,
    "user_id": "vip_user_001",
    "preferences": {
      "min_rating": 4.8,
      "budget": "luxury",
      "amenities": ["beach", "spa", "fine dining"],
      "special_requests": ["ocean view", "high floor", "anniversary package"]
    }
  }'
```

## Testing with PowerShell (Windows)

**Simple test:**
```powershell
$body = @{
    query_type = "hotel"
    location = "Barcelona"
    check_in = "2026-03-20"
    check_out = "2026-03-25"
    guests = 2
    use_rag = $true
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/json/process" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $body | Select-Object -ExpandProperty Content
```

## Testing with Python

**Simple script:**
```python
import requests
import json

url = "http://localhost:8000/json/process"
payload = {
    "query_type": "hotel",
    "location": "Barcelona, Spain",
    "check_in": "2026-03-20",
    "check_out": "2026-03-25",
    "guests": 2,
    "use_rag": True
}

response = requests.post(url, json=payload, timeout=30)
print(json.dumps(response.json(), indent=2))
```

## Response Format

All endpoints return structured JSON:

```json
{
  "status": "success",
  "query_type": "hotel",
  "sources": ["hotel_search_engine", "qdrant_vectordb"],
  "hotel_results": [
    {
      "name": "Hotel Name",
      "rating": 4.5,
      "price_per_night": 150,
      "location": "City Center"
    }
  ],
  "travel_packages": [],
  "llm_analysis": "Detailed analysis and recommendations...",
  "recommendations": [],
  "total_results": {
    "hotels": 5,
    "travel_packages": 0
  }
}
```

## Error Responses

**400 Bad Request - Missing fields:**
```json
{
  "detail": "Missing required field: location"
}
```

**500 Server Error - Service unavailable:**
```json
{
  "detail": "Hotel Search Service unavailable: Connection refused"
}
```

## Performance Tips

1. **Minimize context** - Include only necessary fields
2. **Use specific locations** - "Paris, France" vs "Paris"
3. **Set realistic dates** - Use future dates only
4. **Batch requests** - Don't spam the API
5. **Cache results** - Store responses locally
6. **Monitor response time** - Track API performance

## Example Request Files

**create request.json:**
```json
{
  "query_type": "hotel",
  "location": "Barcelona, Spain",
  "check_in": "2026-03-20",
  "check_out": "2026-03-25",
  "guests": 2,
  "preferences": {
    "min_rating": 4.0,
    "max_price": 250
  },
  "use_rag": true
}
```

**Run with curl:**
```bash
curl -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d @request.json
```

## Debugging Tips

**Pretty print response:**
```bash
curl -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d '{"query_type":"hotel","location":"Barcelona","check_in":"2026-03-20","check_out":"2026-03-25","guests":2}' | python -m json.tool
```

**Check response headers:**
```bash
curl -i http://localhost:8000/health
```

**Save response with headers:**
```bash
curl -i -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d @request.json > response.txt
```

**Measure response time:**
```bash
curl -w "\nTotal time: %{time_total}s\n" \
  -X POST http://localhost:8000/json/process \
  -H "Content-Type: application/json" \
  -d '{"query_type":"hotel","location":"Barcelona","check_in":"2026-03-20","check_out":"2026-03-25","guests":2}'
```

---

**Last Updated**: March 1, 2026
