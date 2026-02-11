"""Database models for Travel Agent Application"""
from datetime import datetime, timedelta
from typing import Optional, List
import json

# Note: Full implementation requires SQLAlchemy
# This is a template structure for database models

class UserModel:
    """User account model"""
    
    def __init__(self, email: str, password_hash: str, full_name: str):
        self.id = None  # Auto-generated
        self.email = email
        self.password_hash = password_hash
        self.full_name = full_name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.is_active = True
        self.profile_picture = None
        self.phone_number = None
        self.country_of_residence = None
        self.preferred_language = "en"
        self.travel_preferences = {}  # JSON: budget, pace, interests, etc.
        
        # Social features
        self.trips = []  # List of Trip IDs
        self.friends = []  # List of Friend IDs
        self.saved_itineraries = []  # List of Itinerary IDs
        
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
            "profile_picture": self.profile_picture,
            "phone_number": self.phone_number,
            "country_of_residence": self.country_of_residence,
            "preferred_language": self.preferred_language,
            "travel_preferences": self.travel_preferences
        }


class TripModel:
    """Trip planning model"""
    
    def __init__(self, user_id: int, destination: str, start_date: datetime, end_date: datetime):
        self.id = None  # Auto-generated
        self.user_id = user_id
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.status = "planning"  # planning, booked, completed, cancelled
        
        # Trip details
        self.title = f"Trip to {destination}"
        self.description = ""
        self.traveler_count = 1
        self.travelers = []  # List of Traveler objects
        self.budget_total = 0
        self.budget_spent = 0
        self.currency = "USD"
        
        # Budget breakdown
        self.budget_breakdown = {
            "flights": 0,
            "accommodation": 0,
            "activities": 0,
            "food": 0,
            "transport": 0,
            "other": 0
        }
        
        # Components
        self.flights = []  # Flight IDs
        self.accommodations = []  # Hotel IDs
        self.activities = []  # Activity IDs
        self.itineraries = []  # Itinerary IDs
        self.transport_bookings = []  # Transport reservation IDs
        self.documents = []  # Visa, insurance, etc
        
        # Sharing & collaboration
        self.is_shared = False
        self.shared_with = []  # User IDs
        self.collaborators = []  # User IDs
        
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "destination": self.destination,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "duration_days": self.duration_days(),
            "title": self.title,
            "status": self.status,
            "budget_total": self.budget_total,
            "budget_spent": self.budget_spent,
            "currency": self.currency,
            "traveler_count": self.traveler_count
        }


class FlightBookingModel:
    """Flight booking model"""
    
    def __init__(self, trip_id: int, departure: str, arrival: str):
        self.id = None  # Auto-generated
        self.trip_id = trip_id
        self.departure_city = departure
        self.arrival_city = arrival
        self.created_at = datetime.utcnow()
        self.booking_date = None
        self.status = "searching"  # searching, selected, booked, completed, cancelled
        
        # Flight details
        self.outbound_flight = None  # Flight data
        self.return_flight = None  # Flight data
        self.airline = None
        self.total_price = 0
        self.currency = "USD"
        self.passengers = []  # Passenger details
        self.seat_selections = {}  # Seat class: economy, business, first
        
        # Booking reference
        self.confirmation_number = None
        self.booking_reference = None
        self.tickets = []
        
    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "from": self.departure_city,
            "to": self.arrival_city,
            "status": self.status,
            "airline": self.airline,
            "price": self.total_price,
            "currency": self.currency,
            "confirmation": self.confirmation_number
        }


class AccommodationModel:
    """Hotel/Accommodation booking model"""
    
    def __init__(self, trip_id: int, destination: str, check_in: datetime):
        self.id = None
        self.trip_id = trip_id
        self.destination = destination
        self.check_in = check_in
        self.check_out = None
        self.created_at = datetime.utcnow()
        self.status = "searching"  # searching, selected, booked, checked-in, completed
        
        # Hotel details
        self.name = None
        self.address = None
        self.rating = None  # 1-5 stars
        self.reviews_count = 0
        self.amenities = []  # WiFi, Pool, Gym, etc.
        self.room_type = None  # Single, Double, Suite, etc.
        self.nights = 0
        self.nightly_rate = 0
        self.total_price = 0
        self.currency = "USD"
        
        # Contact
        self.phone = None
        self.email = None
        self.website = None
        
        # Booking
        self.confirmation_number = None
        self.payment_status = "pending"
        self.notes = ""
        
    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "destination": self.destination,
            "name": self.name,
            "check_in": self.check_in.isoformat(),
            "check_out": self.check_out.isoformat() if self.check_out else None,
            "nights": self.nights,
            "total_price": self.total_price,
            "currency": self.currency,
            "status": self.status,
            "rating": self.rating
        }


class VisaDocumentModel:
    """Visa application tracking model"""
    
    def __init__(self, trip_id: int, destination: str, user_id: int):
        self.id = None
        self.trip_id = trip_id
        self.user_id = user_id
        self.destination = destination
        self.created_at = datetime.utcnow()
        self.status = "not_started"  # not_started, in_progress, submitted, approved, rejected
        
        # Visa details
        self.visa_type = None
        self.processing_days = 0
        self.visa_fee = 0
        self.currency = "USD"
        
        # Checklist
        self.documents = []  # Document checklist items
        self.submission_date = None
        self.approval_date = None
        self.visa_number = None
        self.validity_start = None
        self.validity_end = None
        
        # Documents uploaded
        self.uploaded_files = []  # File paths
        self.application_form_url = None
        
    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "destination": self.destination,
            "visa_type": self.visa_type,
            "status": self.status,
            "processing_days": self.processing_days,
            "visa_fee": self.visa_fee,
            "currency": self.currency,
            "approval_date": self.approval_date.isoformat() if self.approval_date else None
        }


class ActivityModel:
    """Activity/Experience booking model"""
    
    def __init__(self, trip_id: int, activity_name: str, date: datetime):
        self.id = None
        self.trip_id = trip_id
        self.name = activity_name
        self.date = date
        self.created_at = datetime.utcnow()
        self.status = "pending"  # pending, booked, completed, cancelled
        
        # Activity details
        self.description = ""
        self.category = None  # Tour, Museum, Adventure, Food, etc.
        self.location = None
        self.duration_hours = 0
        self.start_time = None
        self.end_time = None
        self.price_per_person = 0
        self.participants = 1
        self.total_price = 0
        self.currency = "USD"
        
        # Provider
        self.provider_name = None
        self.provider_rating = None
        self.cancellation_policy = None
        
        # Booking
        self.confirmation_number = None
        self.ticket_url = None
        
    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "name": self.name,
            "date": self.date.isoformat(),
            "category": self.category,
            "duration": self.duration_hours,
            "price": self.total_price,
            "currency": self.currency,
            "status": self.status,
            "provider": self.provider_name
        }


class ItineraryModel:
    """Day-by-day itinerary model"""
    
    def __init__(self, trip_id: int, day_number: int, date: datetime):
        self.id = None
        self.trip_id = trip_id
        self.day_number = day_number
        self.date = date
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Daily schedule
        self.title = None  # Day title/theme
        self.description = None
        self.activities = []  # Activity IDs for this day
        self.meals = {}  # breakfast, lunch, dinner
        self.accommodation = None  # Hotel ID
        self.transport = None  # Transport booking
        
        # Time slots
        self.schedule = []  # List of {time, activity, notes}
        
        # Notes
        self.notes = ""
        self.highlights = []
        
    def to_dict(self):
        return {
            "id": self.id,
            "trip_id": self.trip_id,
            "day_number": self.day_number,
            "date": self.date.isoformat(),
            "title": self.title,
            "activities_count": len(self.activities),
            "description": self.description
        }


# Database initialization template
class DatabaseManager:
    """Database connection and operations manager"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.connection = None
        
    def init_db(self):
        """Initialize database connection"""
        # Implementation with SQLAlchemy
        pass
    
    def create_tables(self):
        """Create all database tables"""
        # Implementation with SQLAlchemy
        pass
    
    def close(self):
        """Close database connection"""
        pass
    
    # User operations
    def create_user(self, user: UserModel) -> int:
        """Create new user and return user_id"""
        pass
    
    def get_user(self, user_id: int) -> Optional[UserModel]:
        """Get user by ID"""
        pass
    
    def update_user(self, user: UserModel) -> bool:
        """Update user information"""
        pass
    
    # Trip operations
    def create_trip(self, trip: TripModel) -> int:
        """Create new trip and return trip_id"""
        pass
    
    def get_trips(self, user_id: int) -> List[TripModel]:
        """Get all trips for a user"""
        pass
    
    def get_trip(self, trip_id: int) -> Optional[TripModel]:
        """Get specific trip"""
        pass
    
    def update_trip(self, trip: TripModel) -> bool:
        """Update trip information"""
        pass
    
    # Booking operations
    def create_flight_booking(self, booking: FlightBookingModel) -> int:
        """Create flight booking"""
        pass
    
    def create_accommodation(self, accommodation: AccommodationModel) -> int:
        """Create accommodation booking"""
        pass
    
    def create_activity(self, activity: ActivityModel) -> int:
        """Create activity booking"""
        pass
