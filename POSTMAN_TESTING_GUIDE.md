📌 POSTMAN TESTING GUIDE - Travel Recommendation API
==================================================

This guide shows you how to test the integrated travel recommendation endpoint using Postman.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUICK START (2 MINUTES)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. OPEN POSTMAN
   - Download from: https://www.postman.com/downloads/
   - Or open it if already installed

2. CREATE NEW REQUEST
   - Click: "+ New" > "HTTP"
   - Method: POST
   - URL: http://localhost:8000/recommend/travel-plan

3. SET UP HEADERS (Tab: "Headers")
   - Key: Content-Type
   - Value: application/json

4. ADD REQUEST BODY (Tab: "Body" > select "raw" > JSON)
   - Copy-paste one of the examples below
   - Click: "Send"

5. VIEW RESPONSE
   - See the 5 recommended packages with LLM analysis
   - Response time: ~4-5 minutes on first run

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLE 1: LUXURY BUSINESS TRAVEL (Paris)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Request URL: POST http://localhost:8000/recommend/travel-plan

Headers:
  Content-Type: application/json

Body (Raw JSON):
```json
{
  "origin": "New York (JFK)",
  "destination": "Paris, France",
  "check_in": "2026-03-15",
  "check_out": "2026-03-22",
  "passengers": 2,
  "budget": 8000,
  "user_preferences": {
    "hotel_rating": 5,
    "amenities": ["WiFi", "Gym", "Restaurant", "Spa"],
    "travel_style": "Luxury Business",
    "preferences": "Premium accommodation near Champs-Élysées, flexible cancellation"
  },
  "business_rules": {
    "profit_margin_target": 0.25,
    "include_upsells": true,
    "prefer_partner_hotels": true
  }
}
```

Expected Response Time: 4-5 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLE 2: FAMILY BUDGET TRAVEL (Barcelona)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Request URL: POST http://localhost:8000/recommend/travel-plan

Headers:
  Content-Type: application/json

Body (Raw JSON):
```json
{
  "origin": "London (LHR)",
  "destination": "Barcelona, Spain",
  "check_in": "2026-04-10",
  "check_out": "2026-04-17",
  "passengers": 4,
  "budget": 3000,
  "user_preferences": {
    "hotel_rating": 3.5,
    "amenities": ["WiFi", "Pool", "Family-friendly"],
    "travel_style": "Family Budget",
    "preferences": "Near beach, kid-friendly attractions, affordable dining options"
  },
  "business_rules": {
    "profit_margin_target": 0.20,
    "include_upsells": false,
    "prefer_partner_hotels": false
  }
}
```

Expected Response Time: 4-5 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLE 3: ADVENTURE TRAVEL (Bali)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Request URL: POST http://localhost:8000/recommend/travel-plan

Headers:
  Content-Type: application/json

Body (Raw JSON):
```json
{
  "origin": "Singapore (SIN)",
  "destination": "Bali, Indonesia",
  "check_in": "2026-05-01",
  "check_out": "2026-05-08",
  "passengers": 2,
  "budget": 4000,
  "user_preferences": {
    "hotel_rating": 4,
    "amenities": ["WiFi", "Yoga", "Water Sports", "Beach Access"],
    "travel_style": "Adventure",
    "preferences": "Beach resort, water activities, yoga classes, natural attractions"
  },
  "business_rules": {
    "profit_margin_target": 0.22,
    "include_upsells": true,
    "prefer_partner_hotels": true
  }
}
```

Expected Response Time: 4-5 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EXAMPLE 4: CORPORATE GROUP TRAVEL (Zurich)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Request URL: POST http://localhost:8000/recommend/travel-plan

Headers:
  Content-Type: application/json

Body (Raw JSON):
```json
{
  "origin": "Berlin (BER)",
  "destination": "Zurich, Switzerland",
  "check_in": "2026-06-15",
  "check_out": "2026-06-18",
  "passengers": 10,
  "budget": 18000,
  "user_preferences": {
    "hotel_rating": 4.5,
    "amenities": ["WiFi", "Conference Rooms", "Business Center", "Restaurant"],
    "travel_style": "Corporate Retreat",
    "preferences": "Central location, meeting facilities, team building activities"
  },
  "business_rules": {
    "profit_margin_target": 0.25,
    "include_upsells": true,
    "prefer_partner_hotels": true
  }
}
```

Expected Response Time: 4-5 minutes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UNDERSTANDING THE RESPONSE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The response includes:

1. "recommendation" - The BEST package selected by LLM
   {
     "hotel_name": "Hotel Name",
     "hotel_rating": 4.5,
     "hotel_amenities": ["WiFi", "Gym", ...],
     "flight_info": {
       "airline": "Airline Name",
       "departure": "2026-03-15 08:00",
       "arrival": "2026-03-15 20:00"
     },
     "total_cost": 2840.00,
     "profit": 710.00,
     "rank": 1
   }

2. "all_recommendations" - Array of 5 options (ranked by profit)
   - Option 1: Highest profit combination
   - Option 2: Balance of price and amenities
   - Option 3: Best value
   - Option 4: Luxury with good availability
   - Option 5: Budget alternative

3. "analysis" - LLM's detailed reasoning
   Includes:
   - WHY this was selected
   - Customer preference alignment
   - Profit optimization
   - Upsell recommendations
   - Risk analysis

4. "comparison_summary" - Side-by-side table of all 5 options
   Shows:
   - Hotel names
   - Flight details
   - Prices
   - Profit margins
   - Amenities match

5. "status" - "success" or error message

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAVE & REUSE (COLLECTION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To save these requests for later:

1. In Postman, click: "+ New" > "Collection"
   Name: "Travel Recommendation Tests"

2. Within collection, create requests:
   - Right-click collection > "Add Request"
   - Copy request details from examples above
   - Add as: "Luxury Paris", "Family Barcelona", etc.

3. Reuse by opening saved request and clicking "Send"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TESTING HINTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Check Postman Settings:
  - Postman > Settings > Response timeout
  - Set to: 600 seconds or higher

✓ Monitor Progress:
  - Open browser to: http://localhost:8000/health
  - Should return: {"status": "healthy", ...}

✓ If service not available:
  - Ensure Docker containers running: docker ps
  - Check logs: docker logs tbo-orchestrator (last 50 lines)
  - Restart if needed: docker restart tbo-orchestrator

✓ Dates:
  - Must be in format: YYYY-MM-DD
  - Must be at least 14 days in future
  - Example: 2026-03-15 is 14 days from now (March 1, 2026)

✓ Budget:
  - Should be realistic for destination
  - Paris luxury: $8000+ for 2 people, 7 days
  - Barcelona budget: $2000-4000 for 4 people, 7 days
  - Bali adventure: $3000-5000 for 2 people, 7 days

✓ Passengers:
  - 1-20 recommended
  - Each adds to total cost

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API ENDPOINTS SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Health Check:
  GET http://localhost:8000/health
  Response: {"status": "healthy", "service": "orchestrator-agent", "version": "1.0.0"}

Travel Recommendation:
  POST http://localhost:8000/recommend/travel-plan
  Body: TravelRecommendationRequest (see examples above)
  Response: TravelRecommendationResponse with 5 options + LLM analysis

Hotel Search (if needed separately):
  POST http://localhost:5000/search
  Body: {"query": "luxury hotel in Paris", "num_results": 5}

Qdrant Vector DB (if needed separately):
  GET http://localhost:6333/readyz
  Web UI: http://localhost:6333/dashboard

Ollama LLM (if needed separately):
  GET http://localhost:11434/api/tags
  List all available models

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ "Connection refused" (http://localhost:8000)
   → Docker containers not running
   → Solution: docker-compose up -d
   → Wait 30 seconds for Orchestrator to start

❌ "Request timeout (600s)"
   → Increase Postman timeout in Settings
   → Or wait for LLM model warmup (first request ~5 mins)

❌ "Invalid date format"
   → Dates must be: YYYY-MM-DD
   → Example: 2026-03-15 (March 15, 2026)

❌ "Budget too low"
   → Increase budget in request
   → System needs to cover hotel + flight + profit margin

❌ "No hotels found"
   → Check destination city name spelling
   → Try common cities: Paris, Barcelona, Bali, Zurich, New York

❌ "Model not found" (Ollama)
   → Models take time to initialize
   → Wait 2 minutes and retry
   → Or check: GET http://localhost:11434/api/tags

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Try EXAMPLE 1 (Luxury Paris) first - most data available
2. Test with your own travel scenarios
3. Monitor response times and LLM analysis quality
4. Adjust prompts/preferences based on results
5. Integrate with your application

Good luck! 🚀
