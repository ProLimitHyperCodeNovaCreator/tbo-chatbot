# Travel Recommendation API - cURL Examples

## 1. Simple Travel Recommendation Request

```bash
curl -X POST http://localhost:8000/recommend/travel-plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "New York (JFK)",
    "destination": "Paris, France",
    "check_in": "2026-04-15",
    "check_out": "2026-04-22",
    "passengers": 1,
    "budget": 5000,
    "user_id": "user_123",
    "travel_style": "luxury",
    "profit_priority": true
  }'
```

## 2. Family Vacation with Budget Constraints

```bash
curl -X POST http://localhost:8000/recommend/travel-plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "London (LHR)",
    "destination": "Barcelona, Spain",
    "check_in": "2026-07-01",
    "check_out": "2026-07-08",
    "passengers": 4,
    "budget": 2000,
    "user_name": "Sarah Family",
    "travel_style": "budget",
    "user_preferences": {
      "hotel_rating_min": 3.5,
      "amenities": ["pool", "family rooms", "breakfast included"],
      "location": "Near beach"
    },
    "special_requirements": "Children aged 5 and 8, interconnected rooms needed"
  }'
```

## 3. Adventure Travel with Custom Business Rules

```bash
curl -X POST http://localhost:8000/recommend/travel-plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Singapore (SIN)",
    "destination": "Bali, Indonesia",
    "check_in": "2026-05-10",
    "check_out": "2026-05-17",
    "passengers": 2,
    "budget": 3000,
    "travel_style": "adventure",
    "user_preferences": {
      "amenities": ["gym", "wifi", "adventure planning"]
    },
    "business_rules": {
      "markup_percentage": 18,
      "bundle_discount": 8,
      "preferred_partners": ["Local boutique hotels"]
    },
    "profit_priority": true
  }'
```

## 4. Corporate Retreat (Large Group)

```bash
curl -X POST http://localhost:8000/recommend/travel-plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "London (LHR)",
    "destination": "Zurich, Switzerland",
    "check_in": "2026-06-01",
    "check_out": "2026-06-05",
    "passengers": 10,
    "budget": 15000,
    "user_name": "TechCorp Inc",
    "travel_style": "business",
    "user_preferences": {
      "hotel_rating_min": 4.5,
      "amenities": ["conference rooms", "team activities"]
    },
    "special_requirements": "10 rooms, conference facilities, team building",
    "business_rules": {
      "markup_percentage": 22,
      "group_bonus": 0.08,
      "loyalty_multiplier": 1.5
    }
  }'
```

## 5. Luxury Honeymoon Package

```bash
curl -X POST http://localhost:8000/recommend/travel-plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "New York (JFK)",
    "destination": "Maldives",
    "check_in": "2026-08-15",
    "check_out": "2026-08-22",
    "passengers": 2,
    "budget": 8000,
    "user_name": "Mr & Mrs Johnson",
    "travel_style": "luxury",
    "user_preferences": {
      "hotel_rating_min": 5,
      "amenities": ["over-water bungalow", "spa", "private beach"],
      "location": "Exclusive resort area"
    },
    "special_requirements": "Honeymoon suite, romantic dinner setup, flower decorations",
    "profit_priority": true,
    "business_rules": {
      "markup_percentage": 25,
      "luxury_premium": 0.20
    }
  }'
```

## 6. Mid-Range Business Trip with Loyalty

```bash
curl -X POST http://localhost:8000/recommend/travel-plan \
  -H "Content-Type: application/json" \
  -d '{
    "origin": "Boston (BOS)",
    "destination": "San Francisco (SFO)",
    "check_in": "2026-03-20",
    "check_out": "2026-03-23",
    "passengers": 1,
    "budget": 1500,
    "user_id": "loyalty_user_456",
    "user_name": "Corporate Executive",
    "travel_style": "business",
    "user_preferences": {
      "hotel_rating_min": 4,
      "amenities": ["business center", "fast wifi", "gym"]
    },
    "profit_priority": true,
    "business_rules": {
      "markup_percentage": 16,
      "loyalty_multiplier": 1.5
    }
  }'
```

## Response Structure

All requests will return a comprehensive response:

```json
{
  "status": "success",
  "user_id": "user_123",
  
  "hotel_options": [
    {
      "name": "Hotel Name",
      "rating": 4.5,
      "price_per_night": 250,
      "location": "City Center",
      "profit_potential": {
        "total_profit": 500.50,
        "margin_percentage": 18.5
      }
    }
  ],
  
  "flight_options": [
    {
      "id": "flight_123",
      "airline": "Air France",
      "price": 450,
      "duration": "8 hours"
    }
  ],
  
  "analysis": "Detailed LLM analysis of all options...",
  
  "recommendation": {
    "hotel": { /* Best hotel option */ },
    "flights": { /* Best flight option */ },
    "total_package_cost": 2500.00,
    "estimated_user_cost": 2500.00,
    "platform_profit": 375.00
  },
  
  "reasoning": "Why this option was selected based on profit and user satisfaction...",
  
  "profit_metrics": {
    "total_revenue": 2500.00,
    "platform_profit": 375.00,
    "profit_margin_percentage": 15.0
  },
  
  "roi_analysis": {
    "total_revenue": 2500.00,
    "platform_profit": 375.00,
    "profit_margin": 15.0,
    "customer_satisfaction": "high",
    "roi_percentage": 15.0
  },
  
  "complete_journey": {
    "destination": "Paris, France",
    "duration_days": 7,
    "hotel": "Hotel Name",
    "flights": "Air France",
    "estimated_total_cost": 2500.00
  }
}
```

## PowerShell Examples

### Simple Request
```powershell
$body = @{
    origin = "New York (JFK)"
    destination = "Paris, France"
    check_in = "2026-04-15"
    check_out = "2026-04-22"
    passengers = 1
    budget = 5000
    travel_style = "luxury"
    profit_priority = $true
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/recommend/travel-plan" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $body | Select-Object -ExpandProperty Content | ConvertFrom-Json
```

### Save Response to File
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:8000/recommend/travel-plan" `
    -Method Post `
    -Headers @{"Content-Type" = "application/json"} `
    -Body $body

$response.Content | Out-File -FilePath "recommendation.json"
```

## Python Examples

### Basic Request
```python
import requests
import json

url = "http://localhost:8000/recommend/travel-plan"

payload = {
    "origin": "New York (JFK)",
    "destination": "Paris, France",
    "check_in": "2026-04-15",
    "check_out": "2026-04-22",
    "passengers": 1,
    "budget": 5000,
    "travel_style": "luxury",
    "profit_priority": True
}

response = requests.post(url, json=payload, timeout=60)

if response.status_code == 200:
    data = response.json()
    
    # Extract key information
    rec = data['recommendation']
    print(f"Hotel: {rec['hotel']['name']}")
    print(f"Total Cost: ${rec['total_package_cost']:.2f}")
    print(f"Platform Profit: ${rec['platform_profit']:.2f}")
    print(f"\nReasoning:\n{data['reasoning']}")
else:
    print(f"Error: {response.status_code}")
```

### Full Analysis
```python
import requests
import json

response = requests.post("http://localhost:8000/recommend/travel-plan", json=payload)
data = response.json()

print("=== TRAVEL RECOMMENDATION ===")
print(f"\nStatus: {data['status']}")

print("\n📊 PROFIT METRICS:")
profit = data['profit_metrics']
print(f"  Revenue: ${profit['total_revenue']:.2f}")
print(f"  Profit: ${profit['platform_profit']:.2f}")
print(f"  Margin: {profit['profit_margin_percentage']:.1f}%")

print("\n📈 ROI ANALYSIS:")
roi = data['roi_analysis']
print(f"  ROI: {roi['roi_percentage']:.1f}%")
print(f"  Customer Satisfaction: {roi['customer_satisfaction']}")

print("\n🏨 HOTEL OPTIONS:")
for i, hotel in enumerate(data['hotel_options'][:3], 1):
    print(f"  {i}. {hotel['name']}")
    print(f"     Rating: {hotel['rating']}/5")
    print(f"     Price: ${hotel['price_per_night']}/night")

print("\n🤖 LLM ANALYSIS:")
print(data['analysis'][:500] + "...")

print("\n💡 RECOMMENDATION REASONING:")
print(data['reasoning'])
```

## Expected Response Times

- Simple query: 5-10 seconds
- Complex analysis (LLM): 10-30 seconds
- Large groups (10+ passengers): 15-40 seconds

## Key Features

✅ **Profit Maximization**
- Calculates profit potential for each option
- Applies business rules and markups
- Considers bundle discounts and loyalty multipliers

✅ **Comprehensive Analysis**
- LLM analyzes all available options
- Provides detailed reasoning
- Suggests upsell opportunities

✅ **Multi-Option Search**
- Hotels from search engine
- Routes from travel database
- Integrated flight options

✅ **Business Rules Engine**
- Custom markups and commissions
- Loyalty multipliers
- Group bonuses
- Minimum commission handling

✅ **Detailed Response**
- All available options
- Best recommendation
- ROI analysis
- Complete journey itinerary
- Profit metrics
