"""Visa assistance agent"""
from .base_agent import BaseAgent
from typing import Dict, Any, List
from datetime import datetime, timedelta


class VisaAgent(BaseAgent):
    """Agent for visa requirements and checklist tracking"""
    
    def __init__(self):
        super().__init__(
            name="Visa Assistant",
            description="Provide visa requirements, checklists, and application reminders"
        )
        
        # Comprehensive visa requirements database
        self.visa_requirements = {
            "France": {
                "processing_days": 15,
                "fee": 80,
                "visa_type": "Schengen",
                "validity": "90 days",
                "required_docs": [
                    "Valid passport (6 months validity minimum)",
                    "Visa application form (Schengen form)",
                    "Passport photo (35x45mm, recent)",
                    "Birth certificate or marriage certificate",
                    "Proof of funds (€600+/month)",
                    "Proof of accommodation (hotel/Airbnb booking)",
                    "Travel insurance (Schengen minimum €30,000)",
                    "Round trip flight booking",
                    "Employment letter or student enrollment letter"
                ],
                "notes": "EU/EEA nationals may not need visa",
                "processing_location": "French Embassy/Consulate",
                "links": {
                    "official": "https://www.diplomatie.gouv.fr/",
                    "visa_info": "https://france-visas.gouv.fr/"
                }
            },
            "India": {
                "processing_days": 10,
                "fee": 40,
                "visa_type": "Tourist e-Visa available",
                "validity": "60 days",
                "required_docs": [
                    "Valid passport (6 months validity minimum)",
                    "Visa application form (online for e-Visa)",
                    "Passport photo (2x2 inches, white background)",
                    "Yellow fever vaccination (if from endemic areas)",
                    "Proof of funds (bank statements, credit card)",
                    "Hotel booking confirmation",
                    "Round trip flight ticket",
                    "Employment letter",
                    "Address proof (utility bill, lease agreement)"
                ],
                "notes": "Many nationalities can get e-Visa online within 24 hours",
                "processing_location": "Indian Embassy or Online",
                "links": {
                    "official": "https://www.indiaimmigration.gov.in/",
                    "e_visa": "https://indianvisaonline.gov.in/"
                }
            },
            "Japan": {
                "processing_days": 5,
                "fee": 0,
                "visa_type": "Visa waiver / Tourist visa",
                "validity": "90 days",
                "required_docs": [
                    "Valid passport (6 months validity)",
                    "Return/onward ticket",
                    "Proof of accommodation",
                    "Proof of sufficient funds (¥100,000+)",
                    "Employment letter or student ID",
                    "Completed landing card (given on arrival)"
                ],
                "notes": "90-day visa waiver for many nationalities (no visa needed)",
                "processing_location": "Japanese Embassy or Automatic on Arrival",
                "links": {
                    "official": "https://www.mofa.go.jp/",
                    "visa_info": "https://www.us.emb-japan.go.jp/english/"
                }
            },
            "USA": {
                "processing_days": 30,
                "fee": 160,
                "visa_type": "B1/B2 Tourist/Business",
                "validity": "10 years",
                "required_docs": [
                    "Valid passport (6 months validity beyond stay)",
                    "DS-160 form (online)",
                    "Visa application fee receipt",
                    "Passport photo (51x51mm, white background)",
                    "Proof of funds (bank statements, 6 months)",
                    "Travel itinerary and dates",
                    "Employment/study letter",
                    "Proof of residence (utility bill, lease)",
                    "Ties to home country (property, family)"
                ],
                "notes": "Interview usually required. ESTA alternative for some nationalities",
                "processing_location": "US Consulate/Embassy (Interview required)",
                "links": {
                    "official": "https://travel.state.gov/",
                    "visa_forms": "https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/forms/forms-visa-application.html",
                    "consulates": "https://travel.state.gov/content/travel/en/us-visas/visa-information-resources/directory/visa-post-directory.html"
                }
            },
            "UK": {
                "processing_days": 21,
                "fee": 100,
                "visa_type": "Standard Visitor",
                "validity": "6 months",
                "required_docs": [
                    "Valid passport (6 months validity)",
                    "Visa application form (online)",
                    "Passport photos (35x45mm)",
                    "Proof of funds (bank statements, 6 months)",
                    "Proof of accommodation",
                    "Return flight booking",
                    "Employment letter",
                    "Proof of UK ties"
                ],
                "notes": "UK Visas and Immigration (UKVI). No interview required",
                "processing_location": "UK Visa Application Centre",
                "links": {
                    "official": "https://www.gov.uk/government/organisations/uk-visas-and-immigration",
                    "apply": "https://apply-for-a-uk-visa.service.gov.uk/"
                }
            },
            "Canada": {
                "processing_days": 20,
                "fee": 100,
                "visa_type": "Visitor Visa / eTA",
                "validity": "6 months",
                "required_docs": [
                    "Valid passport",
                    "Online application form",
                    "Passport photos (35x45mm, color)",
                    "Proof of funds",
                    "Return flight booking",
                    "Proof of ties to home country",
                    "Employment/study letter",
                    "Travel history"
                ],
                "notes": "EU citizens may need eTA (electronic travel authority) only",
                "processing_location": "Immigration, Refugees and Citizenship Canada (IRCC)",
                "links": {
                    "official": "https://www.canada.ca/en/immigration-refugees-citizenship.html",
                    "apply": "https://www.canada.ca/en/immigration-refugees-citizenship/services/visit-canada/visit-visa.html"
                }
            },
            "Australia": {
                "processing_days": 14,
                "fee": 145,
                "visa_type": "eVisitor/Visitor",
                "validity": "12 months",
                "required_docs": [
                    "Valid passport (6 months validity)",
                    "Visa application (online)",
                    "Passport photo (digital, 100x150px)",
                    "Health declaration",
                    "Proof of funds",
                    "Return/onward ticket",
                    "Employment/family letter"
                ],
                "notes": "eVisitor available for most nationalities",
                "processing_location": "Department of Home Affairs",
                "links": {
                    "official": "https://immi.homeaffairs.gov.au/",
                    "apply": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/tourist-family-friends"
                }
            }
        }
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process visa-related queries"""
        
        intent = self._extract_intent(user_input)
        
        if intent != "visa":
            return self._format_response("error", {"message": "Not a visa query"})
        
        # Extract destination country
        destination = context.get("destination", "")
        
        # Try to extract from user input if not in context
        if not destination:
            for country in self.visa_requirements.keys():
                if country.lower() in user_input.lower():
                    destination = country
                    break
        
        if not destination:
            return self._format_response("pending", {
                "message": "Which country's visa info do you need?",
                "available_countries": list(self.visa_requirements.keys())
            })
        
        # Get visa requirements
        requirements = self.visa_requirements.get(destination)
        
        if not requirements:
            return self._format_response("error", {
                "message": f"Detailed visa info not available for {destination}",
                "suggestion": f"Available: {', '.join(list(self.visa_requirements.keys()))}",
                "note": "Please check official embassy website for most current info"
            })
        
        # Generate checklist with timeline
        checklist = self._generate_checklist(destination, requirements, context)
        timeline = self._calculate_timeline(requirements)
        
        return self._format_response("success", {
            "destination": destination,
            "visa_type": requirements.get("visa_type"),
            "validity": requirements.get("validity"),
            "fee": f"${requirements.get('fee')}",
            "processing_days": requirements.get("processing_days"),
            "required_documents": requirements.get("required_docs", []),
            "notes": requirements.get("notes"),
            "processing_location": requirements.get("processing_location"),
            "useful_links": requirements.get("links", {}),
            "checklist": checklist,
            "timeline": timeline,
            "cost_breakdown": self._estimate_visa_costs(requirements),
        }, confidence=0.95)
    
    def _generate_checklist(self, destination: str, requirements: Dict, 
                           context: Dict) -> List[Dict]:
        """Generate a trackable checklist for visa application"""
        
        checklist = []
        docs = requirements.get("required_docs", [])
        
        for i, doc in enumerate(docs, 1):
            # Calculate due date: 3 weeks before travel
            travel_date = context.get("start_date")
            if travel_date:
                due = (datetime.fromisoformat(travel_date) - timedelta(days=21)).isoformat()
            else:
                due = (datetime.now() + timedelta(days=14)).isoformat()
            
            checklist.append({
                "id": f"visa_{i}",
                "item": i,
                "document": doc,
                "status": "pending",  # pending, ready, submitted, approved
                "due_date": due,
                "estimated_cost": self._estimate_doc_cost(doc),
                "notes": "",
                "importance": "critical" if i <= 3 else "important"
            })
        
        return checklist
    
    def _calculate_timeline(self, requirements: Dict) -> Dict:
        """Calculate visa application timeline"""
        processing_days = requirements.get("processing_days", 15)
        buffer_days = 7
        
        today = datetime.now()
        apply_by = today + timedelta(days=14)
        estimated_approval = apply_by + timedelta(days=processing_days)
        recommended_latest = estimated_approval + timedelta(days=buffer_days)
        
        return {
            "start_preparing": today.isoformat(),
            "apply_by": apply_by.isoformat(),
            "processing_days": processing_days,
            "visa_ready_by": estimated_approval.isoformat(),
            "recommended_latest": recommended_latest.isoformat(),
            "buffer_days": buffer_days,
            "total_days_needed": 14 + processing_days + buffer_days
        }
    
    def _estimate_doc_cost(self, document: str) -> float:
        """Estimate cost for document"""
        doc_costs = {
            "passport": 120,
            "photo": 10,
            "insurance": 30,
            "translation": 20,
            "notarization": 15,
            "vaccination": 50
        }
        
        for key, cost in doc_costs.items():
            if key in document.lower():
                return cost
        
        return 0  # Free documents
    
    def _estimate_visa_costs(self, requirements: Dict) -> Dict:
        """Estimate total visa application costs"""
        visa_fee = requirements.get("fee", 0)
        
        # Estimate supporting document costs
        doc_costs = sum([self._estimate_doc_cost(doc) 
                        for doc in requirements.get("required_docs", [])])
        
        # Additional costs (photos, stamps, delivery)
        misc_costs = 50  # stamps, envelopes, delivery, etc
        
        return {
            "visa_fee": f"${visa_fee}",
            "supporting_documents": f"${min(doc_costs, 200)}",  # Cap at reasonable amount
            "miscellaneous": f"${misc_costs}",
            "total_estimated": f"${visa_fee + min(doc_costs, 200) + misc_costs}"
        }

