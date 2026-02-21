#!/usr/bin/env python3
"""
Setup script for initializing the database with sample data
"""
import asyncio
from datetime import datetime
from prisma import Prisma

async def setup_database():
    db = Prisma()
    await db.connect()
    
    print("Setting up database with sample data...")
    
    # Create sample user profile
    user = await db.user_profile.upsert(
        where={"user_id": "sample-user-1"},
        data={
            "create": {
                "user_id": "sample-user-1",
                "agency_id": "agency-1",
                "budget_pref": "mid",
                "refund_pref": "high",
                "preferred_suppliers": ["supplier-1", "supplier-2"],
                "frequent_routes": {"routes": ["NYC-LAX", "SFO-NYC"]},
                "language_pref": "en",
                "last_active_at": datetime.utcnow()
            },
            "update": {}
        }
    )
    print(f"✓ Created user profile: {user.user_id}")
    
    # Create sample booking stats
    stats = await db.booking_stats.upsert(
        where={"agency_id": "agency-1"},
        data={
            "create": {
                "agency_id": "agency-1",
                "avg_booking_value": 500.0,
                "cancellation_rate": 0.15,
                "conversion_rate": 0.25,
                "top_destinations": ["LAX", "NYC", "LHR"],
                "updated_at": datetime.utcnow()
            },
            "update": {
                "avg_booking_value": 500.0,
                "cancellation_rate": 0.15,
                "conversion_rate": 0.25,
                "top_destinations": ["LAX", "NYC", "LHR"],
                "updated_at": datetime.utcnow()
            }
        }
    )
    print(f"✓ Created booking stats for agency: {stats.agency_id}")
    
    # Create sample preference rules
    rules_data = [
        {
            "rule_id": "rule-1",
            "scope": "global",
            "condition": "high_cancellation_rate",
            "boost_type": "refundable",
            "boost_weight": 0.2,
            "reason": "Prefers refundable options",
            "active": True
        },
        {
            "rule_id": "rule-2",
            "scope": "user",
            "condition": "budget_match",
            "boost_type": "price_bucket",
            "boost_weight": 0.15,
            "reason": "Matches budget preference",
            "active": True
        }
    ]
    
    for rule_data in rules_data:
        rule = await db.preference_rules.upsert(
            where={"rule_id": rule_data["rule_id"]},
            data={
                "create": rule_data,
                "update": rule_data
            }
        )
        print(f"✓ Created rule: {rule.rule_id}")
    
    # Create sample training events for model training
    training_events = [
        {
            "user_id": "sample-user-1",
            "option_id": f"opt-{i}",
            "price_bucket": ["low", "mid", "high"][i % 3],
            "distance_bucket": ["near", "mid", "far"][i % 3],
            "rating_bucket": ["low", "mid", "high"][i % 3],
            "supplier_id": f"supplier-{(i % 3) + 1}",
            "refundable": i % 2 == 0,
            "accepted": i % 3 == 0,  # 33% acceptance rate
            "created_at": datetime.utcnow()
        }
        for i in range(150)  # Create 150 samples for training
    ]
    
    for event_data in training_events:
        await db.training_events.create(data=event_data)
    
    print(f"✓ Created {len(training_events)} training events")
    
    await db.disconnect()
    print("\n✅ Database setup complete!")
    print("\nYou can now:")
    print("1. Start the server: python -m uvicorn app.main:app --reload")
    print("2. Train the model: curl -X POST http://localhost:8000/train")
    print("3. Test personalization: curl -X POST http://localhost:8000/personalize")

if __name__ == "__main__":
    asyncio.run(setup_database())
