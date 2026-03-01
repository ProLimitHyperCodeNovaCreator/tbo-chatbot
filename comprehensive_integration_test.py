#!/usr/bin/env python3
"""
Comprehensive Integration Testing Script
Tests all three components together: Orchestrator, Hotel Search, and Vector DB (Qdrant)
Validates the complete travel recommendation flow with detailed user inputs
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import sys
from dataclasses import dataclass

# ==================== CONFIGURATION ====================

BASE_URLS = {
    "orchestrator": "http://localhost:8000",
    "hotel_search": "http://localhost:5000",
    "qdrant": "http://localhost:6333",
    "ollama": "http://localhost:11434"
}

TEST_TIMEOUT = 120  # seconds per request


# ==================== DATA CLASSES ====================

@dataclass
class TestResult:
    """Test result container"""
    test_name: str
    component: str
    passed: bool
    message: str
    duration: float
    details: Optional[Dict] = None
    
    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        return f"{status} | {self.test_name:<40} | {self.message:<50} | {self.duration:.2f}s"


# ==================== REALISTIC TEST DATA ====================

class TestProfiles:
    """Realistic user profiles with detailed information"""
    
    @staticmethod
    def luxury_business_traveler() -> Dict[str, Any]:
        """High-income executive, luxury preference, profit priority"""
        return {
            "origin": "New York (JFK)",
            "destination": "Paris, France",
            "check_in": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "check_out": (datetime.now() + timedelta(days=37)).strftime("%Y-%m-%d"),
            "passengers": 1,
            "budget": 8000,
            
            "user_id": "user_luxury_001",
            "user_name": "James Anderson",
            "travel_style": "luxury",
            "user_preferences": {
                "hotel_rating_min": 4.5,
                "amenities": ["spa", "fine dining", "business center"],
                "location": "city center",
                "room_type": "suite"
            },
            "special_requirements": "Late checkout preferred, airport transfers",
            
            "profit_priority": True,
            "business_rules": {
                "markup_percentage": 20,
                "min_commission": 50,
                "preferred_partners": ["Four Seasons", "Ritz Carlton"],
                "bundle_discount": 8
            }
        }
    
    @staticmethod
    def budget_family_vacation() -> Dict[str, Any]:
        """Family with multiple passengers, budget conscious"""
        return {
            "origin": "London (LHR)",
            "destination": "Barcelona, Spain",
            "check_in": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
            "check_out": (datetime.now() + timedelta(days=52)).strftime("%Y-%m-%d"),
            "passengers": 4,
            "budget": 3000,
            
            "user_id": "user_family_001",
            "user_name": "Sarah Williams",
            "travel_style": "budget",
            "user_preferences": {
                "hotel_rating_min": 3.5,
                "amenities": ["pool", "kids activities", "family rooms"],
                "location": "beach",
                "room_type": "family suite"
            },
            "special_requirements": "Children 5 and 8, need cribs/high chair",
            
            "profit_priority": False,
            "business_rules": {
                "group_bonus": 0.08,
                "bundle_discount": 5
            }
        }
    
    @staticmethod
    def adventure_traveler() -> Dict[str, Any]:
        """Young professional, adventure/experience focused"""
        return {
            "origin": "Singapore (SIN)",
            "destination": "Bali, Indonesia",
            "check_in": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
            "check_out": (datetime.now() + timedelta(days=75)).strftime("%Y-%m-%d"),
            "passengers": 2,
            "budget": 4000,
            
            "user_id": "user_adventure_001",
            "user_name": "Alex Chen",
            "travel_style": "adventure",
            "user_preferences": {
                "hotel_rating_min": 4.0,
                "amenities": ["yoga", "surfing", "wellness", "mountain views"],
                "location": "near beaches and mountains",
                "room_type": "villa or bungalow"
            },
            "special_requirements": "Nearby adventure activities, eco-friendly options",
            
            "profit_priority": True,
            "business_rules": {
                "markup_percentage": 18,
                "bundle_discount": 6
            }
        }
    
    @staticmethod
    def corporate_group_retreat() -> Dict[str, Any]:
        """Large group booking, team retreat"""
        return {
            "origin": "Berlin (BER)",
            "destination": "Zurich, Switzerland",
            "check_in": (datetime.now() + timedelta(days=50)).strftime("%Y-%m-%d"),
            "check_out": (datetime.now() + timedelta(days=55)).strftime("%Y-%m-%d"),
            "passengers": 12,
            "budget": 18000,
            
            "user_id": "user_corporate_001",
            "user_name": "Michael Johnson",
            "travel_style": "business",
            "user_preferences": {
                "hotel_rating_min": 4.2,
                "amenities": ["conference rooms", "team activities", "dining"],
                "location": "downtown",
                "room_type": "mix of singles and doubles"
            },
            "special_requirements": "Group rates, team building activities, dietary requirements for staff",
            
            "profit_priority": True,
            "business_rules": {
                "group_bonus": 0.12,
                "bundle_discount": 10,
                "loyalty_multiplier": 1.5
            }
        }


# ==================== TEST CASES ====================

class IntegrationTests:
    """Integration test suite for travel recommendation system"""
    
    def __init__(self):
        self.results: List[TestResult] = []
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def run_all_tests(self) -> bool:
        """Run all tests and return success status"""
        print("\n" + "="*100)
        print("🔧 COMPREHENSIVE INTEGRATION TEST SUITE")
        print("="*100 + "\n")
        
        # Phase 1: Component Health Checks
        print("PHASE 1: Service Health Checks")
        print("-" * 100)
        self.test_orchestrator_health()
        self.test_hotel_search_health()
        self.test_qdrant_health()
        self.test_ollama_health()
        
        # Phase 2: Individual Component Tests
        print("\nPHASE 2: Individual Component Tests")
        print("-" * 100)
        self.test_hotel_search_functionality()
        self.test_orchestrator_basic_query()
        
        # Phase 3: Full Integration Tests with Realistic Data
        print("\nPHASE 3: Full Integration Tests (Multi-Option Recommendation)")
        print("-" * 100)
        self.test_travel_recommendation_luxury()
        self.test_travel_recommendation_family()
        self.test_travel_recommendation_adventure()
        self.test_travel_recommendation_corporate()
        
        # Phase 4: Data Quality & Validation
        print("\nPHASE 4: Data Quality & Response Validation")
        print("-" * 100)
        self.test_response_structure()
        self.test_profit_calculations()
        self.test_llm_analysis_quality()
        
        # Print summary
        self.print_summary()
        return all(r.passed for r in self.results)
    
    # ==================== PHASE 1: HEALTH CHECKS ====================
    
    def test_orchestrator_health(self) -> TestResult:
        """Test orchestrator API health"""
        start = time.time()
        test_name = "Orchestrator Health Check"
        component = "Orchestrator"
        
        try:
            response = self.session.get(
                f"{BASE_URLS['orchestrator']}/health",
                timeout=10
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=True,
                    message=f"Service healthy ({data.get('version', 'N/A')})",
                    duration=duration,
                    details=data
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Connection failed: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    def test_hotel_search_health(self) -> TestResult:
        """Test hotel search engine health"""
        start = time.time()
        test_name = "Hotel Search Health Check"
        component = "Hotel Search"
        
        try:
            response = self.session.get(
                f"{BASE_URLS['hotel_search']}/health",
                timeout=10
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=True,
                    message="Service healthy",
                    duration=duration,
                    details=response.json()
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Connection failed: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    def test_qdrant_health(self) -> TestResult:
        """Test Qdrant vector DB health"""
        start = time.time()
        test_name = "Qdrant Vector DB Health Check"
        component = "Qdrant"
        
        try:
            response = self.session.get(
                f"{BASE_URLS['qdrant']}/health",
                timeout=10
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=True,
                    message="Vector DB healthy",
                    duration=duration,
                    details=response.json()
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Connection failed: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    def test_ollama_health(self) -> TestResult:
        """Test Ollama LLM health"""
        start = time.time()
        test_name = "Ollama LLM Health Check"
        component = "Ollama"
        
        try:
            response = self.session.get(
                f"{BASE_URLS['ollama']}/api/tags",
                timeout=10
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                models = len(data.get("models", []))
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=True,
                    message=f"LLM ready ({models} models available)",
                    duration=duration,
                    details=data
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Connection failed: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    # ==================== PHASE 2: COMPONENT TESTS ====================
    
    def test_hotel_search_functionality(self) -> TestResult:
        """Test hotel search endpoint"""
        start = time.time()
        test_name = "Hotel Search Functionality"
        component = "Hotel Search"
        
        try:
            payload = {
                "query": "5 star hotels in Paris France",
                "num_results": 5
            }
            response = self.session.post(
                f"{BASE_URLS['hotel_search']}/search",
                json=payload,
                timeout=10
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=len(results) > 0,
                    message=f"Found {len(results)} hotels",
                    duration=duration,
                    details={"hotel_count": len(results)}
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Search failed: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    def test_orchestrator_basic_query(self) -> TestResult:
        """Test basic orchestrator query"""
        start = time.time()
        test_name = "Orchestrator Basic Query"
        component = "Orchestrator"
        
        try:
            payload = {
                "query": "What are the best hotels in Paris?",
                "user_id": "test_user_001"
            }
            response = self.session.post(
                f"{BASE_URLS['orchestrator']}/query",
                json=payload,
                timeout=30
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                has_response = bool(data.get("response"))
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=has_response,
                    message=f"Query processed (complexity: {data.get('complexity_level')})",
                    duration=duration
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Query failed: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    # ==================== PHASE 3: FULL INTEGRATION TESTS ====================
    
    def test_travel_recommendation_luxury(self) -> TestResult:
        """Test travel recommendation with luxury profile"""
        profile_data = TestProfiles.luxury_business_traveler()
        return self._test_travel_recommendation(
            profile_data,
            "Luxury Business Travel Recommendation",
            "Orchestrator"
        )
    
    def test_travel_recommendation_family(self) -> TestResult:
        """Test travel recommendation with family profile"""
        profile_data = TestProfiles.budget_family_vacation()
        return self._test_travel_recommendation(
            profile_data,
            "Family Budget Travel Recommendation",
            "Orchestrator"
        )
    
    def test_travel_recommendation_adventure(self) -> TestResult:
        """Test travel recommendation with adventure profile"""
        profile_data = TestProfiles.adventure_traveler()
        return self._test_travel_recommendation(
            profile_data,
            "Adventure Travel Recommendation",
            "Orchestrator"
        )
    
    def test_travel_recommendation_corporate(self) -> TestResult:
        """Test travel recommendation with corporate profile"""
        profile_data = TestProfiles.corporate_group_retreat()
        return self._test_travel_recommendation(
            profile_data,
            "Corporate Group Travel Recommendation",
            "Orchestrator"
        )
    
    def _test_travel_recommendation(
        self,
        profile: Dict[str, Any],
        test_name: str,
        component: str
    ) -> TestResult:
        """Generic travel recommendation test"""
        start = time.time()
        
        try:
            print(f"\n  Testing: {test_name}")
            print(f"  User: {profile.get('user_name')} | Origin: {profile.get('origin')} → {profile.get('destination')}")
            
            response = self.session.post(
                f"{BASE_URLS['orchestrator']}/recommend/travel-plan",
                json=profile,
                timeout=TEST_TIMEOUT
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response structure
                has_all_fields = all(key in data for key in [
                    "status", "hotel_options", "all_recommendations", "recommendation",
                    "analysis", "profit_metrics", "roi_analysis"
                ])
                
                num_options = len(data.get("all_recommendations", []))
                
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=has_all_fields and num_options >= 3,
                    message=f"{num_options} options analyzed | Best choice selected",
                    duration=duration,
                    details={
                        "recommendation_count": num_options,
                        "best_hotel": data.get("recommendation", {}).get("hotel", {}).get("name"),
                        "platform_profit": data.get("recommendation", {}).get("platform_profit")
                    }
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}: {response.text[:50]}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Error: {str(e)[:60]}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    # ==================== PHASE 4: DATA QUALITY TESTS ====================
    
    def test_response_structure(self) -> TestResult:
        """Test response structure completeness"""
        start = time.time()
        test_name = "Response Structure Validation"
        component = "Orchestrator"
        
        try:
            profile = TestProfiles.luxury_business_traveler()
            response = self.session.post(
                f"{BASE_URLS['orchestrator']}/recommend/travel-plan",
                json=profile,
                timeout=TEST_TIMEOUT
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = [
                    "status", "hotel_options", "flight_options", "all_recommendations",
                    "recommendation", "analysis", "reasoning", "comparison_summary",
                    "profit_metrics", "roi_analysis", "complete_journey"
                ]
                
                missing = [f for f in required_fields if f not in data]
                passed = len(missing) == 0
                
                message = "All fields present" if passed else f"Missing: {', '.join(missing[:3])}"
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=passed,
                    message=message,
                    duration=duration
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Error: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    def test_profit_calculations(self) -> TestResult:
        """Validate profit calculations across options"""
        start = time.time()
        test_name = "Profit Calculation Validation"
        component = "Orchestrator"
        
        try:
            profile = TestProfiles.luxury_business_traveler()
            response = self.session.post(
                f"{BASE_URLS['orchestrator']}/recommend/travel-plan",
                json=profile,
                timeout=TEST_TIMEOUT
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("all_recommendations", [])
                
                # Verify profit calculations
                valid_calculations = True
                for rec in recommendations:
                    profit = rec.get("profit_metrics", {})
                    if profit:
                        # Check that numbers are consistent
                        total = profit.get("total_profit", 0)
                        commission = profit.get("commission", 0)
                        if total < commission:  # Total should include bonuses
                            valid_calculations = False
                
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=valid_calculations and len(recommendations) > 0,
                    message=f"Validated {len(recommendations)} profit calculations",
                    duration=duration
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Error: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    def test_llm_analysis_quality(self) -> TestResult:
        """Check LLM analysis quality and presence"""
        start = time.time()
        test_name = "LLM Analysis Quality"
        component = "Orchestrator"
        
        try:
            profile = TestProfiles.luxury_business_traveler()
            response = self.session.post(
                f"{BASE_URLS['orchestrator']}/recommend/travel-plan",
                json=profile,
                timeout=TEST_TIMEOUT
            )
            duration = time.time() - start
            
            if response.status_code == 200:
                data = response.json()
                analysis = data.get("analysis", "")
                reasoning = data.get("reasoning", "")
                comparison = data.get("comparison_summary", "")
                
                # Check that we have substantive analysis
                analysis_length = len(analysis) + len(reasoning) + len(comparison)
                has_good_analysis = analysis_length > 200
                
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=has_good_analysis,
                    message=f"LLM provided detailed analysis ({analysis_length} chars)",
                    duration=duration
                )
            else:
                result = TestResult(
                    test_name=test_name,
                    component=component,
                    passed=False,
                    message=f"HTTP {response.status_code}",
                    duration=duration
                )
        except Exception as e:
            duration = time.time() - start
            result = TestResult(
                test_name=test_name,
                component=component,
                passed=False,
                message=f"Error: {str(e)}",
                duration=duration
            )
        
        self.results.append(result)
        print(result)
        return result
    
    # ==================== SUMMARY ====================
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*100)
        print("TEST RESULTS SUMMARY")
        print("="*100)
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed
        
        # Group by component
        by_component = {}
        for result in self.results:
            comp = result.component
            if comp not in by_component:
                by_component[comp] = {"passed": 0, "failed": 0}
            if result.passed:
                by_component[comp]["passed"] += 1
            else:
                by_component[comp]["failed"] += 1
        
        print("\nComponent Status:")
        print("-" * 100)
        for comp, stats in sorted(by_component.items()):
            total_comp = stats["passed"] + stats["failed"]
            print(f"  {comp:<25} {stats['passed']}/{total_comp} passed")
        
        print("\n" + "="*100)
        print(f"TOTAL: {passed}/{total} tests passed ({passed*100//total}%)")
        print("="*100 + "\n")
        
        if failed == 0:
            print("✅ ALL TESTS PASSED - Systems fully integrated!")
        else:
            print(f"⚠️  {failed} test(s) failed - Review above for details")
        
        return failed == 0


# ==================== MAIN ====================

if __name__ == "__main__":
    print("\n" + "🚀 Starting Comprehensive Integration Test Suite\n")
    
    tester = IntegrationTests()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)
