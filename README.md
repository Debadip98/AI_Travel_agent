# AI Travel Agent 🌍

A comprehensive AI-powered travel planning assistant for solo travelers.

## Features

### ✈️ Flight Booking
- Search flights by budget tier (cheap, moderate, luxury)
- Easy price comparison
- Direct booking links

### 🛂 Visa Assistance
- Destination-specific visa requirements
- Document checklists with timeline
- Application tracking

### 📧 Email Assistant
- Auto-draft emails to hotels, airlines
- Secure Gmail OAuth integration
- Preview before sending

### 🗺️ Virtual Tour Guide
- City guides with must-see attractions
- Local tips and scam warnings
- Restaurant recommendations
- Day-by-day itineraries

### 💡 Smart Cost Optimizer
- Budget-aware suggestions
- Train vs flight comparison
- Accommodation near transit hubs
- Local grocery stores for budget travelers

### 🚂 Transport Bookings
- Trains, buses, ferries
- Multi-modal journey planning
- Real-time pricing

## Tech Stack

### Backend
- Python 3.10+
- Flask 3.0
- SQLAlchemy
- OpenAI/LLM integration
- Multiple travel API integrations

### Frontend
- React 18
- Vite
- Tailwind CSS
- Responsive design

## Project Structure

```
AI_Travel_agent/
├── backend/
│   ├── agents/              # AI agents (flight, visa, email, guide)
│   ├── integrations/        # API integrations
│   ├── models/              # Data models
│   ├── config/              # Configuration
│   ├── main.py             # Flask app entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   ├── styles/          # CSS
│   │   └── pages/           # Page components
│   ├── package.json
│   └── vite.config.js
└── travel_agent_plan.md     # Detailed product plan
```

## Getting Started

### Backend Setup

```bash
cd backend
cp config/.env.example .env
# Add your API keys to .env
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

## API Integrations Needed

- **Flights**: Amadeus, Skyscanner
- **Hotels**: Booking.com, Hotels.com
- **Trains**: Rome2Rio, Trainline
- **Maps/POI**: Google Maps, Foursquare
- **Email**: Gmail API
- **Visa**: Sherpa, iVisa
- **Weather**: Open-Meteo (free)
- **Currency**: ExchangeRate-API (free)

## MVP Roadmap

### Phase 1 (Week 1-3)
- [x] Chat interface
- [x] Trip planner form
- [x] Flight search agent
- [ ] Flight API integration

### Phase 2 (Week 4-6)
- [ ] Visa checklist module
- [ ] Gmail OAuth integration
- [ ] Local POI search

### Phase 3 (Week 7-10)
- [ ] Train/ferry booking
- [ ] Virtual guide with voice
- [ ] Cost optimizer

## Usage Examples

### Example 1: Budget Traveler
```
User: "I'm a budget solo traveler to Italy for 7 days with $800"
Bot: suggests overnight trains, budget hotels near stations, local eateries
```

### Example 2: Flight Search
```
User: "Find cheapest flight from NYC to Paris next month"
Bot: searches, compares prices, shows options with baggage details
```

### Example 3: Visa Help
```
User: "What do I need for a US visa from India?"
Bot: shows requirements, generates checklist, tracks deadlines
```

### Example 4: Hotel Email
```
User: "Draft email requesting early check-in at my Paris hotel"
Bot: creates draft, shows preview, sends after approval
```

## Contributing

This project is actively being developed. Feel free to fork and contribute!

## License

MIT

## Contact

For questions or suggestions, open an issue or contact the maintainer.

---

**Happy Travels! 🌍✈️**
