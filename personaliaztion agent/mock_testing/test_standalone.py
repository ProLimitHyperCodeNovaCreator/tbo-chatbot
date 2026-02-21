#!/usr/bin/env python3
"""
Standalone test script that works WITHOUT database
Tests the personalization logic directly
"""
import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import app modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Use mock configuration
import mock_testing.config_mock as config_module
sys.modules['app.config'] = config_module

# Use mock database
from mock_testing.mock_db import mock_db
sys.modules['app.db'] = type('module', (), {'db': mock_db})()

from app.rules import apply_rules
from app.ml.ranker import MLRanker
from mock_testing.trainer_mock import train_model


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


async def test_mock_database():
    """Test 1: Mock Database"""
    print_section("TEST 1: Mock Database")
    
    await mock_db.connect()
    
    # Test user lookup
    user = await mock_db.user_profile.find_unique(where={"user_id": "sample-user-1"})
    print(f"✓ Found user: {user.user_id}")
    print(f"  - Agency: {user.agency_id}")
    print(f"  - Budget Preference: {user.budget_pref}")
    print(f"  - Preferred Suppliers: {user.preferred_suppliers}")
    
    # Test stats lookup
    stats = await mock_db.booking_stats.find_unique(where={"agency_id": user.agency_id})
    print(f"\n✓ Found booking stats for agency: {stats.agency_id}")
    print(f"  - Avg Booking Value: ${stats.avg_booking_value}")
    print(f"  - Cancellation Rate: {stats.cancellation_rate * 100}%")
    print(f"  - Conversion Rate: {stats.conversion_rate * 100}%")
    
    return True


async def test_rule_based_scoring():
    """Test 2: Rule-Based Scoring"""
    print_section("TEST 2: Rule-Based Scoring")
    
    user = await mock_db.user_profile.find_unique(where={"user_id": "sample-user-1"})
    stats = await mock_db.booking_stats.find_unique(where={"agency_id": user.agency_id})
    
    # Test different options
    test_options = [
        {
            "option_id": "opt-1",
            "price_bucket": "mid",
            "distance_bucket": "near",
            "rating_bucket": "high",
            "supplier_id": "supplier-1",
            "refundable": True
        },
        {
            "option_id": "opt-2",
            "price_bucket": "low",
            "distance_bucket": "far",
            "rating_bucket": "low",
            "supplier_id": "supplier-unknown",
            "refundable": False
        },
        {
            "option_id": "opt-3",
            "price_bucket": "high",
            "distance_bucket": "mid",
            "rating_bucket": "high",
            "supplier_id": "supplier-2",
            "refundable": True
        }
    ]
    
    print(f"Testing rules for user: {user.user_id}")
    print(f"User preferences: budget={user.budget_pref}, refund={user.refund_pref}")
    print(f"Agency cancellation rate: {stats.cancellation_rate * 100}%\n")
    
    for option in test_options:
        score, reasons = apply_rules(user, stats, option)
        print(f"Option {option['option_id']}:")
        print(f"  Price: {option['price_bucket']}, Supplier: {option['supplier_id']}, Refundable: {option['refundable']}")
        print(f"  Rule Score: {score:.3f}")
        print(f"  Reasons: {', '.join(reasons) if reasons else 'No matches'}")
        print()
    
    return True


async def test_ml_model_training():
    """Test 3: ML Model Training"""
    print_section("TEST 3: ML Model Training")
    
    print("Training ML model with mock data...")
    print("(This creates 150 training samples)")
    
    metrics = await train_model()
    
    if metrics:
        print("\n✓ Model trained successfully!")
        print(f"\nTraining Metrics:")
        print(f"  - Accuracy:  {metrics['accuracy']:.3f}")
        print(f"  - Precision: {metrics['precision']:.3f}")
        print(f"  - Recall:    {metrics['recall']:.3f}")
        print(f"  - F1 Score:  {metrics['f1_score']:.3f}")
        print(f"  - Samples:   {metrics['training_samples']}")
        return True
    else:
        print("\n⚠ Model training skipped (insufficient data or other issue)")
        return False


async def test_ml_scoring():
    """Test 4: ML Model Scoring"""
    print_section("TEST 4: ML Model Scoring")
    
    try:
        ranker = MLRanker()
        print(f"ML Model Status: {'Available ✓' if ranker.is_available else 'Not Available ✗'}")
        
        if ranker.is_available:
            # Test scoring
            test_option = {
                "price_bucket": "mid",
                "distance_bucket": "near",
                "rating_bucket": "high",
                "supplier_id": "supplier-1",
                "refundable": True
            }
            
            score = ranker.score(test_option)
            print(f"\nML Score for sample option: {score:.4f}")
            print(f"Option: {test_option}")
        
        return True
    except Exception as e:
        print(f"⚠ ML scoring not available: {str(e)}")
        return False


async def test_full_personalization():
    """Test 5: Complete Personalization Pipeline"""
    print_section("TEST 5: Complete Personalization")
    
    user = await mock_db.user_profile.find_unique(where={"user_id": "sample-user-1"})
    stats = await mock_db.booking_stats.find_unique(where={"agency_id": user.agency_id})
    
    # Try to load ML model
    try:
        ranker = MLRanker()
        ml_available = ranker.is_available
    except:
        ranker = None
        ml_available = False
    
    print(f"User: {user.user_id}")
    print(f"ML Model: {'Available ✓' if ml_available else 'Not Available (using rules only)'}\n")
    
    # Test options (simulating hotel/flight options)
    options = [
        {
            "option_id": "hotel-luxury",
            "name": "Luxury Hotel - High End",
            "base_score": 0.85,
            "price_bucket": "high",
            "distance_bucket": "near",
            "rating_bucket": "high",
            "supplier_id": "supplier-1",
            "refundable": True
        },
        {
            "option_id": "hotel-budget",
            "name": "Budget Hotel - Economy",
            "base_score": 0.70,
            "price_bucket": "low",
            "distance_bucket": "far",
            "rating_bucket": "mid",
            "supplier_id": "supplier-3",
            "refundable": False
        },
        {
            "option_id": "hotel-business",
            "name": "Business Hotel - Mid Range",
            "base_score": 0.80,
            "price_bucket": "mid",
            "distance_bucket": "near",
            "rating_bucket": "high",
            "supplier_id": "supplier-1",
            "refundable": True
        },
        {
            "option_id": "hotel-standard",
            "name": "Standard Hotel - Good Value",
            "base_score": 0.75,
            "price_bucket": "mid",
            "distance_bucket": "mid",
            "rating_bucket": "mid",
            "supplier_id": "supplier-2",
            "refundable": True
        }
    ]
    
    # Score each option
    results = []
    for opt in options:
        rule_score, reasons = apply_rules(user, stats, opt)
        ml_score = ranker.score(opt) if ml_available else 0.0
        
        final_score = opt["base_score"] + rule_score + ml_score
        
        results.append({
            "option_id": opt["option_id"],
            "name": opt["name"],
            "base_score": opt["base_score"],
            "rule_score": rule_score,
            "ml_score": ml_score,
            "final_score": final_score,
            "reasons": reasons
        })
    
    # Sort by final score
    results.sort(key=lambda x: x["final_score"], reverse=True)
    
    print("PERSONALIZED RANKING:")
    print("-" * 70)
    for i, result in enumerate(results, 1):
        print(f"\n#{i} - {result['name']}")
        print(f"     Option ID: {result['option_id']}")
        print(f"     Base Score:  {result['base_score']:.3f}")
        print(f"     Rule Score:  {result['rule_score']:.3f}")
        print(f"     ML Score:    {result['ml_score']:.3f}")
        print(f"     FINAL SCORE: {result['final_score']:.3f} ⭐")
        if result['reasons']:
            print(f"     Why: {', '.join(result['reasons'])}")
    
    return True


async def test_different_users():
    """Test 6: Test with Different User Profiles"""
    print_section("TEST 6: Different User Profiles")
    
    test_users = ["sample-user-1", "test-user-1", "test-user-2"]
    
    # Try to load ML model
    try:
        ranker = MLRanker()
        ml_available = ranker.is_available
    except:
        ranker = None
        ml_available = False
    
    # Same test option
    test_option = {
        "option_id": "test-opt",
        "price_bucket": "mid",
        "distance_bucket": "near",
        "rating_bucket": "high",
        "supplier_id": "supplier-1",
        "refundable": True,
        "base_score": 0.80
    }
    
    print(f"Testing same option for different users...")
    print(f"Option: mid-price, near, high-rating, supplier-1, refundable\n")
    
    for user_id in test_users:
        user = await mock_db.user_profile.find_unique(where={"user_id": user_id})
        if not user:
            continue
            
        stats = await mock_db.booking_stats.find_unique(where={"agency_id": user.agency_id})
        
        rule_score, reasons = apply_rules(user, stats, test_option)
        ml_score = ranker.score(test_option) if ml_available else 0.0
        final_score = test_option["base_score"] + rule_score + ml_score
        
        print(f"User: {user_id}")
        print(f"  Profile: budget={user.budget_pref}, refund={user.refund_pref}")
        print(f"  Preferred suppliers: {user.preferred_suppliers}")
        print(f"  Rule Score: {rule_score:.3f}")
        print(f"  ML Score: {ml_score:.3f}")
        print(f"  Final Score: {final_score:.3f}")
        print(f"  Reasons: {', '.join(reasons) if reasons else 'No matches'}")
        print()
    
    return True


async def main():
    """Run all tests"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  PERSONALIZATION ENGINE - STANDALONE TEST SUITE".center(68) + "█")
    print("█" + "  (No Database Required)".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    tests = [
        ("Mock Database", test_mock_database),
        ("Rule-Based Scoring", test_rule_based_scoring),
        ("ML Model Training", test_ml_model_training),
        ("ML Model Scoring", test_ml_scoring),
        ("Full Personalization", test_full_personalization),
        ("Different Users", test_different_users),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ {test_name} failed with error:")
            print(f"   {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print_section("TEST SUMMARY")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n{'=' * 70}")
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your personalization engine is working!")
    elif passed >= total - 1:
        print("\n✓ Core functionality working! ML model may need training.")
    else:
        print("\n⚠ Some tests failed. Check the output above.")
    
    print("=" * 70 + "\n")
    
    await mock_db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
