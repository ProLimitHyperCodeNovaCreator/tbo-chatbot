"""
Mock database for testing without PostgreSQL
"""
from datetime import datetime
from typing import Optional, List, Dict, Any


class MockUserProfile:
    def __init__(self, **kwargs):
        self.user_id = kwargs.get('user_id')
        self.agency_id = kwargs.get('agency_id')
        self.budget_pref = kwargs.get('budget_pref')
        self.refund_pref = kwargs.get('refund_pref')
        self.preferred_suppliers = kwargs.get('preferred_suppliers', [])
        self.frequent_routes = kwargs.get('frequent_routes', {})
        self.language_pref = kwargs.get('language_pref')
        self.last_active_at = kwargs.get('last_active_at')


class MockBookingStats:
    def __init__(self, **kwargs):
        self.agency_id = kwargs.get('agency_id')
        self.avg_booking_value = kwargs.get('avg_booking_value', 0.0)
        self.cancellation_rate = kwargs.get('cancellation_rate', 0.0)
        self.conversion_rate = kwargs.get('conversion_rate', 0.0)
        self.top_destinations = kwargs.get('top_destinations', [])
        self.updated_at = kwargs.get('updated_at')


class MockDB:
    """Mock database with in-memory data"""
    
    def __init__(self):
        self.connected = False
        self._personalization_scores = []
        self._training_events = []
        self._setup_data()
    
    def _setup_data(self):
        """Initialize mock data"""
        self.users = {
            "sample-user-1": MockUserProfile(
                user_id="sample-user-1",
                agency_id="agency-1",
                budget_pref="mid",
                refund_pref="high",
                preferred_suppliers=["supplier-1", "supplier-2"],
                frequent_routes={"routes": ["NYC-LAX", "SFO-NYC"]},
                language_pref="en",
                last_active_at=datetime.utcnow()
            ),
            "test-user-1": MockUserProfile(
                user_id="test-user-1",
                agency_id="agency-2",
                budget_pref="low",
                refund_pref="low",
                preferred_suppliers=["supplier-3"],
                frequent_routes={"routes": ["BOS-LAX"]},
                language_pref="en",
                last_active_at=datetime.utcnow()
            ),
            "test-user-2": MockUserProfile(
                user_id="test-user-2",
                agency_id="agency-1",
                budget_pref="high",
                refund_pref="high",
                preferred_suppliers=["supplier-1", "supplier-4"],
                frequent_routes={"routes": ["NYC-LHR"]},
                language_pref="en",
                last_active_at=datetime.utcnow()
            )
        }
        
        self.stats = {
            "agency-1": MockBookingStats(
                agency_id="agency-1",
                avg_booking_value=500.0,
                cancellation_rate=0.35,  # High cancellation rate
                conversion_rate=0.25,
                top_destinations=["LAX", "NYC", "LHR"],
                updated_at=datetime.utcnow()
            ),
            "agency-2": MockBookingStats(
                agency_id="agency-2",
                avg_booking_value=300.0,
                cancellation_rate=0.15,
                conversion_rate=0.08,  # Low conversion rate
                top_destinations=["LAX", "SFO"],
                updated_at=datetime.utcnow()
            )
        }
    
    async def connect(self):
        """Mock connect"""
        self.connected = True
        print("✓ Mock database connected")
    
    async def disconnect(self):
        """Mock disconnect"""
        self.connected = False
        print("✓ Mock database disconnected")
    
    async def query_raw(self, query: str):
        """Mock raw query"""
        return [{"result": 1}]
    
    class UserProfileQuery:
        def __init__(self, db):
            self.db = db
        
        async def find_unique(self, where: Dict):
            user_id = where.get("user_id")
            return self.db.users.get(user_id)
    
    class BookingStatsQuery:
        def __init__(self, db):
            self.db = db
        
        async def find_unique(self, where: Dict):
            agency_id = where.get("agency_id")
            return self.db.stats.get(agency_id)
    
    class PersonalizationScoresQuery:
        def __init__(self, db):
            self.db = db
        
        async def upsert(self, where: Dict, data: Dict):
            score_data = {
                **where.get("user_id_option_id", {}),
                **data.get("create", {})
            }
            self.db.personalization_scores.append(score_data)
            return score_data
    
    class TrainingEventsQuery:
        def __init__(self, db):
            self.db = db
        
        async def create(self, data: Dict):
            event = {**data, "event_id": f"event-{len(self.db._training_events)}"}
            self.db._training_events.append(event)
            return type('obj', (object,), event)
        
        async def find_many(self):
            # Return mock training events for model training
            events = []
            for i in range(150):
                event = type('obj', (object,), {
                    'user_id': 'sample-user-1',
                    'option_id': f'opt-{i}',
                    'price_bucket': ['low', 'mid', 'high'][i % 3],
                    'distance_bucket': ['near', 'mid', 'far'][i % 3],
                    'rating_bucket': ['low', 'mid', 'high'][i % 3],
                    'supplier_id': f'supplier-{(i % 3) + 1}',
                    'refundable': i % 2 == 0,
                    'accepted': i % 3 == 0,
                })
                events.append(event)
            return events
    
    @property
    def user_profile(self):
        return self.UserProfileQuery(self)
    
    @property
    def booking_stats(self):
        return self.BookingStatsQuery(self)
    
    @property
    def personalization_scores(self):
        return self.PersonalizationScoresQuery(self)
    
    @property
    def training_events(self):
        return self.TrainingEventsQuery(self)


# Global mock database instance
mock_db = MockDB()
