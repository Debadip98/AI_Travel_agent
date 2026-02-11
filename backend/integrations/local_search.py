"""Local search and utilities"""
import requests
from typing import List, Dict, Any
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


class LocalSearchManager:
    """Search for local services and optimize stay locations"""
    
    def __init__(self):
        self.geocoder = Nominatim(user_agent="travel_agent")
        self.budget_keywords = {
            "grocery": ["supermarket", "market", "convenience store", "farmer's market"],
            "food": ["restaurant", "cafe", "food court", "diner"],
            "pharmacy": ["pharmacy", "drugstore", "medical clinic"],
            "transport": ["bus station", "train station", "metro", "tram"],
            "cheap_stay": ["hostel", "budget hotel", "guesthouse", "airbnb"]
        }
    
    def find_locations(self, city: str, search_type: str, 
                       limit: int = 5) -> List[Dict]:
        """
        Find locations for a specific category
        
        Args:
            city: City name
            search_type: Type of location (grocery, food, pharmacy, etc.)
            limit: Number of results
        """
        try:
            # TODO: Use Overpass API or Google Maps for actual searches
            # For now return mock data
            return self._mock_locations(city, search_type, limit)
        except Exception as e:
            print(f"Local search error: {e}")
            return []
    
    def _mock_locations(self, city: str, search_type: str, 
                       limit: int) -> List[Dict]:
        """Return mock location data"""
        locations = []
        
        keywords = self.budget_keywords.get(search_type, [search_type])
        
        for i in range(limit):
            locations.append({
                "id": f"LOC{search_type}{i}",
                "name": f"{keywords[i % len(keywords)].title()} {i+1}",
                "city": city,
                "type": search_type,
                "distance": f"{0.5 + i*0.3} km",
                "rating": 4.0 + (i*0.1),
                "open_hours": "9am-9pm"
            })
        
        return locations
    
    def estimate_daily_cost(self, city: str, budget_tier: str = "moderate",
                           travelers: int = 1) -> Dict[str, float]:
        """Estimate daily costs for a city"""
        # Budget estimates (in USD)
        cost_matrix = {
            "cheap": {
                "accommodation": 15,
                "food": 10,
                "transport": 5,
                "activities": 5,
                "total": 35
            },
            "moderate": {
                "accommodation": 40,
                "food": 25,
                "transport": 10,
                "activities": 20,
                "total": 95
            },
            "luxury": {
                "accommodation": 150,
                "food": 80,
                "transport": 30,
                "activities": 100,
                "total": 360
            }
        }
        
        tier_costs = cost_matrix.get(budget_tier, cost_matrix["moderate"])
        
        return {
            **tier_costs,
            "per_person": tier_costs["total"] // travelers
        }
    
    def find_near_station(self, city: str, station_type: str = "train",
                         accommodation_type: str = "budget") -> List[Dict]:
        """Find budget accommodations near stations"""
        # TODO: Implement with Google Maps Nearby Search
        return self._mock_locations(city, "cheap_stay", 5)
    
    def get_discount_times(self, city: str, business_type: str = "restaurant") -> List[Dict]:
        """Get discount/happy hour times for businesses"""
        return [
            {
                "business_type": business_type,
                "discount": "20-30% off",
                "time": "5pm-7pm",
                "days": ["Monday", "Tuesday", "Wednesday", "Thursday"]
            }
        ]


local_search = LocalSearchManager()
