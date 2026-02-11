# Quick Start Guide

## 🚀 Getting Started (5 minutes)

### 1. Initial Setup

```bash
# Make setup script executable (Unix/Mac)
chmod +x setup.sh

# Run setup
./setup.sh
```

Or manually:

```bash
# Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp config/.env.example .env

# Frontend
cd frontend
npm install
```

### 2. Configure API Keys

Edit `backend/.env` and add your API keys:

```env
# Free/Trial tiers first
AMADEUS_API_KEY=your-key-here
GOOGLE_MAPS_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here

# Gmail OAuth (get from Google Cloud Console)
GMAIL_CLIENT_ID=your-client-id
GMAIL_CLIENT_SECRET=your-client-secret
```

### 3. Run Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
# Backend running on http://localhost:5000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Frontend running on http://localhost:3000
```

### 4. Test the Application

1. Open http://localhost:3000
2. Enter trip details:
   - Destination: Paris
   - Dates: Pick future dates
   - Budget: $1000
   - Budget tier: moderate

3. Click "Start Planning"
4. Chat with the bot:
   - "Find me flights to Paris"
   - "What documents do I need for France?"
   - "Show me a city guide for Paris"

## 📋 Free API Resources

### Flight & Hotel
- [Amadeus Self-Service API](https://developers.amadeus.com/) - Free tier available
- [RapidAPI Skyscanner](https://rapidapi.com/skyscanner/api/skyscanner-flight-search)
- [Booking.com Affiliate API](https://affiliate.booking.com/)

### Maps & Places
- [Google Maps Places API](https://developers.google.com/maps) - Free credits monthly
- [OpenStreetMap + Overpass](https://overpass-api.de/) - Completely free
- [Foursquare Places API](https://developer.foursquare.com/) - Free tier

### Email
- [Gmail API](https://developers.google.com/gmail/api) - Free
- Microsoft Graph API for Outlook - Free

### Travel & Visa
- [Sherpa Travel API](https://www.sherpa.travel/) - For visa info
- Government embassy websites - Free

### Other
- [Open-Meteo Weather](https://open-meteo.com/) - Free, no API key needed
- [ExchangeRate.host](https://exchangerate.host/) - Free currency conversion
- [LibreTranslate](https://libretranslate.com/) - Free translation

## 🧪 Testing Without APIs

The app works with mock data, so you can test immediately:

1. All agents return mock responses
2. No real API calls are made
3. Perfect for UI/UX testing

To enable real APIs later, just update `config/.env` with keys.

## 📱 Features to Test

- ✅ Chat interface with suggestions
- ✅ Trip planner form
- ✅ Flight search with price tiers
- ✅ Visa requirements by country
- ✅ Email draft composition
- ✅ City guides and itineraries
- ✅ Local recommendations

## 🐛 Troubleshooting

### Port already in use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Python virtual environment issues
```bash
# Recreate venv
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### npm issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 🚀 Next Steps

1. **Add Real API Keys** - Get them from services listed above
2. **Enhance Agents** - Add more sophisticated NLP
3. **Mobile App** - Use React Native or Flutter
4. **Database** - Connect SQLAlchemy to real DB
5. **Authentication** - Add user login system
6. **Payment Integration** - Connect Stripe for bookings

## 📚 Useful Files

- `travel_agent_plan.md` - Full product roadmap
- `README.md` - Project overview
- `backend/requirements.txt` - Python dependencies
- `frontend/package.json` - Node dependencies

## 💬 Support

For issues or questions:
1. Check error messages in terminal
2. Review agent logs in `backend/agents/`
3. Open an issue on GitHub

Happy travels! 🌍✈️
