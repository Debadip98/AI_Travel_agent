"""Utility functions for the application"""
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any
import json


def calculate_trip_duration(start_date: str, end_date: str) -> int:
    """Calculate days between two dates"""
    start = datetime.fromisoformat(start_date)
    end = datetime.fromisoformat(end_date)
    return (end - start).days


def parse_budget_tier(budget: float, duration: int) -> str:
    """
    Determine budget tier based on total budget and duration
    
    Returns: 'cheap', 'moderate', or 'luxury'
    """
    daily_budget = budget / max(duration, 1)
    
    if daily_budget < 50:
        return "cheap"
    elif daily_budget < 150:
        return "moderate"
    else:
        return "luxury"


def estimate_trip_cost(budget_tier: str, duration: int, travelers: int = 1) -> Dict[str, float]:
    """Estimate breakdown of trip costs"""
    daily_costs = {
        "cheap": {
            "accommodation": 15,
            "food": 10,
            "transport": 5,
            "activities": 5
        },
        "moderate": {
            "accommodation": 40,
            "food": 25,
            "transport": 10,
            "activities": 20
        },
        "luxury": {
            "accommodation": 150,
            "food": 80,
            "transport": 30,
            "activities": 100
        }
    }
    
    costs = daily_costs.get(budget_tier, daily_costs["moderate"])
    
    total_cost = {}
    for category, daily_cost in costs.items():
        total_cost[category] = daily_cost * duration * travelers
    
    total_cost["total"] = sum(total_cost.values())
    
    return total_cost


def format_currency(amount: float, currency: str = "USD") -> str:
    """Format amount as currency"""
    currency_symbols = {
        "USD": "$",
        "EUR": "€",
        "GBP": "£",
        "INR": "₹",
        "JPY": "¥"
    }
    
    symbol = currency_symbols.get(currency, currency)
    return f"{symbol}{amount:,.2f}"


def get_next_available_date(days_ahead: int = 14) -> str:
    """Get date X days from now in ISO format"""
    return (datetime.now() + timedelta(days=days_ahead)).isoformat()


def parse_user_preferences(message: str) -> Dict[str, str]:
    """Extract travel preferences from user message"""
    preferences = {
        "budget_tier": "moderate",
        "solo": "solo" in message.lower(),
        "family": "family" in message.lower(),
        "adventure": any(word in message.lower() for word in ["adventure", "hiking", "trek", "active"]),
        "culture": any(word in message.lower() for word in ["culture", "museum", "history", "heritage"]),
        "relaxation": any(word in message.lower() for word in ["relax", "beach", "spa", "resort"])
    }
    
    # Detect budget tier
    if any(word in message.lower() for word in ["budget", "cheap", "affordable", "economical"]):
        preferences["budget_tier"] = "cheap"
    elif any(word in message.lower() for word in ["luxury", "premium", "expensive", "high-end"]):
        preferences["budget_tier"] = "luxury"
    
    return preferences


def validate_dates(start_date: str, end_date: str) -> Tuple[bool, str]:
    """Validate travel dates"""
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        if start >= end:
            return False, "End date must be after start date"
        
        if start < datetime.now():
            return False, "Start date cannot be in the past"
        
        duration = (end - start).days
        if duration > 365:
            return False, "Trip duration cannot exceed 365 days"
        
        return True, "Valid"
    except ValueError:
        return False, "Invalid date format. Use ISO format (YYYY-MM-DD)"


def validate_budget(budget: float, duration: int) -> Tuple[bool, str]:
    """Validate trip budget"""
    if budget <= 0:
        return False, "Budget must be positive"
    
    daily_budget = budget / max(duration, 1)
    
    if daily_budget < 30:
        return True, f"Warning: Daily budget of ${daily_budget:.2f} is very tight. Consider increasing budget or duration."
    
    return True, "Budget is acceptable"
