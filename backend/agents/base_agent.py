"""Base agent class for all travel agents"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime


class BaseAgent(ABC):
    """Abstract base class for travel agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.created_at = datetime.now()
    
    @abstractmethod
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user input and return response
        
        Args:
            user_input: User's request/message
            context: Trip and user context
            
        Returns:
            Agent response with intent, data, and next steps
        """
        pass
    
    def _extract_intent(self, text: str) -> str:
        """Extract user's intent from text"""
        text_lower = text.lower()
        
        intents = {
            "flight": ["flight", "fly", "airline", "plane"],
            "hotel": ["hotel", "stay", "accommodation", "room"],
            "train": ["train", "rail", "railway"],
            "visa": ["visa", "passport", "travel document"],
            "email": ["email", "send email", "draft", "contact"],
            "guide": ["guide", "tour", "itinerary", "activity", "where to go"],
            "budget": ["budget", "cheap", "save", "cost"],
            "grocery": ["grocery", "food", "eat", "restaurant", "market"],
            "transport": ["transport", "taxi", "uber", "public transport", "metro"]
        }
        
        for intent, keywords in intents.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return "general"
    
    def _format_response(self, status: str, data: Dict = None, 
                        confidence: float = 1.0) -> Dict[str, Any]:
        """Format standard agent response"""
        return {
            "agent": self.name,
            "status": status,  # success, pending, error
            "data": data or {},
            "confidence": confidence,
            "timestamp": datetime.now().isoformat()
        }
