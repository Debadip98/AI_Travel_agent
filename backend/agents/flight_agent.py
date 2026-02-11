"""Flight booking agent"""
from .base_agent import BaseAgent
from typing import Dict, Any, List
import json


class FlightAgent(BaseAgent):
    """Agent for flight search and booking"""
    
    def __init__(self):
        super().__init__(
            name="Flight Booking Agent",
            description="Search and book flight tickets at different price tiers"
        )
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process flight booking request
        
        Example inputs:
        - "Find me the cheapest flight from NYC to Paris on Jan 15"
        - "I want a luxury flight, price doesn't matter"
        - "Show me moderate flights for Feb trip"
        """
        
        intent = self._extract_intent(user_input)
        
        if intent != "flight":
            return self._format_response("error", {"message": "Not a flight query"})
        
        # Parse location and dates from user input
        parsed = self._parse_flight_request(user_input, context)
        
        if not parsed:
            return self._format_response("pending", {
                "message": "Need more details",
                "required": ["from_city", "to_city", "departure_date", "budget_tier"]
            })
        
        # Get preferences
        budget_tier = context.get("preferences", {}).get("budget_tier", "moderate")
        
        # Search flights
        flights = self._search_flights(
            parsed["from"],
            parsed["to"],
            parsed["departure_date"],
            parsed.get("return_date"),
            budget_tier
        )
        
        if not flights:
            return self._format_response("error", {
                "message": f"No flights found for {parsed['from']} to {parsed['to']}"
            })
        
        return self._format_response("success", {
            "flights": flights,
            "count": len(flights),
            "budget_tier": budget_tier,
            "total_options": len(flights)
        }, confidence=0.85)
    
    def _parse_flight_request(self, text: str, context: Dict) -> Dict[str, Any]:
        """Extract flight details from user input"""
        # TODO: Implement advanced NLP parsing
        # For now, return placeholder
        return {
            "from": "NYC",
            "to": "Paris",
            "departure_date": "2024-06-15",
            "return_date": "2024-06-22"
        }
    
    def _search_flights(self, origin: str, destination: str, 
                       departure_date: str, return_date: str = None,
                       budget_tier: str = "moderate") -> List[Dict]:
        """Search flights based on tier"""
        
        from integrations.apis import flight_api
        
        try:
            # Try to fetch from real API
            flights = flight_api.search_flights(origin, destination, departure_date, return_date)
            
            if flights:
                # Sort and filter by tier
                return self._filter_by_tier(flights, budget_tier)
        except Exception as e:
            # Fall back to mock data
            print(f"FlightAPI error: {e}. Using mock data...")
        
        # Mock data for testing
        flights = [
            {
                "id": "FL001",
                "airline": "Budget Air",
                "departure": f"{departure_date} 08:00",
                "arrival": f"{departure_date} 16:30",
                "duration": "8h 30m",
                "stops": 1,
                "price": 150,
                "tier": "cheap",
                "baggage": "1x carry-on",
                "seat_class": "economy",
                "rating": 3.8
            },
            {
                "id": "FL002",
                "airline": "Standard Airlines",
                "departure": f"{departure_date} 10:00",
                "arrival": f"{departure_date} 18:00",
                "duration": "8h",
                "stops": 0,
                "price": 350,
                "tier": "moderate",
                "baggage": "1x checked, 2x carry-on",
                "seat_class": "economy",
                "rating": 4.2
            },
            {
                "id": "FL003",
                "airline": "Premium Airlines",
                "departure": f"{departure_date} 11:00",
                "arrival": f"{departure_date} 19:00",
                "duration": "8h",
                "stops": 0,
                "price": 800,
                "tier": "luxury",
                "baggage": "2x checked, unlimited carry-on",
                "seat_class": "business",
                "lounge_access": True,
                "rating": 4.8
            }
        ]
        
        # Filter by tier
        return self._filter_by_tier(flights, budget_tier)
    
    def _filter_by_tier(self, flights: List[Dict], budget_tier: str) -> List[Dict]:
        """Filter flights by budget tier"""
        if budget_tier == "cheap":
            return sorted([f for f in flights if f.get("tier") == "cheap"], 
                         key=lambda x: x.get("price", 0))
        elif budget_tier == "luxury":
            return sorted([f for f in flights if f.get("tier") == "luxury"], 
                         key=lambda x: x.get("price", float('inf')), reverse=True)
        else:
            return sorted(flights, key=lambda x: x.get("price", 0))
