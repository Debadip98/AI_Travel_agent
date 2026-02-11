"""Visa assistance agent - Version 2 with comprehensive database support"""
from .base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime, timedelta
from integrations.visa_database import (
    get_visa_requirements,
    get_all_countries,
    search_visa_countries
)


class VisaAgent(BaseAgent):
    """Agent for visa assistance and requirements - supports 30+ countries"""
    
    def __init__(self):
        super().__init__(
            name="Visa Assistant",
            description="Provide visa requirements, costs, and timelines for 30+ destinations"
        )
        self.supported_countries = get_all_countries()
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process visa-related queries"""
        
        intent = self._extract_intent(user_input)
        
        if intent != "visa":
            return self._format_response("error", {"message": "Not a visa query"})
        
        # Extract destination country
        destination = context.get("destination", "")
        
        # Try to extract from user input if not in context
        if not destination:
            for country in self.supported_countries:
                if country.lower() in user_input.lower():
                    destination = country
                    break
        
        # Try searching if still not found
        if not destination and len(user_input) > 2:
            search_results = search_visa_countries(user_input)
            if search_results:
                destination = search_results[0]
        
        if not destination:
            return self._format_response("pending", {
                "message": "Which country's visa information do you need?",
                "available_countries": self.supported_countries[:10] + ["... and 20+ more"],
                "total_countries": len(self.supported_countries)
            })
        
        # Get visa requirements from database
        visa_data = get_visa_requirements(destination)
        
        if not visa_data:
            return self._format_response("error", {
                "message": f"Visa information not available for {destination}",
                "suggestion": f"Available countries: {', '.join(self.supported_countries[:5])} and more",
                "note": "Please check the official embassy website for the most current information"
            })
        
        # Generate checklist with timeline
        checklist = self._generate_checklist(destination, visa_data, context)
        timeline = self._calculate_timeline(visa_data)
        
        return self._format_response("success", {
            "destination": destination,
            "country": visa_data.get("country"),
            "region": visa_data.get("region"),
            "visa_type": visa_data.get("visa_type"),
            "validity": visa_data.get("validity"),
            "processing_days": visa_data.get("processing_days"),
            "visa_fee": f"${visa_data.get('visa_fee', 0)} {visa_data.get('currency', 'USD')}",
            "currency": visa_data.get("currency"),
            "processing_location": visa_data.get("processing_location"),
            "required_documents": visa_data.get("required_documents", []),
            "useful_links": visa_data.get("useful_links", []),
            "checklist": checklist,
            "timeline": timeline,
            "cost_breakdown": self._estimate_visa_costs(visa_data),
        }, confidence=0.92)
    
    def _generate_checklist(self, destination: str, visa_data: Dict, 
                           context: Dict) -> List[Dict]:
        """Generate a trackable checklist for visa application"""
        
        checklist = []
        docs = visa_data.get("required_documents", [])
        
        # Calculate base due date
        travel_date = context.get("start_date")
        if travel_date:
            try:
                travel = datetime.fromisoformat(travel_date)
                base_due = travel - timedelta(days=21)
            except:
                base_due = datetime.now() + timedelta(days=21)
        else:
            base_due = datetime.now() + timedelta(days=21)
        
        for i, doc in enumerate(docs, 1):
            # Offset due dates for different documents
            due_date = base_due - timedelta(days=(len(docs) - i) * 2)
            
            checklist.append({
                "id": f"visa_{i}",
                "document": doc,
                "order": i,
                "status": "pending",
                "due_date": due_date.isoformat(),
                "importance": "critical" if i <= 3 else "important"
            })
        
        return checklist
    
    def _calculate_timeline(self, visa_data: Dict) -> Dict:
        """Calculate visa application timeline and recommendations"""
        processing_days = visa_data.get("processing_days", 15)
        
        today = datetime.now()
        apply_by = today + timedelta(days=7)  # Start within a week
        visa_ready = apply_by + timedelta(days=processing_days)
        buffer_ready = visa_ready + timedelta(days=7)  # 7-day safety buffer
        
        return {
            "today": today.isoformat(),
            "apply_by_date": apply_by.isoformat(),
            "processing_time_days": processing_days,
            "visa_ready_by": visa_ready.isoformat(),
            "recommended_ready_by": buffer_ready.isoformat(),
            "recommended_travel_date": (buffer_ready + timedelta(days=1)).isoformat(),
            "total_days_from_today": (buffer_ready - today).days
        }
    
    def _estimate_visa_costs(self, visa_data: Dict) -> Dict:
        """Estimate total visa application costs"""
        visa_fee = visa_data.get("visa_fee", 0)
        currency = visa_data.get("currency", "USD")
        
        # Document costs
        doc_costs = {
            "photographs": 15,
            "translation": 25,
            "vaccination": 50,
            "notarization": 20,
            "courier": 30
        }
        
        # Estimate based on document count
        num_docs = len(visa_data.get("required_documents", []))
        estimated_doc_cost = min(num_docs * 10, 100)
        
        # Miscellaneous
        misc = 25  # stamps, envelopes, etc
        
        total = visa_fee + estimated_doc_cost + misc
        
        return {
            "visa_application_fee": f"{visa_fee} {currency}",
            "supporting_documents_estimated": f"{estimated_doc_cost} {currency}",
            "miscellaneous": f"{misc} {currency}",
            "total_estimated": f"{total} {currency}",
            "notes": "Costs vary by country and service provider. Prices shown are estimates."
        }
    
    def get_countries(self) -> List[str]:
        """Get list of all supported countries"""
        return self.supported_countries
    
    def search_countries(self, query: str) -> List[str]:
        """Search for countries by name or region"""
        return search_visa_countries(query)
