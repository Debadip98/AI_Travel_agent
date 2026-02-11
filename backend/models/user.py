from datetime import datetime
from typing import List

class User:
    """User model for travel agent"""
    
    def __init__(self, user_id: str, email: str, name: str = None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.created_at = datetime.now()
        self.preferences = {
            "budget_tier": "moderate",  # cheap, moderate, luxury
            "travel_style": "comfort",  # budget, comfort, luxury
            "currency": "USD",
            "language": "en",
            "dietary_restrictions": []
        }
        self.past_trips: List[dict] = []
        self.saved_documents = {
            "passport": None,
            "visa_docs": [],
            "flight_bookings": [],
            "hotel_bookings": []
        }
        self.gmail_token = None
        self.gmail_refresh_token = None
    
    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "preferences": self.preferences,
            "past_trips": self.past_trips
        }


class Trip:
    """Trip model"""
    
    def __init__(self, trip_id: str, user_id: str, destination: str, 
                 start_date: str, end_date: str, budget: float):
        self.trip_id = trip_id
        self.user_id = user_id
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.budget = budget
        self.created_at = datetime.now()
        self.status = "planning"  # planning, booked, completed, cancelled
        
        # Suggested itinerary & bookings
        self.flights = []
        self.hotels = []
        self.trains = []
        self.activities = []
        self.cost_breakdown = {
            "flights": 0,
            "accommodation": 0,
            "transport": 0,
            "food": 0,
            "activities": 0,
            "other": 0
        }
    
    def to_dict(self) -> dict:
        return {
            "trip_id": self.trip_id,
            "user_id": self.user_id,
            "destination": self.destination,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "status": self.status,
            "flights": self.flights,
            "hotels": self.hotels,
            "trains": self.trains,
            "cost_breakdown": self.cost_breakdown
        }
