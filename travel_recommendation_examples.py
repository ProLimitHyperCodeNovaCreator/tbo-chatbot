#!/usr/bin/env python3
"""
Travel Recommendation API Examples
Shows how to use the intelligent travel recommendation endpoint
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def format_response(data):
    """Pretty print response data"""
    print(json.dumps(data, indent=2))

def example_1_luxury_business_trip():
    """
    Example 1: Luxury Business Trip to Paris
    High budget, quality focus, profit maximization
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: LUXURY BUSINESS TRIP TO PARIS")
    print("="*80)
    
    payload = {
        "origin": "New York (JFK)",
        "destination": "Paris, France",
        "check_in": "2026-04-15",
        "check_out": "2026-04-22",
        "passengers": 1,
        "budget": 5000,
        "user_id": "user_business_001",
        "user_name": "John Corporate",
        "travel_style": "luxury",
        "user_preferences": {
            "hotel_rating_min": 4.5,
            "amenities": ["business center", "fine dining", "spa"],
            "location": "Central Paris"
        },
        "special_requirements": "Executive floor, late check-in flexibility",
        "profit_priority": True,
        "business_rules": {
            "markup_percentage": 20,
            "min_commission": 50,
            "preferred_partners": ["Four Seasons", "Ritz Carlton", "Air France"],
            "bundle_discount": 5
        }
    }
    
    print("\nRequest Payload:")
    print(json.dumps(payload, indent=2))
    
    print("\nSending request to /recommend/travel-plan...")
    try:
        response = requests.post(
            f"{BASE_URL}/recommend/travel-plan",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ RESPONSE RECEIVED")
            print(f"Status: {data.get('status')}")
            print(f"User ID: {data.get('user_id')}")
            
            print("\n📊 RECOMMENDATION:")
            rec = data.get('recommendation', {})
            print(f"  Hotel: {rec.get('hotel', {}).get('name')}")
            print(f"  Total Cost: ${rec.get('total_package_cost', 0):.2f}")
            print(f"  Platform Profit: ${rec.get('platform_profit', 0):.2f}")
            
            print("\n💼 PROFIT METRICS:")
            profit = data.get('profit_metrics', {})
            print(f"  Revenue: ${profit.get('total_revenue', 0):.2f}")
            print(f"  Profit: ${profit.get('platform_profit', 0):.2f}")
            print(f"  Margin: {profit.get('profit_margin_percentage', 0):.1f}%")
            
            print("\n📈 ROI ANALYSIS:")
            roi = data.get('roi_analysis', {})
            print(f"  ROI: {roi.get('roi_percentage', 0):.1f}%")
            print(f"  Customer Satisfaction: {roi.get('customer_satisfaction')}")
            
            print("\n🤖 LLM ANALYSIS:")
            print(f"{data.get('analysis', 'Analysis not available')[:300]}...")
            
            print("\n💡 REASONING:")
            print(data.get('reasoning', 'Reasoning not provided'))
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_2_budget_family_vacation():
    """
    Example 2: Budget Family Vacation to Barcelona
    Multiple passengers, cost-conscious, still profitable
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: BUDGET FAMILY VACATION TO BARCELONA")
    print("="*80)
    
    payload = {
        "origin": "London (LHR)",
        "destination": "Barcelona, Spain",
        "check_in": "2026-07-01",
        "check_out": "2026-07-08",
        "passengers": 4,  # 2 adults, 2 children
        "budget": 2000,
        "user_id": "user_family_001",
        "user_name": "Sarah Family",
        "travel_style": "budget",
        "user_preferences": {
            "hotel_rating_min": 3.5,
            "amenities": ["pool", "family rooms", "breakfast included"],
            "location": "Near beach"
        },
        "special_requirements": "Children aged 5 and 8, need interconnected rooms",
        "profit_priority": True
    }
    
    print("\nRequest Payload:")
    print(json.dumps(payload, indent=2))
    
    print("\nSending request to /recommend/travel-plan...")
    try:
        response = requests.post(
            f"{BASE_URL}/recommend/travel-plan",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ RESPONSE RECEIVED")
            print(f"Status: {data.get('status')}")
            
            # Show hotel options
            hotels = data.get('hotel_options', [])
            print(f"\n🏨 Available Hotels ({len(hotels)}):")
            for i, hotel in enumerate(hotels[:3], 1):
                profit = hotel.get('profit_potential', {})
                print(f"  {i}. {hotel.get('name')}")
                print(f"     Rating: {hotel.get('rating')}/5")
                print(f"     Price: ${hotel.get('price_per_night')}/night")
                print(f"     Platform Profit: ${profit.get('total_profit', 0):.2f}")
            
            print("\n🎯 BEST RECOMMENDATION:")
            rec = data.get('recommendation', {})
            print(f"  Hotel: {rec.get('hotel', {}).get('name')}")
            print(f"  Total Trip Cost: ${rec.get('total_package_cost', 0):.2f}")
            print(f"  Platform Profit: ${rec.get('platform_profit', 0):.2f}")
            
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_3_adventure_travel():
    """
    Example 3: Adventure Travel to Bali
    Experience-focused, moderate budget, unique options
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: ADVENTURE TRAVEL TO BALI")
    print("="*80)
    
    payload = {
        "origin": "Singapore (SIN)",
        "destination": "Bali, Indonesia",
        "check_in": "2026-05-10",
        "check_out": "2026-05-17",
        "passengers": 2,
        "budget": 3000,
        "user_id": "user_adventure_001",
        "user_name": "Alex Adventure",
        "travel_style": "adventure",
        "user_preferences": {
            "hotel_rating_min": 4.0,
            "amenities": ["gym", "wifi", "adventure planning"],
            "location": "Ubud or beach area"
        },
        "special_requirements": "Need sports equipment rental nearby",
        "profit_priority": True,
        "business_rules": {
            "markup_percentage": 18,
            "preferred_partners": ["Local boutique hotels", "Budget airlines"],
            "bundle_discount": 8
        }
    }
    
    print("\nSending request to /recommend/travel-plan...")
    try:
        response = requests.post(
            f"{BASE_URL}/recommend/travel-plan",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ RECOMMENDATION SUCCESSFUL")
            
            # Complete journey info
            journey = data.get('complete_journey', {})
            print("\n🗺️  COMPLETE JOURNEY:")
            print(f"  Destination: {journey.get('destination')}")
            print(f"  Duration: {journey.get('duration_days')} days")
            print(f"  Hotel: {journey.get('hotel')}")
            print(f"  Total Cost: ${journey.get('estimated_total_cost', 0):.2f}")
            
            # ROI
            roi = data.get('roi_analysis', {})
            print("\n📊 BUSINESS METRICS:")
            print(f"  Revenue: ${roi.get('total_revenue', 0):.2f}")
            print(f"  Platform Profit: ${roi.get('platform_profit', 0):.2f}")
            print(f"  Margin: {roi.get('profit_margin', 0):.1f}%")
            
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def example_4_corporate_retreat():
    """
    Example 4: Corporate Team Retreat to Switzerland
    Multiple rooms, custom business rules, high profit potential
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: CORPORATE TEAM RETREAT TO SWITZERLAND")
    print("="*80)
    
    payload = {
        "origin": "London (LHR)",
        "destination": "Zurich, Switzerland",
        "check_in": "2026-06-01",
        "check_out": "2026-06-05",
        "passengers": 10,  # Team of 10
        "budget": 15000,  # Total budget
        "user_id": "corp_retreat_001",
        "user_name": "TechCorp Inc",
        "travel_style": "business",
        "user_preferences": {
            "hotel_rating_min": 4.5,
            "amenities": ["conference rooms", "team activities", "executive lounge"],
            "location": "Zurich city center"
        },
        "special_requirements": "Need 10 rooms, conference facilities for 3 days, team building activities",
        "profit_priority": True,
        "business_rules": {
            "markup_percentage": 22,
            "min_commission": 100,
            "preferred_partners": ["5-star chains", "Swiss airlines"],
            "bundle_discount": 10,
            "loyalty_multiplier": 1.5,
            "group_bonus": 0.08
        }
    }
    
    print("\nSending request to /recommend/travel-plan...")
    try:
        response = requests.post(
            f"{BASE_URL}/recommend/travel-plan",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n✅ CORPORATE RETREAT RECOMMENDED")
            
            rec = data.get('recommendation', {})
            print(f"\n🏆 SELECTED OPTION:")
            print(f"  Hotel: {rec.get('hotel', {}).get('name')}")
            print(f"  Group Size: 10 people")
            print(f"  Duration: 4 nights")
            print(f"  Total Trip Cost: ${rec.get('total_package_cost', 0):.2f}")
            print(f"  Cost Per Person: ${rec.get('total_package_cost', 0) / 10:.2f}")
            
            profit = data.get('profit_metrics', {})
            print(f"\n💰 PROFITABILITY:")
            print(f"  Total Revenue: ${profit.get('total_revenue', 0):.2f}")
            print(f"  Platform Profit: ${profit.get('platform_profit', 0):.2f}")
            print(f"  Profit per Person: ${profit.get('platform_profit', 0) / 10:.2f}")
            print(f"  Profit Margin: {profit.get('profit_margin_percentage', 0):.1f}%")
            
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def show_menu():
    """Display example menu"""
    print("\n" + "="*80)
    print("TRAVEL RECOMMENDATION API - EXAMPLE SCENARIOS")
    print("="*80)
    print("\n1. Luxury Business Trip (Paris)")
    print("2. Budget Family Vacation (Barcelona)")
    print("3. Adventure Travel (Bali)")
    print("4. Corporate Retreat (Switzerland)")
    print("5. Custom Request")
    print("0. Exit")
    print("\n" + "="*80)


if __name__ == "__main__":
    print("\n🌍 Travel Recommendation API Examples")
    print("Make sure services are running on localhost:8000\n")
    
    while True:
        show_menu()
        choice = input("\nSelect example (0-5): ").strip()
        
        if choice == "1":
            example_1_luxury_business_trip()
        elif choice == "2":
            example_2_budget_family_vacation()
        elif choice == "3":
            example_3_adventure_travel()
        elif choice == "4":
            example_4_corporate_retreat()
        elif choice == "5":
            print("\nEnter custom payload (JSON format):")
            try:
                payload = json.loads(input())
                response = requests.post(
                    f"{BASE_URL}/recommend/travel-plan",
                    json=payload,
                    timeout=60
                )
                if response.status_code == 200:
                    format_response(response.json())
                else:
                    print(f"Error: {response.status_code}\n{response.text}")
            except json.JSONDecodeError:
                print("Invalid JSON format")
            except Exception as e:
                print(f"Error: {str(e)}")
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice")
        
        input("\nPress Enter to continue...")
