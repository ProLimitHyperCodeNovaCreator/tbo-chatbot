#!/usr/bin/env python3
"""
QUICK START GUIDE - Travel Recommendation Platform
Complete setup and testing in 5 easy steps
"""

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: CLEAN UP & REBUILD
# ═══════════════════════════════════════════════════════════════════════════

print("""
═══════════════════════════════════════════════════════════════════════════
STEP 1: Clean Up & Fresh Build
═══════════════════════════════════════════════════════════════════════════

Run these commands in PowerShell:

cd c:\\Users\\DELL\\Desktop\\pathway\\tbo-chatbot

# Clean all old containers and volumes
docker-compose down --remove-orphans
docker container prune -f
docker volume prune -f

# Fresh build (takes 3-5 minutes first time)
docker-compose build --no-cache

Expected: All services rebuilt successfully
""")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: START ALL SERVICES
# ═══════════════════════════════════════════════════════════════════════════

print("""
═══════════════════════════════════════════════════════════════════════════
STEP 2: Start All 7 Services
═══════════════════════════════════════════════════════════════════════════

In NEW PowerShell terminal, run:

cd c:\\Users\\DELL\\Desktop\\pathway\\tbo-chatbot
docker-compose up

Expected output sequence:
  ✓ redis starting...
  ✓ postgres starting...
  ✓ qdrant starting...
  ✓ ollama starting... (takes 5-10 minutes on first run - downloading models)
  ✓ hotel-search starting on port 5000
  ✓ model-init running initialization
  ✓ orchestrator starting on port 8000

Wait until you see "orchestrator | Application startup complete"
Then proceed to STEP 3
""")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: VERIFY ALL SERVICES ARE HEALTHY
# ═══════════════════════════════════════════════════════════════════════════

print("""
═══════════════════════════════════════════════════════════════════════════
STEP 3: Verify All Services Are Running
═══════════════════════════════════════════════════════════════════════════

In a NEW PowerShell terminal, check each service:

# Check Orchestrator (should show healthy status)
curl http://localhost:8000/health

Expected: {"status":"healthy","service":"orchestrator-agent",...}

# Check Hotel Search (should show ok status)
curl http://localhost:5000/health

Expected: {"status":"healthy","service":"Hotel Search Engine",...}

# Check Qdrant (should show ok status)
curl http://localhost:6333/health

Expected: {"status":"ok"}

# Check Ollama (should list available models)
curl http://localhost:11434/api/tags

Expected: {"models":[{"name":"llama2:latest"},{"name":"phi4:latest"},...]}

All should return 200 OK. If any fail, check docker logs:
  docker logs orchestrator
  docker logs hotel-search
  docker logs qdrant
  docker logs ollama

Then proceed to STEP 4
""")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: RUN COMPREHENSIVE TEST SUITE
# ═══════════════════════════════════════════════════════════════════════════

print("""
═══════════════════════════════════════════════════════════════════════════
STEP 4: Run Comprehensive Integration Tests
═══════════════════════════════════════════════════════════════════════════

In a NEW PowerShell terminal:

cd c:\\Users\\DELL\\Desktop\\pathway\\tbo-chatbot
python comprehensive_integration_test.py

This tests:
  ✓ Phase 1: All 4 services health checks
  ✓ Phase 2: Individual component functionality
  ✓ Phase 3: Full integration with 4 realistic user profiles
    - Luxury business traveler (Paris, $8000)
    - Family vacation (Barcelona, $3000, 4 passengers)
    - Adventure traveler (Bali, $4000, 2 passengers)
    - Corporate retreat (Zurich, $18000, 12 passengers)
  ✓ Phase 4: Data quality validation

Expected: 15-20 tests PASSING
  ✓ All health checks pass
  ✓ Hotel search returns hotels
  ✓ Travel recommendations work
  ✓ Multiple options generated
  ✓ LLM analysis provided
  ✓ Profit calculations valid

If any fail, review the error messages and check docker logs

Then proceed to STEP 5
""")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: TEST YOUR OWN PROFILE
# ═══════════════════════════════════════════════════════════════════════════

print("""
═══════════════════════════════════════════════════════════════════════════
STEP 5A: Interactive Testing - Run Example Script
═══════════════════════════════════════════════════════════════════════════

In the SAME PowerShell terminal (or new one), run:

cd c:\\Users\\DELL\\Desktop\\pathway\\tbo-chatbot
python -c "
import requests
import json
from datetime import datetime, timedelta

# Create your custom request
request_data = {
    'origin': 'New York (JFK)',
    'destination': 'Paris, France',
    'check_in': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'),
    'check_out': (datetime.now() + timedelta(days=37)).strftime('%Y-%m-%d'),
    'passengers': 1,
    'budget': 5000,
    'user_name': 'Your Name',
    'travel_style': 'luxury',
    'user_preferences': {
        'hotel_rating_min': 4.5,
        'amenities': ['spa', 'fine dining']
    },
    'profit_priority': True
}

print('\\nSending travel recommendation request...')
response = requests.post(
    'http://localhost:8000/recommend/travel-plan',
    json=request_data,
    timeout=120
)

data = response.json()

print('\\n📊 TOP 5 RECOMMENDED PACKAGES:')
print('=' * 80)

for rec in data['all_recommendations'][:5]:
    print(f\"\\nRank {rec['rank']}: {rec['hotel']['name']}\")
    print(f\"  Hotel: {rec['hotel']['location']} | Rating: {rec['hotel']['rating']}/5\")
    print(f\"  Price: \\${rec['hotel']['price_per_night']}/night\")
    print(f\"  Flight: {rec['flight']['airline']} (\\${rec['flight']['price']})\")
    print(f\"  Total Cost: \\${rec['total_cost']:.2f}\")
    print(f\"  Platform Profit: \\${rec['profit_metrics']['total_profit']:.2f} ({rec['profit_metrics']['margin']:.1f}%)\")

print('\\n' + '=' * 80)
best = data['recommendation']
print(f\"\\n✨ BEST CHOICE (Selected by LLM): {best['hotel']['name']}\")
print(f\"\\nREASONING:\\n{data['reasoning']}\")
print(f\"\\n📊 PROFIT ANALYSIS:\\n{data['comparison_summary']}\")
"

Expected:
  - 5 ranked options displayed
  - Best choice highlighted with LLM reasoning
  - Profit metrics shown for each
  - Journey itinerary available
  - Total execution time: 10-30 seconds

═══════════════════════════════════════════════════════════════════════════
STEP 5B: Manual cURL Test
═══════════════════════════════════════════════════════════════════════════

Or use cURL directly:

$body = @{
    origin = 'London (LHR)'
    destination = 'Barcelona, Spain'
    check_in = '2026-07-01'
    check_out = '2026-07-08'
    passengers = 4
    budget = 3000
    travel_style = 'budget'
    user_name = 'Sarah Family'
} | ConvertTo-Json

curl -X POST http://localhost:8000/recommend/travel-plan `
  -H 'Content-Type: application/json' `
  -d $body `
  --max-time 120

Expected: JSON response with all_recommendations and best choice

═══════════════════════════════════════════════════════════════════════════
STEP 5C: Python Script Test
═══════════════════════════════════════════════════════════════════════════

Create file test_recommendation.py:

import requests
import json

# Your custom profile
profile = {
    'origin': 'Singapore (SIN)',
    'destination': 'Bali, Indonesia',
    'check_in': '2026-05-01',
    'check_out': '2026-05-15',
    'passengers': 2,
    'budget': 4000,
    'travel_style': 'adventure',
    'user_preferences': {
        'amenities': ['yoga', 'surfing', 'wellness']
    }
}

# Send request
response = requests.post(
    'http://localhost:8000/recommend/travel-plan',
    json=profile,
    timeout=120
)

data = response.json()

# Print results
print(f"Status: {data['status']}")
print(f"\\nOptions Analyzed: {len(data['all_recommendations'])}")
print(f"\\nBest Option: {data['recommendation']['hotel']['name']}")
print(f"Total Cost: \\${data['recommendation']['total_user_cost']:.2f}")
print(f"Platform Profit: \\${data['recommendation']['platform_profit']:.2f}")
print(f\"\\nAnalysis:\\n{data['analysis']}\")

Run with: python test_recommendation.py
""")

# ═══════════════════════════════════════════════════════════════════════════
# ADDITIONAL INFORMATION
# ═══════════════════════════════════════════════════════════════════════════

print("""
═══════════════════════════════════════════════════════════════════════════
ADDITIONAL COMMANDS & TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════

View Live Logs:
──────────────────────────────────────────────────────────────────────────
docker logs -f orchestrator           # Main service logs
docker logs -f hotel-search          # Hotel search logs
docker logs -f ollama                # LLM service logs
docker logs -f qdrant                # Vector DB logs

Monitor Services:
──────────────────────────────────────────────────────────────────────────
docker ps                             # Show all running containers
docker stats                          # Show CPU/memory usage

Stop All Services:
──────────────────────────────────────────────────────────────────────────
docker-compose down                   # Clean shutdown
docker-compose down -v                # Remove volumes too

Check Service Health:
──────────────────────────────────────────────────────────────────────────
# All services at once
curl http://localhost:8000/health &
curl http://localhost:5000/health &
curl http://localhost:6333/health

Access Service Logs:
──────────────────────────────────────────────────────────────────────────
# Show last 50 lines
docker logs --tail 50 orchestrator

# Show real-time logs
docker logs -f orchestrator

Common Issues:
──────────────────────────────────────────────────────────────────────────

1. "Connection refused on port 8000"
   → Orchestrator not running: docker-compose restart orchestrator
   → Check logs: docker logs orchestrator

2. "Timeout on recommendation endpoint"
   → First time Ollama is loading models (5-10 minutes)
   → Wait and retry, or check: docker logs ollama

3. "Hotels not found"
   → Hotel Search Engine down: docker-compose restart hotel-search
   → Check: curl http://localhost:5000/health

4. "No travel packages"
   → Qdrant not populated yet
   → Run: python tbo/qdrant_ingest.py
   → Or just use synthetic data (works fine)

5. "LLM analysis is empty"
   → Ollama not ready: docker logs ollama
   → Models not loaded: curl http://localhost:11434/api/tags
   → Wait 10 minutes for first-time model loading

═══════════════════════════════════════════════════════════════════════════
REQUEST TIMEOUT SETTINGS
═══════════════════════════════════════════════════════════════════════════

First Request:  120+ seconds (Ollama loading models)
Subsequent:     20-30 seconds (normal)

Always use --max-time 120 or timeout=120 in requests

═══════════════════════════════════════════════════════════════════════════
EXPECTED RESPONSE STRUCTURE
═══════════════════════════════════════════════════════════════════════════

{
  "status": "success",
  "all_recommendations": [          # 5 options ranked by profit
    {
      "rank": 1,                     # #1 best option
      "hotel": {...},                # Hotel details
      "flight": {...},               # Flight details
      "total_cost": 3700,            # Price to customer
      "profit_metrics": {...}        # Our profit
    },
    ...  # 4 more options
  ],
  
  "recommendation": {...},           # Best choice (LLM selected)
  "analysis": "...",                 # LLM analysis text
  "reasoning": "...",                # Why best was chosen
  "comparison_summary": "...",       # Comparison table
  "profit_metrics": {...},
  "roi_analysis": {...},
  "complete_journey": {...}
}

Key Fields:
  - all_recommendations: Top 5 combinations with all details
  - recommendation: Single best choice (LLM selected)
  - analysis: Detailed LLM reasoning
  - comparison_summary: Table comparing all options
  - profit_metrics: Revenue and margins

═══════════════════════════════════════════════════════════════════════════
DOCUMENTATION FILES
═══════════════════════════════════════════════════════════════════════════

COMPLETE_INTEGRATION_GUIDE.md       # Full integration details & architecture
comprehensive_integration_test.py   # Complete test suite with 4 profiles
DEPLOYMENT_TESTING_GUIDE.md        # Step-by-step deployment
TRAVEL_RECOMMENDATION_SUMMARY.md    # Feature overview
IMPLEMENTATION_CODE_REFERENCE.md   # Code implementation details

═══════════════════════════════════════════════════════════════════════════
YOU ARE ALL SET! 
═══════════════════════════════════════════════════════════════════════════

The system is fully integrated with:
  ✅ Orchestrator Agent (port 8000) - Central hub
  ✅ Hotel Search Engine (port 5000) - Real-time hotels
  ✅ Qdrant Vector DB (port 6333) - Travel packages & semantic search
  ✅ Ollama LLM (port 11434) - Intelligent analysis
  ✅ Multi-option recommendations - 5 options analyzed
  ✅ LLM-based selection - Best choice highlighted
  ✅ Profit maximization - Commission calculations
  ✅ Comprehensive testing - Realistic user profiles

NEXT STEPS:
1. Run comprehensive_integration_test.py to validate everything
2. Test with your own custom profiles
3. Monitor logs and performance
4. Integrate with your frontend

Happy traveling! 🚀✨
===============================================================================
""")

print("\n🎉 Ready to go! Follow the steps above to get everything running.\n")
