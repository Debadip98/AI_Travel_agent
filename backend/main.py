"""Main Flask application"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from config.settings import config
from agents import FlightAgent, VisaAgent, EmailAgent, GuideAgent
from integrations.auth import register_auth_routes
import os


def create_app(config_name="development"):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config.get(config_name, "development"))
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    
    # Initialize agents
    app.flight_agent = FlightAgent()
    app.visa_agent = VisaAgent()
    app.email_agent = EmailAgent()
    app.guide_agent = GuideAgent()
    
    # Register authentication routes
    register_auth_routes(app)
    
    # Register API routes
    register_routes(app)
    
    return app


def register_routes(app):
    """Register application routes"""
    
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy", "service": "AI Travel Agent"})
    
    @app.route("/api/chat", methods=["POST"])
    def chat():
        """Main chat endpoint - routes to appropriate agent"""
        data = request.json
        user_message = data.get("message", "")
        user_context = data.get("context", {})
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Route to appropriate agent based on intent
        response = route_to_agent(app, user_message, user_context)
        
        return jsonify(response)
    
    @app.route("/api/flights/search", methods=["POST"])
    def search_flights():
        """Search flights endpoint"""
        data = request.json
        response = app.flight_agent.process(
            data.get("query", ""),
            data.get("context", {})
        )
        return jsonify(response)
    
    @app.route("/api/visa/requirements", methods=["POST"])
    def visa_requirements():
        """Get visa requirements"""
        data = request.json
        response = app.visa_agent.process(
            data.get("query", ""),
            data.get("context", {})
        )
        return jsonify(response)
    
    @app.route("/api/email/draft", methods=["POST"])
    def draft_email():
        """Draft an email"""
        data = request.json
        response = app.email_agent.process(
            data.get("query", ""),
            data.get("context", {})
        )
        return jsonify(response)
    
    @app.route("/api/guide/itinerary", methods=["POST"])
    def guide_itinerary():
        """Get city guide and itinerary"""
        data = request.json
        response = app.guide_agent.process(
            data.get("query", ""),
            data.get("context", {})
        )
        return jsonify(response)
    
    @app.route("/api/trip/create", methods=["POST"])
    def create_trip():
        """Create a new trip"""
        data = request.json
        trip_data = {
            "destination": data.get("destination"),
            "start_date": data.get("start_date"),
            "end_date": data.get("end_date"),
            "budget": data.get("budget"),
            "status": "planning"
        }
        return jsonify({"status": "success", "trip": trip_data})


def route_to_agent(app, message, context):
    """Route message to appropriate agent"""
    message_lower = message.lower()
    
    if any(keyword in message_lower for keyword in ["flight", "fly", "airline"]):
        return app.flight_agent.process(message, context)
    elif any(keyword in message_lower for keyword in ["visa", "passport"]):
        return app.visa_agent.process(message, context)
    elif any(keyword in message_lower for keyword in ["email", "send", "draft"]):
        return app.email_agent.process(message, context)
    elif any(keyword in message_lower for keyword in ["guide", "tour", "itinerary", "activity"]):
        return app.guide_agent.process(message, context)
    else:
        return {"agent": "General", "status": "info", "message": "How can I help you with your trip?"}


if __name__ == "__main__":
    app = create_app(os.getenv("FLASK_ENV", "development"))
    app.run(debug=True, host="0.0.0.0", port=5000)
