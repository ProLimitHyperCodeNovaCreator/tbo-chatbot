#!/usr/bin/env python3
"""
Single Complex Query Test - Tests the full travel recommendation integration
"""
import requests
import json
import time
from datetime import datetime, timedelta

# Configuration
ORCHESTRATOR_URL = "http://localhost:8000"
TIMEOUT = 600  # 10 minutes

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    print(f"\n{BOLD}{BLUE}{'='*100}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'='*100}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✓ {text}{RESET}")

def print_error(text):
    print(f"{RED}✗ {text}{RESET}")

def print_info(text):
    print(f"{YELLOW}ℹ {text}{RESET}")

def test_orchestrator_health():
    """Test Orchestrator health endpoint"""
    print_header("STEP 1: Testing Orchestrator Health")
    
    try:
        response = requests.get(f"{ORCHESTRATOR_URL}/health", timeout=10)
        if response.status_code == 200:
            print_success("Orchestrator is healthy")
            print(f"  Response: {response.json()}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Failed to connect to Orchestrator: {str(e)}")
        return False

def test_complex_travel_recommendation():
    """Test complex travel recommendation with multiple options"""
    print_header("STEP 2: Testing Complex Travel Recommendation")
    
    # Complex user profile for luxury business travel
    request_data = {
        "origin": "New York (JFK)",
        "destination": "Paris, France",
        "check_in": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
        "check_out": (datetime.now() + timedelta(days=21)).strftime("%Y-%m-%d"),
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
            "include_upsells": True,
            "prefer_partner_hotels": True
        }
    }
    
    print(f"Sending request:")
    print(f"  Origin: {request_data['origin']}")
    print(f"  Destination: {request_data['destination']}")
    print(f"  Duration: {request_data['check_in']} to {request_data['check_out']}")
    print(f"  Passengers: {request_data['passengers']}")
    print(f"  Budget: ${request_data['budget']}")
    print()
    
    start_time = time.time()
    
    try:
        print_info(f"Waiting for response (timeout: {TIMEOUT}s / 10 minutes)...")
        print_info("This may take 30-60 seconds on first run (LLM model warmup)...")
        print()
        
        response = requests.post(
            f"{ORCHESTRATOR_URL}/recommend/travel-plan",
            json=request_data,
            timeout=TIMEOUT
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            print_success(f"Recommendation generated successfully in {elapsed_time:.2f}s")
            
            result = response.json()
            
            # Validate response structure
            required_fields = [
                "recommendation",
                "all_recommendations",
                "analysis",
                "comparison_summary"
            ]
            
            missing_fields = [f for f in required_fields if f not in result]
            if missing_fields:
                print_error(f"Missing fields in response: {missing_fields}")
                return False
            
            print_success(f"Response structure validated - all required fields present")
            
            # Display recommendations summary
            print(f"\n{BOLD}RECOMMENDATIONS SUMMARY:{RESET}")
            if "all_recommendations" in result and result["all_recommendations"]:
                for i, rec in enumerate(result["all_recommendations"][:5], 1):
                    hotel_name = rec.get("hotel_name", "N/A")
                    flight_info = rec.get("flight_info", {})
                    total_cost = rec.get("total_cost", 0)
                    profit = rec.get("profit", 0)
                    print(f"\n  Option {i}:")
                    print(f"    Hotel: {hotel_name}")
                    print(f"    Flight: {flight_info.get('airline', 'N/A')} ({flight_info.get('departure', 'N/A')} to {flight_info.get('arrival', 'N/A')})")
                    print(f"    Total Cost: ${total_cost:.2f}")
                    print(f"    Profit: ${profit:.2f}")
            
            # Display best recommendation
            best_rec = result.get("recommendation", {})
            if best_rec:
                print(f"\n{BOLD}BEST RECOMMENDATION (Selected by LLM):{RESET}")
                print(f"  Hotel: {best_rec.get('hotel_name', 'N/A')}")
                print(f"  Total Cost: ${best_rec.get('total_cost', 0):.2f}")
            
            # Display LLM analysis
            if "analysis" in result and result["analysis"]:
                print(f"\n{BOLD}LLM ANALYSIS:{RESET}")
                analysis_text = result["analysis"]
                # Show first 500 chars of analysis
                if len(analysis_text) > 500:
                    print(f"  {analysis_text[:500]}...")
                else:
                    print(f"  {analysis_text}")
            
            print(f"\n{BOLD}RESPONSE METRICS:{RESET}")
            print(f"  Total Recommendations: {len(result.get('all_recommendations', []))}")
            print(f"  Response Time: {elapsed_time:.2f}s")
            print(f"  Status: {result.get('status', 'unknown')}")
            
            return True
            
        else:
            elapsed_time = time.time() - start_time
            print_error(f"Request failed with status {response.status_code} after {elapsed_time:.2f}s")
            print(f"Response: {response.text}")
            return False
            
    except requests.Timeout:
        elapsed_time = time.time() - start_time
        print_error(f"Request timed out after {elapsed_time:.2f}s")
        return False
    except Exception as e:
        elapsed_time = time.time() - start_time
        print_error(f"Request failed after {elapsed_time:.2f}s: {str(e)}")
        return False

def main():
    """Run all tests"""
    print(f"\n{BOLD}{BLUE}{'█'*100}{RESET}")
    print(f"{BOLD}SINGLE COMPLEX QUERY TEST - Travel Recommendation Integration{RESET}")
    print(f"{BOLD}{BLUE}{'█'*100}{RESET}\n")
    
    # Test 1: Health check
    health_ok = test_orchestrator_health()
    
    if not health_ok:
        print_error("\nOrchestrator is not responding. Please ensure Docker services are running:")
        print(f"  {YELLOW}docker-compose up -d{RESET}")
        return False
    
    # Test 2: Complex recommendation
    test_ok = test_complex_travel_recommendation()
    
    # Summary
    print_header("TEST SUMMARY")
    if health_ok and test_ok:
        print_success("All tests PASSED!")
        print(f"\n{GREEN}✓ Orchestrator is healthy{RESET}")
        print(f"{GREEN}✓ Complex travel recommendation working{RESET}")
        print(f"{GREEN}✓ Multi-option generation functioning{RESET}")
        print(f"{GREEN}✓ LLM integration operational{RESET}")
        return True
    else:
        print_error("Some tests FAILED!")
        if not health_ok:
            print_error("  - Orchestrator health check failed")
        if not test_ok:
            print_error("  - Complex recommendation test failed")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
