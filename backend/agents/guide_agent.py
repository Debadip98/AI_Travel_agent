"""Virtual tour guide agent"""
from .base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime, timedelta


class GuideAgent(BaseAgent):
    """Agent for virtual tour guide and itinerary planning"""
    
    def __init__(self):
        super().__init__(
            name="Virtual Tour Guide",
            description="Provide local recommendations, city guides, and travel tips"
        )
        
        # Comprehensive city guides database with multiple cities
        self.city_guides = {
            "Paris": {
                "country": "France",
                "currency": "EUR",
                "must_see": [
                    {"name": "Eiffel Tower", "duration": "2-3h", "cost": "€15", "time": "morning"},
                    {"name": "Louvre Museum", "duration": "3-4h", "cost": "€17", "time": "afternoon"},
                    {"name": "Notre-Dame", "duration": "1h", "cost": "free", "time": "anytime"},
                    {"name": "Arc de Triomphe", "duration": "1.5h", "cost": "€13", "time": "sunset"},
                    {"name": "Sacré-Cœur", "duration": "1.5h", "cost": "free", "time": "afternoon"},
                    {"name": "Musée d'Orsay", "duration": "2-3h", "cost": "€14", "time": "afternoon"},
                ],
                "local_tips": [
                    "Buy a carnet of 10 metro tickets for €17 (saves 30%)",
                    "Many museums are free on first Sunday of the month",
                    "Avoid eating near tourist spots - go to local bistros on side streets",
                    "Metro runs until 1:15 AM (2:15 AM on Fri-Sat)",
                    "A 'boulangerie' (bakery) on every corner - great for breakfast",
                    "Street markets open Tuesday-Sunday mornings",
                    "Bring wine from supermarket to parks (drinking is allowed)",
                ],
                "scams_to_avoid": [
                    "Gold ring/bracelet giveaway scam around Sacré-Cœur",
                    "Fake police asking to check your wallet for counterfeit money",
                    "Taxi overcharges - use white official taxis or Uber",
                    "Street petition scammers claiming to collect for the deaf",
                    "Inflated prices at tourist restaurants",
                ],
                "best_restaurants": [
                    "L'Ami Jean (Bistro, budget) - Confit de canard",
                    "Frenchie To Go (Casual, budget) - Pulled pork sandwich",
                    "Breizh Café (Crêperie, budget) - Savory crêpes",
                    "Café de Flore (Iconic, luxury) - Crème brûlée"
                ]
            },
            "Tokyo": {
                "country": "Japan",
                "currency": "JPY",
                "must_see": [
                    {"name": "Senso-ji Temple", "duration": "1-1.5h", "cost": "free", "time": "morning"},
                    {"name": "Shibuya Crossing", "duration": "30min", "cost": "free", "time": "evening"},
                    {"name": "Tokyo Tower", "duration": "2h", "cost": "¥900", "time": "afternoon"},
                    {"name": "Meiji Shrine", "duration": "1.5h", "cost": "free", "time": "morning"},
                    {"name": "Harajuku District", "duration": "2-3h", "cost": "free", "time": "afternoon"},
                    {"name": "Tsukiji Market", "duration": "2h", "cost": "variable", "time": "morning"},
                ],
                "local_tips": [
                    "Get a Suica/Pasmo card for unlimited metro use",
                    "JR Pass expensive - buy individual tickets instead",
                    "Convenience stores (7-11, Lawson) have excellent cheap food",
                    "No tipping culture - just pay the bill",
                    "Always remove shoes before entering homes/temples",
                    "Slurp noodles - it's polite and shows appreciation",
                    "Train runs 24 hours on major lines",
                ],
                "scams_to_avoid": [
                    "Roppongi nightclub touts - will overcharge for drinks",
                    "Unlicensed taxis - use only white taxis with licenses",
                    "Tourist shops with inflated prices",
                    "Fake designer goods in back alley shops",
                ],
                "best_restaurants": [
                    "Ichiran Ramen (Ramen, budget) - Tonkotsu ramen",
                    "Tsukiji Outer Market (Sushi, moderate) - Fresh sushi",
                    "Gonpachi (Izakaya, moderate) - Yakitori",
                    "Michelin-starred Nabezo (Luxury) - Sukiyaki"
                ]
            },
            "Bangkok": {
                "country": "Thailand",
                "currency": "THB",
                "must_see": [
                    {"name": "Grand Palace", "duration": "2-3h", "cost": "฿500", "time": "morning"},
                    {"name": "Wat Pho", "duration": "1.5h", "cost": "฿100", "time": "morning"},
                    {"name": "Floating Markets", "duration": "3-4h", "cost": "free+food", "time": "early morning"},
                    {"name": "Chatuchak Market", "duration": "3-4h", "cost": "free", "time": "weekend"},
                    {"name": "Jim Thompson House", "duration": "1.5h", "cost": "฿100", "time": "afternoon"},
                ],
                "local_tips": [
                    "Tuk-tuks are cheap but negotiate prices first",
                    "BTS Skytrain is the fastest way around",
                    "Street food is everywhere and incredibly cheap",
                    "Always show respect to the Thai royal family",
                    "Beware of drinks scams in tourist areas",
                ],
                "scams_to_avoid": [
                    "Gem shop scams - overpriced fakes",
                    "Taxi scams - insist on meter or use Grab app",
                    "Ping pong shows in tourist areas",
                    "Overpriced tuk-tuk tours",
                ],
                "best_restaurants": [
                    "Pad Thai vendors (Street, budget) - Pad Thai ฿30",
                    "Som tam stands (Street, budget) - Som tam ฿40",
                    "Baan Khanit (Local, budget) - Mango chicken",
                    "Gaggan (Fine dining, luxury) - Progressive Indian"
                ]
            },
            "New York": {
                "country": "USA",
                "currency": "USD",
                "must_see": [
                    {"name": "Statue of Liberty", "duration": "3-4h", "cost": "$24", "time": "morning"},
                    {"name": "Central Park", "duration": "2-3h", "cost": "free", "time": "afternoon"},
                    {"name": "Times Square", "duration": "1h", "cost": "free", "time": "evening"},
                    {"name": "Brooklyn Bridge", "duration": "1h", "cost": "free", "time": "sunset"},
                    {"name": "MoMA Museum", "duration": "3h", "cost": "$25", "time": "afternoon"},
                ],
                "local_tips": [
                    "Get a MetroCard for subway/bus",
                    "Walk around - best way to see the city",
                    "Visit neighborhood restaurants, not chain stores",
                    "Use Citibike for cheap transportation",
                    "Broadway shows sell discounted tickets at TKTS booth",
                ],
                "scams_to_avoid": [
                    "Street shell game scams",
                    "Fake jewelry dealers",
                    "Unlicensed taxis - use yellow cabs or Uber",
                    "Overpriced tourist restaurants",
                ],
                "best_restaurants": [
                    "Joe's Pizza (Pizza, budget) - Classic slice $2.75",
                    "Katz's Deli (Deli, budget) - Pastrami sandwich",
                    "Shake Shack (Burger, moderate) - Classic burger",
                    "Per Se (Fine dining, luxury) - Michelin 3-star"
                ]
            }
        }
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process guide-related queries with enhanced city data"""
        
        intent = self._extract_intent(user_input)
        
        if intent != "guide":
            return self._format_response("error", {"message": "Not a guide request"})
        
        destination = context.get("destination", "").title()
        if not destination:
            return self._format_response("pending", {
                "message": "Which city would you like a guide for?",
                "available_cities": list(self.city_guides.keys())
            })
        
        guide = self.city_guides.get(destination, {})
        if not guide:
            return self._format_response("pending", {
                "message": f"Detailed guide not available for {destination}",
                "available_cities": list(self.city_guides.keys()),
                "suggestion": "I can provide guides for: " + ", ".join(self.city_guides.keys())
            })
        
        # Generate comprehensive itinerary
        trip_duration = self._calculate_duration(context)
        travel_style = context.get("travel_style", "moderate")
        itinerary = self._generate_itinerary(destination, trip_duration)
        
        return self._format_response("success", {
            "destination": destination,
            "country": guide.get("country", ""),
            "currency": guide.get("currency", ""),
            "must_see_attractions": guide.get("must_see", []),
            "daily_itinerary": itinerary,
            "local_tips": guide.get("local_tips", []),
            "scams_to_avoid": guide.get("scams_to_avoid", []),
            "recommended_restaurants": guide.get("best_restaurants", []),
            "estimated_daily_cost": self._estimate_daily_cost(destination, travel_style=travel_style),
            "travel_pace_recommendations": self._recommend_pace(trip_duration, len(guide.get("must_see", [])))
        }, confidence=0.88)
    
    def _calculate_duration(self, context: Dict) -> int:
        """Calculate trip duration in days"""
        start = context.get("start_date")
        end = context.get("end_date")
        if start and end:
            try:
                start_date = datetime.fromisoformat(start) if isinstance(start, str) else start
                end_date = datetime.fromisoformat(end) if isinstance(end, str) else end
                return max(1, (end_date - start_date).days)
            except:
                pass
        return context.get("duration", 3)  # Default to 3 days
    
    def _recommend_pace(self, duration_days: int, attractions_count: int = 5) -> Dict:
        """Recommend optimal travel pace based on trip duration"""
        attractions_per_day = max(1, attractions_count // max(1, (duration_days - 1))) if duration_days > 1 else attractions_count
        
        return {
            "recommended_tempo": "Relaxed" if duration_days >= 7 else "Moderate" if duration_days >= 5 else "Fast-paced",
            "attractions_per_day": attractions_per_day,
            "rest_strategy": "1 full rest day per week" if duration_days >= 7 else "1 half-day per 2 days" if duration_days >= 5 else "No rest - go fast!",
            "exploration_time": "3-4 hours daily for neighborhoods & hidden gems",
            "meal_strategy": "Breakfast at hotel, Lunch at attraction, Dinner exploring local area",
            "daily_schedule": {
                "morning": "6:00 AM - Visit major attractions early",
                "lunch": "12:00-13:00 PM - Local cuisine at real restaurants",
                "afternoon": "14:00-17:00 PM - Secondary attractions or neighborhoods",
                "evening": "18:00+ - Relax, eat, reflect & plan next day"
            }
        }
    
    def _generate_itinerary(self, destination: str, days: int) -> List[Dict]:
        """Generate detailed day-by-day itinerary with timing and budgets"""
        guide = self.city_guides.get(destination, {})
        attractions = guide.get("must_see", [])
        
        itinerary = []
        attraction_index = 0
        
        for day in range(1, min(days + 1, 8)):  # Max 7 days
            morning_attraction = attractions[attraction_index % len(attractions)] if attractions else {}
            afternoon_attraction = attractions[(attraction_index + 1) % len(attractions)] if attractions else {}
            
            day_itinerary = {
                "day": day,
                "date": f"Day {day}",
                "morning": {
                    "time": "08:00-11:00",
                    "activity": morning_attraction.get("name", "Free time"),
                    "duration": morning_attraction.get("duration", "2h"),
                    "cost": morning_attraction.get("cost", "free"),
                    "tips": ["Start early to beat crowds", "Bring water and snacks"]
                },
                "afternoon": {
                    "time": "13:00-17:00",
                    "activity": afternoon_attraction.get("name", "Lunch & exploration"),
                    "duration": afternoon_attraction.get("duration", "3h"),
                    "cost": afternoon_attraction.get("cost", "$20-40"),
                    "tips": ["Have lunch at local restaurant", "Rest or explore neighborhoods"]
                },
                "evening": {
                    "time": "18:00-22:00",
                    "activity": "Dinner & relaxation",
                    "recommendations": guide.get("best_restaurants", [])[:1],
                    "cost": "$15-30",
                    "tips": ["Try local cuisine", "Early night for recovery"]
                }
            }
            
            itinerary.append(day_itinerary)
            attraction_index += 2
        
        return itinerary
    
    def _estimate_daily_cost(self, destination: str, travel_style: str = "moderate") -> Dict:
        """Estimate detailed daily costs based on travel style"""
        cost_breakdown = {
            "cheap": {
                "accommodation": 20,
                "meals": 15,
                "activities": 10,
                "transport": 5,
                "tips": ["Stay in hostels", "Eat street food & local markets", "Free walking tours", "Use public transport"]
            },
            "moderate": {
                "accommodation": 50,
                "meals": 30,
                "activities": 25,
                "transport": 10,
                "tips": ["3-star hotels", "Mix of restaurants & street food", "Paid attractions", "Use metro/bus"]
            },
            "luxury": {
                "accommodation": 150,
                "meals": 80,
                "activities": 100,
                "transport": 20,
                "tips": ["5-star hotels", "Fine dining restaurants", "Premium tours & experiences", "Use taxis/Uber"]
            }
        }
        
        style = travel_style.lower() if travel_style in cost_breakdown else "moderate"
        costs = cost_breakdown[style]
        daily_total = sum(v for k, v in costs.items() if k != "tips")
        
        guide = self.city_guides.get(destination, {})
        currency = guide.get("currency", "USD")
        
        return {
            "travel_style": style,
            "daily_breakdown": {k: v for k, v in costs.items() if k != "tips"},
            "daily_total": daily_total,
            "currency": currency,
            "budget_tips": costs.get("tips", []),
            "multi_day_costs": {
                "3_days": daily_total * 3,
                "7_days": daily_total * 7,
                "14_days": daily_total * 14,
            }
        }
