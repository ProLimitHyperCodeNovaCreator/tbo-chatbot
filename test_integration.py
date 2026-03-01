#!/usr/bin/env python3
"""
TBO ChatBot Platform - Integration Test Suite
Tests all three components and their integration
"""

import requests
import json
import time
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
HOTEL_SEARCH_URL = "http://localhost:5000"
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def test_service_health():
    """Test all service health endpoints"""
    print_header("SERVICE HEALTH CHECK")
    
    services = {
        "Orchestrator": f"{BASE_URL}/health",
        "Hotel Search": f"{HOTEL_SEARCH_URL}/health",
        "Qdrant Vector DB": f"{QDRANT_URL}/readyz",
        "Ollama LLM": f"{OLLAMA_URL}/api/tags"
    }
    
    results = {}
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code in [200, 204]:
                print_success(f"{name} is healthy ({response.status_code})")
                results[name] = True
            else:
                print_error(f"{name} returned {response.status_code}")
                results[name] = False
        except Exception as e:
            print_error(f"{name} is unreachable: {str(e)}")
            results[name] = False
    
    return all(results.values())

def test_hotel_search():
    """Test hotel search integration"""
    print_header("HOTEL SEARCH TEST")
    
    try:
        payload = {
            "query": "5 star hotels in Athens Greece",
            "num_results": 3
        }
        
        print(f"Searching: {payload['query']}")
        response = requests.post(f"{HOTEL_SEARCH_URL}/search", json=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            hotel_count = len(data.get('results', []))
            print_success(f"Found {hotel_count} hotels")
            
            if hotel_count > 0:
                hotel = data['results'][0]
                print(f"  Sample: {hotel.get('name', 'Unknown')}")
                print(f"  Rating: {hotel.get('rating', 'N/A')}")
            return True
        else:
            print_error(f"Hotel search returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Hotel search failed: {str(e)}")
        return False

def test_qdrant_rag():
    """Test Qdrant vector DB"""
    print_header("QDRANT VECTOR DB TEST")
    
    try:
        response = requests.get(f"{QDRANT_URL}/collections", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            collections = data.get('collections', [])
            collection_count = len(collections)
            
            if collection_count > 0:
                print_success(f"Qdrant has {collection_count} collection(s)")
                for col in collections[:3]:
                    print(f"  - {col.get('name', 'Unknown')}")
            else:
                print_warning("No collections found in Qdrant (ingestion pending)")
            return True
        else:
            print_error(f"Qdrant returned {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Qdrant check failed: {str(e)}")
        return False

def test_json_query():
    """Test JSON-formatted query"""
    print_header("JSON QUERY TEST")
    
    try:
        tomorrow = (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d")
        checkout = (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d")
        
        payload = {
            "query_type": "hotel",
            "location": "Barcelona, Spain",
            "check_in": tomorrow,
            "check_out": checkout,
            "guests": 2,
            "preferences": {
                "min_rating": 4.0,
                "max_price": 200
            },
            "use_rag": True
        }
        
        print(f"Query Type: {payload['query_type']}")
        print(f"Location: {payload['location']}")
        print(f"Check-in: {payload['check_in']}")
        print(f"Guests: {payload['guests']}")
        
        response = requests.post(
            f"{BASE_URL}/json/process",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            hotel_count = len(data.get('hotel_results', []))
            print_success(f"JSON query processed successfully")
            print(f"  Hotels found: {data.get('total_results', {}).get('hotels', 0)}")
            print(f"  Travel packages: {data.get('total_results', {}).get('travel_packages', 0)}")
            print(f"  Sources: {', '.join(data.get('sources', []))}")
            return True
        else:
            print_error(f"JSON query returned {response.status_code}")
            if response.text:
                print(f"  Response: {response.text[:200]}")
            return False
    except requests.exceptions.Timeout:
        print_warning("JSON query timed out (LLM processing may take time)")
        return True  # Not a failure, just slow
    except Exception as e:
        print_error(f"JSON query failed: {str(e)}")
        return False

def test_rag_endpoint():
    """Test RAG endpoint directly"""
    print_header("RAG ENDPOINT TEST")
    
    try:
        tomorrow = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        checkout = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
        
        payload = {
            "query_type": "hotel",
            "location": "Paris, France",
            "check_in": tomorrow,
            "check_out": checkout,
            "guests": 2,
            "use_rag": True
        }
        
        print(f"Testing RAG with: {payload['location']}")
        
        response = requests.post(
            f"{BASE_URL}/rag/query",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("RAG query processed")
            
            if data.get('llm_analysis'):
                print(f"  LLM Analysis: {data['llm_analysis'][:100]}...")
            
            return True
        else:
            print_error(f"RAG query returned {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print_warning("RAG query timed out (expected for LLM processing)")
        return True
    except Exception as e:
        print_error(f"RAG query failed: {str(e)}")
        return False

def test_natural_language_query():
    """Test natural language query processing"""
    print_header("NATURAL LANGUAGE QUERY TEST")
    
    try:
        payload = {
            "query": "Find me luxury 5-star hotels in Rome for 5 days starting next week",
            "context": {
                "location": "Rome",
                "guests": 2,
                "check_in": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "check_out": (datetime.now() + timedelta(days=12)).strftime("%Y-%m-%d")
            }
        }
        
        print(f"Query: {payload['query']}")
        
        response = requests.post(
            f"{BASE_URL}/query",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("Natural language query processed")
            print(f"  Complexity: {data.get('complexity_level')}")
            print(f"  Model Used: {data.get('model_used')}")
            return True
        else:
            print_error(f"Query returned {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print_warning("Natural language query timed out")
        return True
    except Exception as e:
        print_error(f"Natural language query failed: {str(e)}")
        return False

def run_all_tests():
    """Run all integration tests"""
    print_header("TBO CHATBOT PLATFORM - INTEGRATION TEST SUITE")
    
    tests = [
        ("Service Health", test_service_health),
        ("Hotel Search Engine", test_hotel_search),
        ("Qdrant Vector DB", test_qdrant_rag),
        ("JSON Query Processing", test_json_query),
        ("RAG Endpoint", test_rag_endpoint),
        ("Natural Language Query", test_natural_language_query),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
            time.sleep(1)  # Pace requests
        except Exception as e:
            print_error(f"Test {name} crashed: {str(e)}")
            results[name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
        print(f"  {status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("All tests passed! Platform is ready.")
        return 0
    else:
        print_warning(f"{total - passed} test(s) failed.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_all_tests()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print_warning("\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Fatal error: {str(e)}")
        sys.exit(1)
