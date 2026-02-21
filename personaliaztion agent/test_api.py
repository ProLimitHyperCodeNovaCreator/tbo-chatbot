#!/usr/bin/env python3
"""
Test script for the personalization API
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_model_status():
    """Test model status endpoint"""
    print("Testing model status...")
    response = requests.get(f"{BASE_URL}/model/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_personalize():
    """Test personalization endpoint"""
    print("Testing personalization...")
    
    payload = {
        "user_id": "sample-user-1",
        "options": [
            {
                "option_id": "opt-1",
                "base_score": 0.8,
                "price_bucket": "mid",
                "distance_bucket": "near",
                "rating_bucket": "high",
                "supplier_id": "supplier-1",
                "refundable": True
            },
            {
                "option_id": "opt-2",
                "base_score": 0.75,
                "price_bucket": "low",
                "distance_bucket": "mid",
                "rating_bucket": "mid",
                "supplier_id": "supplier-2",
                "refundable": False
            },
            {
                "option_id": "opt-3",
                "base_score": 0.85,
                "price_bucket": "high",
                "distance_bucket": "far",
                "rating_bucket": "high",
                "supplier_id": "supplier-3",
                "refundable": True
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/personalize", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_feedback():
    """Test feedback endpoint"""
    print("Testing feedback recording...")
    
    params = {
        "user_id": "sample-user-1",
        "option_id": "opt-1",
        "accepted": True,
        "price_bucket": "mid",
        "distance_bucket": "near",
        "rating_bucket": "high",
        "supplier_id": "supplier-1",
        "refundable": True
    }
    
    response = requests.post(f"{BASE_URL}/feedback", params=params)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def test_training():
    """Test model training endpoint"""
    print("Testing model training...")
    
    response = requests.post(f"{BASE_URL}/train")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200

def main():
    """Run all tests"""
    print("=" * 60)
    print("Personalization API Test Suite")
    print("=" * 60 + "\n")
    
    tests = [
        ("Health Check", test_health),
        ("Model Status", test_model_status),
        ("Personalization", test_personalize),
        ("Feedback", test_feedback),
        ("Training", test_training),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {str(e)}\n")
            results.append((test_name, False))
    
    # Print summary
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} tests passed")

if __name__ == "__main__":
    main()
