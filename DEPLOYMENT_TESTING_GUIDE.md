# Deployment & Testing Guide - Travel Recommendation Platform

## Status Overview

✅ **All code implemented and ready for deployment**
- Travel Recommendation API: Complete
- Business Rules Engine: Complete  
- Profit Maximization Logic: Complete
- LLM Integration: Complete
- Documentation: Complete
- Examples & Tests: Complete

❌ **Still needs**: Fresh Docker build with fixed dependencies

---

## Prerequisites

1. **Docker & Docker Compose** installed
2. **Windows PowerShell 5.1+** or Command Prompt
3. **Python 3.9+** installed (for standalone testing)
4. **Workspace location**: `c:\Users\DELL\Desktop\pathway\tbo-chatbot`

---

## Step 1: Clean Up Old Containers

```powershell
# Stop and remove all old containers
docker-compose down --remove-orphans

# Clean up dangling containers
docker container prune -f

# Clean up dangling volumes
docker volume prune -f

# Verify cleanup
docker ps -a          # Should show empty list
docker volume ls      # Should show minimal volumes
```

---

## Step 2: Build All Services (Fresh Build)

```powershell
# Navigate to workspace
cd c:\Users\DELL\Desktop\pathway\tbo-chatbot

# Build with fresh dependencies
docker-compose build --no-cache
```

**Expected output:**
```
Building redis... done
Building postgres... done
Building qdrant... done
Building ollama... done
Building hotel-search... done
Building model-init... done
Building orchestrator... done
```

**What this does:**
- Rebuilds all 7 services from scratch
- Installs fresh dependencies (including fixed httpx>=0.27.0)
- Pulls latest service images
- Compiles all Python requirements

---

## Step 3: Start All Services

```powershell
# Start all services in foreground (to see logs)
docker-compose up

# OR start in background
docker-compose up -d
```

**Expected startup sequence:**
```
redis:          container starting...
postgres:       container starting...
qdrant:         container starting...
ollama:         container starting... (this will take longest - downloading models)
hotel-search:   Flask server running on port 5000
model-init:     Python script running
orchestrator:   FastAPI server running on port 8000
```

**Wait times:**
- Redis: 1-2 seconds
- PostgreSQL: 3-5 seconds
- Qdrant: 2-3 seconds
- Ollama (first run): 5-10 minutes (downloading phi4 and llama2 models)
- Hotel Search: 1-2 seconds
- Orchestrator: 2-3 seconds (after ollama ready)

**Verification:**
```powershell
# Check all containers running
docker ps

# Should show 7 containers with "Up" status
```

---

## Step 4: Verify Service Health

### Check Individual Endpoints

```powershell
# Check Orchestrator API (Main service)
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-03-01T12:00:00Z",
  "services": {
    "qdrant": "healthy",
    "ollama": "healthy",
    "hotel_search": "healthy",
    "redis": "healthy"
  }
}
```

```powershell
# Check Hotel Search Engine
curl http://localhost:5000/health

# Expected response: {"status": "ok"}
```

```powershell
# Check Qdrant Vector DB
curl http://localhost:6333/health

# Expected response: {"status": "ok"}
```

```powershell
# Check Ollama LLM
curl http://localhost:11434/api/tags

# Expected response: Models available (phi4, llama2)
```

### Quick Service Check Script

```powershell
# Save as check_services.ps1

$endpoints = @(
    @{name="Orchestrator"; url="http://localhost:8000/health"},
    @{name="Hotel Search"; url="http://localhost:5000/health"},
    @{name="Qdrant"; url="http://localhost:6333/health"}
)

foreach ($endpoint in $endpoints) {
    try {
        $response = curl -s -o /dev/null -w "%{http_code}" $endpoint.url
        if ($response -eq "200") {
            Write-Host "✅ $($endpoint.name): OK" -ForegroundColor Green
        } else {
            Write-Host "⚠️ $($endpoint.name): HTTP $response" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "❌ $($endpoint.name): FAILED" -ForegroundColor Red
    }
}
```

---

## Step 5: Run Integration Tests

```powershell
# Navigate to workspace
cd c:\Users\DELL\Desktop\pathway\tbo-chatbot\orchestrator-agent

# Run the integration test (updated)
python test_integration.py
```

**Expected output:**
```
Testing Orchestrator Agent integration...

✅ Orchestrator API: PASSED
✅ Hotel Search Engine: PASSED
✅ Qdrant Vector DB: PASSED
✅ Ollama LLM: PASSED
✅ Travel Recommendation Endpoint: PASSED
✅ RAG Query Processing: PASSED

Results: 6/6 tests passed ✅
```

**If any fail:**
- Note the failed service
- Check Docker logs: `docker logs <service_name>`
- Verify port is not blocked: `netstat -ano | findstr :<port>`
- Restart service: `docker-compose restart <service_name>`

---

## Step 6: Test Travel Recommendation API

### Option A: Interactive Examples (Recommended)

```powershell
# Navigate to workspace root
cd c:\Users\DELL\Desktop\pathway\tbo-chatbot

# Run interactive example script
python travel_recommendation_examples.py
```

**Interactive menu appears:**
```
=== Travel Recommendation API Examples ===

1. Luxury Business Trip (Paris)
2. Budget Family Vacation (Barcelona)
3. Adventure Travel (Bali)
4. Corporate Retreat (Zurich)
5. Exit

Choose an example (1-5):
```

**Select example 1:**
```
Fetching travel recommendation for Luxury Business Trip...

Request:
{
  "origin": "New York (JFK)",
  "destination": "Paris, France",
  ...
}

Response:
{
  "status": "success",
  "hotel_options": [...],
  "recommendation": {
    "hotel": "Four Seasons Hotel George V",
    "profit_potential": 728.00,
    ...
  }
}
```

### Option B: Manual cURL Test

```powershell
# Create request file: travel_request.json
{
  "origin": "New York (JFK)",
  "destination": "Paris, France",
  "check_in": "2026-04-15",
  "check_out": "2026-04-22",
  "passengers": 1,
  "budget": 5000,
  "travel_style": "luxury",
  "user_id": "user_123",
  "profit_priority": true,
  "business_rules": {
    "markup_percentage": 20,
    "bundle_discount": 5
  }
}

# Make request (30+ second timeout)
curl -X POST http://localhost:8000/recommend/travel-plan `
  -H "Content-Type: application/json" `
  -d @travel_request.json `
  --max-time 60
```

### Option C: Python Script Test

```python
import requests
import json
from datetime import datetime, timedelta

# Create request
request_data = {
    "origin": "New York (JFK)",
    "destination": "Paris, France",
    "check_in": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
    "check_out": (datetime.now() + timedelta(days=52)).strftime("%Y-%m-%d"),
    "passengers": 1,
    "budget": 5000,
    "travel_style": "luxury",
    "profit_priority": True
}

# Send request
response = requests.post(
    "http://localhost:8000/recommend/travel-plan",
    json=request_data,
    timeout=60
)

# Display response
data = response.json()
print(json.dumps(data, indent=2))

# Extract recommendation
if data.get("status") == "success":
    recommendation = data.get("recommendation", {})
    print(f"\n✅ Recommended Hotel: {recommendation.get('hotel', {}).get('name')}")
    print(f"💰 Platform Profit: ${recommendation.get('platform_profit'):.2f}")
    print(f"\n📊 Analysis:")
    print(data.get("analysis", "No analysis provided"))
```

---

## Step 7: Test Different Scenarios

### Scenario 1: Luxury Business (High Profit)

```json
{
  "origin": "London (LHR)",
  "destination": "Paris, France",
  "check_in": "2026-04-15",
  "check_out": "2026-04-22",
  "passengers": 1,
  "budget": 5000,
  "travel_style": "luxury",
  "profit_priority": true
}
```

**Expected**: Premium hotel recommendation with 20%+ profit margin

### Scenario 2: Budget Family (Volume Profit)

```json
{
  "origin": "London (LHR)",
  "destination": "Barcelona, Spain",
  "check_in": "2026-07-01",
  "check_out": "2026-07-08",
  "passengers": 4,
  "budget": 2000,
  "travel_style": "budget",
  "profit_priority": true,
  "business_rules": {
    "group_bonus": 0.08
  }
}
```

**Expected**: Affordable option with group discount bonus

### Scenario 3: Corporate Group (Bundle Profit)

```json
{
  "origin": "London (LHR)",
  "destination": "Zurich, Switzerland",
  "check_in": "2026-06-01",
  "check_out": "2026-06-05",
  "passengers": 10,
  "budget": 15000,
  "travel_style": "business",
  "profit_priority": true,
  "business_rules": {
    "bundle_discount": 0.08,
    "group_bonus": 0.10
  }
}
```

**Expected**: Large bundle with multiple profit layers

---

## Step 8: Performance Benchmarking

### Measure Response Times

```powershell
# Create test script: benchmark_travel_api.ps1

$url = "http://localhost:8000/recommend/travel-plan"

$request = @{
    origin = "New York (JFK)"
    destination = "Paris, France"
    check_in = "2026-04-15"
    check_out = "2026-04-22"
    passengers = 1
    budget = 5000
    travel_style = "luxury"
    profit_priority = $true
} | ConvertTo-Json

# Run 5 requests and measure times
$times = @()
for ($i = 1; $i -le 5; $i++) {
    Write-Host "Request $i..."
    $start = Get-Date
    $response = curl -s -X POST $url `
        -H "Content-Type: application/json" `
        -d $request
    $end = Get-Date
    
    $time = ($end - $start).TotalSeconds
    $times += $time
    Write-Host "  Time: ${time}s"
}

# Calculate statistics
$avg = ($times | Measure-Object -Average).Average
$min = ($times | Measure-Object -Minimum).Minimum
$max = ($times | Measure-Object -Maximum).Maximum

Write-Host "`nBenchmark Results:"
Write-Host "  Average: $($avg.ToString('0.00'))s"
Write-Host "  Min: $($min.ToString('0.00'))s"
Write-Host "  Max: $($max.ToString('0.00'))s"
```

**Run it:**
```powershell
. .\benchmark_travel_api.ps1
```

**Expected results:**
```
Benchmark Results:
  Average: 12.34s
  Min: 10.23s
  Max: 15.67s
```

---

## Step 9: Monitor Logs

### Watch Real-Time Logs

```powershell
# Watch Orchestrator logs
docker logs -f <container_id_orchestrator>

# Watch Hotel Search logs
docker logs -f <container_id_hotel_search>

# Watch Ollama logs (for LLM activity)
docker logs -f <container_id_ollama>

# Get container IDs
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```

### Search Logs

```powershell
# Find errors in orchestrator logs
docker logs <container_id> 2>&1 | findstr /i "error exception traceback"

# Find recommendation API calls
docker logs <container_id> 2>&1 | findstr "recommend/travel-plan"
```

---

## Step 10: Troubleshooting

### Issue: "Connection refused" on port 8000

**Cause**: Orchestrator not started or crashed

**Solution**:
```powershell
# Check orchestrator logs
docker logs <orchestrator_container_id>

# Restart it
docker-compose restart orchestrator

# Or rebuild
docker-compose up --build orchestrator
```

### Issue: "Timeout" on /recommend/travel-plan

**Cause**: Ollama still downloading models or LLM is slow

**Solution**:
```powershell
# Check ollama logs
docker logs <ollama_container_id>

# Verify model is loaded
curl http://localhost:11434/api/tags

# Wait 5-10 minutes for first model download, then retry
```

### Issue: "Hotel search unavailable"

**Cause**: Hotel search service crashed or port blocked

**Solution**:
```powershell
# Check hotel search logs
docker logs <hotel_search_container_id>

# Restart it
docker-compose restart hotel-search

# Check port availability
netstat -ano | findstr :5000
```

### Issue: "Qdrant connection failed"

**Cause**: Vector DB not responding

**Solution**:
```powershell
# Verify qdrant running
docker ps | findstr qdrant

# Check qdrant health
curl http://localhost:6333/health

# Restart if needed
docker-compose restart qdrant
```

---

## Complete Deployment Checklist

```
Pre-Deployment
☐ Docker and Docker Compose installed
☐ Workspace at c:\Users\DELL\Desktop\pathway\tbo-chatbot
☐ All code files present and correct
☐ No old containers running

Deployment Steps
☐ Step 1: Clean up old containers
☐ Step 2: Fresh build with --no-cache
☐ Step 3: Start all services
☐ Step 4: Verify service health (all 7 services up)
☐ Step 5: Run integration tests (6/6 passing)
☐ Step 6: Test travel recommendation API

Testing & Validation
☐ Run interactive examples (all 4 scenarios work)
☐ Manual cURL test (successful response)
☐ Python test script (returns valid JSON)
☐ Profit calculations verified
☐ LLM analysis present and reasonable
☐ Performance acceptable (10-30 seconds)

Monitoring
☐ Logs accessible and clean
☐ No error messages in logs
☐ Services stable for 5+ minutes
☐ No container restarts happening

Production Ready
☐ All health checks passing
☐ All tests passing
☐ Performance acceptable
☐ Documentation clear
☐ Examples working
```

---

## Next Steps After Successful Deployment

1. **Load Testing**: Test with concurrent requests
2. **Response Caching**: Implement Redis caching for common queries
3. **Analytics**: Track booking conversion rates
4. **Model Optimization**: Fine-tune LLM prompts based on real requests
5. **Feature Additions**: Add multi-destination planning, payment plans, etc.

---

## Contact & Support

**If issues persist:**
1. Check logs: `docker logs <service_name>`
2. Check connections: `curl http://localhost:<port>/health`
3. Verify dependencies: Review requirements.txt
4. Check docker-compose.yml for configuration issues
5. Review conversation summary for context

**Documentation references:**
- `TRAVEL_RECOMMENDATION_SUMMARY.md` - Feature overview
- `IMPLEMENTATION_CODE_REFERENCE.md` - Code details
- `TRAVEL_RECOMMENDATION_API.md` - API specification
- `travel_recommendation_examples.py` - Working code examples

---

**Status**: Ready for Deployment ✅  
**Version**: 1.0.0  
**Last Updated**: March 1, 2026
