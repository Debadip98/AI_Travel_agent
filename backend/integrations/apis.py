"""Flight API integration"""
import requests
from typing import Dict, List, Any
from config.settings import Config


class FlightAPI:
    """Amadeus and Skyscanner flight API integration"""
    
    def __init__(self):
        self.amadeus_key = Config.AMADEUS_API_KEY
        self.skyscanner_key = Config.SKYSCANNER_API_KEY
        self.amadeus_base_url = "https://api.amadeus.com/v2"
        self.skyscanner_base_url = "https://rapidapi.com/skyscanner"
    
    def search_flights(self, origin: str, destination: str, 
                      departure_date: str, return_date: str = None) -> List[Dict]:
        """
        Search flights using Amadeus API
        
        Args:
            origin: IATA code (e.g., 'NYC')
            destination: IATA code (e.g., 'PAR')
            departure_date: ISO format date
            return_date: Optional return date
            
        Returns:
            List of flight options
        """
        try:
            if not self.amadeus_key:
                # Fall back to mock data
                return self._mock_flights(origin, destination)
            
            # Real Amadeus API call
            headers = {
                "Authorization": f"Bearer {self._get_amadeus_token()}",
                "Content-Type": "application/json"
            }
            
            params = {
                "originLocationCode": origin.upper(),
                "destinationLocationCode": destination.upper(),
                "departureDate": departure_date,
                "adults": "1",
                "max": "10"
            }
            
            response = requests.get(
                f"{self.amadeus_base_url}/shopping/flight-offers",
                headers=headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_flights(data.get("data", []))
            else:
                print(f"Amadeus API error: {response.status_code}")
                return self._mock_flights(origin, destination)
                
        except Exception as e:
            print(f"Flight API error: {e}")
            return self._mock_flights(origin, destination)
    
    def _get_amadeus_token(self) -> str:
        """Get Amadeus authentication token"""
        try:
            auth_url = f"https://test.api.amadeus.com/v1/security/oauth2/token"
            auth_data = {
                "grant_type": "client_credentials",
                "client_id": self.amadeus_key,
                "client_secret": getattr(self, 'amadeus_secret', '')
            }
            response = requests.post(auth_url, data=auth_data, timeout=5)
            if response.status_code == 200:
                return response.json().get("access_token", "")
        except:
            pass
        return "dummy_token"  # Fallback token
    
    def _parse_flights(self, flights_data: List[Dict]) -> List[Dict]:
        """Parse Amadeus API response"""
        parsed = []
        for flight in flights_data[:5]:  # Limit to 5 results
            try:
                itineraries = flight.get("itineraries", [{}])[0]
                segments = itineraries.get("segments", [{}])
                price = flight.get("price", {})
                
                parsed.append({
                    "id": flight.get("id"),
                    "price": float(price.get("total", 500)),
                    "currency": price.get("currency", "USD"),
                    "duration": itineraries.get("duration", "N/A"),
                    "stops": len(segments) - 1,
                    "departure": segments[0].get("departure", {}).get("at", "N/A"),
                    "arrival": segments[-1].get("arrival", {}).get("at", "N/A"),
                    "airline": segments[0].get("operating", {}).get("carrierCode", "N/A"),
                    "seat_class": "economy",
                    "rating": 4.0 + (len(parsed) * 0.1)
                })
            except (KeyError, IndexError, ValueError):
                continue
        
        return parsed if parsed else self._mock_flights("", "")
    
    def _mock_flights(self, origin: str, destination: str) -> List[Dict]:
        """Return mock flight data for testing"""
        return [
            {
                "id": "AM1001",
                "airline": "Airline {origin}-{destination}",
                "price": 250,
                "departure": "10:00",
                "arrival": "18:30",
                "duration": "8h 30m",
                "stops": 0
            }
        ]


class HotelAPI:
    """Hotel booking API integration"""
    
    def __init__(self):
        self.booking_api_key = Config.GOOGLE_MAPS_API_KEY  # Use Google for now
    
    def search_hotels(self, city: str, check_in: str, 
                     check_out: str, guests: int = 1) -> List[Dict]:
        """Search hotels in a city"""
        try:
            # TODO: Integrate with Booking.com or Hotels.com API
            return self._mock_hotels(city)
        except Exception as e:
            print(f"Hotel API error: {e}")
            return []
    
    def _mock_hotels(self, city: str) -> List[Dict]:
        """Return mock hotel data"""
        return [
            {
                "id": "HOT001",
                "name": f"Hotel {city}",
                "price": 120,
                "rating": 4.5,
                "distance_to_center": "1.2 km"
            }
        ]


class TransportAPI:
    """Train and ferry booking API"""
    
    def __init__(self):
        self.rome2rio_key = Config.AMADEUS_API_KEY  # Placeholder
    
    def search_trains(self, origin: str, destination: str, 
                     departure_date: str) -> List[Dict]:
        """Search train routes"""
        try:
            # TODO: Integrate with national rail APIs
            return self._mock_trains(origin, destination)
        except Exception as e:
            print(f"Train API error: {e}")
            return []
    
    def _mock_trains(self, origin: str, destination: str) -> List[Dict]:
        """Return mock train data"""
        return [
            {
                "id": "TR001",
                "provider": "National Railways",
                "departure": "14:00",
                "arrival": "22:00",
                "duration": "8h",
                "price": 80,
                "type": "express"
            }
        ]


class PlacesAPI:
    """Google Maps and Foursquare integration"""
    
    def __init__(self):
        self.google_key = Config.GOOGLE_MAPS_API_KEY
        self.foursquare_key = Config.FOURSQUARE_API_KEY
    
    def search_places(self, query: str, location: str, 
                     place_type: str = None) -> List[Dict]:
        """
        Search places (restaurants, shops, attractions)
        
        Args:
            query: Search query (e.g., 'grocery store')
            location: City or coordinates
            place_type: Optional category filter
        """
        try:
            # TODO: Implement Google Maps Places API
            return self._mock_places(query, location)
        except Exception as e:
            print(f"Places API error: {e}")
            return []
    
    def _mock_places(self, query: str, location: str) -> List[Dict]:
        """Return mock places data"""
        return [
            {
                "id": "PL001",
                "name": f"{query} in {location}",
                "rating": 4.2,
                "address": "123 Main St",
                "type": query,
                "distance": "0.5 km"
            }
        ]
    
    def get_directions(self, origin: str, destination: str, 
                      mode: str = "transit") -> Dict[str, Any]:
        """Get directions between two points"""
        try:
            # TODO: Implement Google Maps Directions API
            return {
                "distance": "5.2 km",
                "duration": "15 mins",
                "mode": mode,
                "steps": []
            }
        except Exception as e:
            print(f"Directions API error: {e}")
            return {}


class VisaAPI:
    """Visa requirements and travel restrictions API"""
    
    def __init__(self):
        self.sherpa_key = Config.SHERPA_API_KEY
    
    def get_visa_requirements(self, destination: str, 
                             nationality: str) -> Dict[str, Any]:
        """Get visa requirements for a destination"""
        try:
            # TODO: Integrate with Sherpa Travel API
            return self._mock_visa_data(destination)
        except Exception as e:
            print(f"Visa API error: {e}")
            return {}
    
    def _mock_visa_data(self, destination: str) -> Dict[str, Any]:
        """Return mock visa data"""
        return {
            "destination": destination,
            "visa_required": True,
            "processing_days": 15,
            "fee": 80,
            "documents": ["passport", "photo", "bank statement"]
        }


# Initialize API clients
flight_api = FlightAPI()
hotel_api = HotelAPI()
transport_api = TransportAPI()
places_api = PlacesAPI()
visa_api = VisaAPI()
