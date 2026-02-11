"""Email composition and sending agent"""
from .base_agent import BaseAgent
from typing import Dict, Any, List


class EmailAgent(BaseAgent):
    """Agent for drafting and sending emails"""
    
    def __init__(self):
        super().__init__(
            name="Email Assistant",
            description="Draft and send emails to hotels, airlines, and travel partners"
        )
        
        # Email templates
        self.templates = {
            "hotel_early_checkin": {
                "subject": "Early Check-in Request",
                "body": """
Dear {hotel_name},

I hope this message finds you well. I am arriving at your hotel on {date} and would like to request early check-in if available.

My reservation details:
- Confirmation number: {confirmation}
- Arrival time: {arrival_time}
- Guest name: {guest_name}

Please let me know if this is possible.

Thank you,
{guest_name}
                """
            },
            "hotel_inquiry": {
                "subject": "Inquiry About Room & Services",
                "body": """
Dear {hotel_name},

I am planning to stay at your hotel from {check_in} to {check_out}. I have a few questions:

1. {question_1}
2. {question_2}

I look forward to your response.

Best regards,
{guest_name}
                """
            },
            "airline_special_meal": {
                "subject": "Special Meal Request",
                "body": """
Dear {airline_name},

I have a flight booked with you on {flight_date}:
Confirmation: {confirmation}

I would like to request a {meal_type} meal due to dietary restrictions.

Thank you,
{passenger_name}
                """
            }
        }
    
    def process(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process email composition request"""
        
        intent = self._extract_intent(user_input)
        
        if intent != "email":
            return self._format_response("error", {"message": "Not an email request"})
        
        # Determine email type
        email_type = self._detect_email_type(user_input)
        
        # Get template
        template = self.templates.get(email_type, {})
        
        if not template:
            return self._format_response("pending", {
                "message": "Please provide more details about the email",
                "examples": list(self.templates.keys())
            })
        
        # Draft email
        draft = self._generate_draft(template, user_input, context)
        
        return self._format_response("success", {
            "draft_email": draft,
            "requires_approval": True,
            "can_send_now": False,
            "placeholders_filled": draft.get("placeholders_filled", []),
            "missing_info": draft.get("missing_info", [])
        }, confidence=0.80)
    
    def _detect_email_type(self, text: str) -> str:
        """Detect type of email to compose"""
        text_lower = text.lower()
        
        if "early" in text_lower and "checkin" in text_lower:
            return "hotel_early_checkin"
        elif "meal" in text_lower and "special" in text_lower:
            return "airline_special_meal"
        elif "hotel" in text_lower or "inquiry" in text_lower:
            return "hotel_inquiry"
        
        return None
    
    def _generate_draft(self, template: Dict, user_input: str, 
                       context: Dict) -> Dict:
        """Generate email draft from template"""
        
        subject = template.get("subject", "")
        body = template.get("body", "")
        
        # Extract context variables
        context_vars = {
            "hotel_name": context.get("hotel_name", "[Hotel Name]"),
            "date": context.get("arrival_date", "[Date]"),
            "guest_name": context.get("user_name", "[Your Name]"),
            "confirmation": context.get("confirmation_number", "[Confirmation #]"),
            "arrival_time": context.get("arrival_time", "[Time]"),
            "check_in": context.get("start_date", "[Check-in Date]"),
            "check_out": context.get("end_date", "[Check-out Date]"),
        }
        
        # Replace placeholders where data available
        for key, value in context_vars.items():
            placeholder = "{" + key + "}"
            subject = subject.replace(placeholder, value)
            body = body.replace(placeholder, value)
        
        return {
            "to": context.get("recipient_email", ""),
            "subject": subject.strip(),
            "body": body.strip(),
            "placeholders_filled": list(context_vars.keys()),
            "missing_info": [],
            "status": "draft"
        }
    
    def send_email(self, email_data: Dict, user_tokens: Dict) -> Dict:
        """Send email using Gmail API (with user approval)"""
        # This will use Gmail API integration
        return {
            "status": "pending",
            "message": "Ready to send. Awaiting user confirmation.",
            "email_preview": email_data
        }
