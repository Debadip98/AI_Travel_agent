"""
AI Travel Agent - Architecture Overview

This document describes the system architecture and how components interact.
"""

# System Architecture

## High-Level Flow

```
┌─────────────────┐
│  React Frontend │
├─────────────────┤
│  Chat Interface │
│  Trip Planner   │
│  Components     │
└────────┬────────┘
         │
         ▼
   [API Calls]
         │
         ▼
┌─────────────────────┐
│  Flask Backend      │
├─────────────────────┤
│  /api/chat          │
│  /api/flights       │
│  /api/visa          │
│  /api/email         │
│  /api/guide         │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
  Agents   Integrations
  
  [FlightAgent] ──→ [Flight APIs]
  [VisaAgent]   ──→ [Visa APIs]
  [EmailAgent]  ──→ [Gmail API]
  [GuideAgent]  ──→ [Maps/POI APIs]
  
    + [LocalSearch]
    + [Utils]
```

## Component Breakdown

### Frontend (`/frontend`)
- **React 18** - UI framework
- **Vite** - Build tool (fast dev experience)
- **Components**:
  - `ChatInterface` - Main chat window
  - `ChatMessage` - Individual messages with data rendering
  - `InputBox` - Message input with suggestions
  - `TripPlanner` - Initial trip planning form
- **Services**:
  - `api.js` - Axios client for backend communication

### Backend (`/backend`)
- **Flask** - REST API server
- **Agents** (`/agents`):
  - `FlightAgent` - Flight booking logic
  - `VisaAgent` - Visa requirements and checklists
  - `EmailAgent` - Email drafting and composition
  - `GuideAgent` - City guides and itineraries
  - BaseAgent - Abstract class for all agents
- **Integrations** (`/integrations`):
  - `apis.py` - Flight, Hotel, Transport, Places, Visa APIs
  - `gmail.py` - Gmail OAuth and email management
  - `local_search.py` - Local POI and budget optimization
  - `utils.py` - Helper functions (date parsing, cost estimation, etc.)
- **Models** (`/models`):
  - `User` - User profile and preferences
  - `Trip` - Trip data and bookings
- **Config** (`/config`):
  - `settings.py` - Configuration management
  - `.env` - Environment variables

## Data Flow Example

### Flight Search Request

```
User Input: "Find cheapest flights to Paris"
    ↓
ChatInterface.handleSendMessage()
    ↓
apiClient.sendMessage(message, context)
    ↓
Backend: /api/chat [POST]
    ↓
main.py: route_to_agent()
    ↓
FlightAgent.process(message, context)
    ↓
FlightAgent._parse_flight_request()
    ↓
FlightAgent._search_flights()
    ├─→ flight_api.search_flights() [API integration]
    └─→ Mock flights returned [testing mode]
    ↓
Response formatted with flights data
    ↓
ChatMessage displaying flights
```

## Agent Workflow

Each agent follows this pattern:

```python
class Agent(BaseAgent):
    def process(self, user_input, context):
        1. Extract intent from user input
        2. Validate required data
        3. Query APIs or local data
        4. Format response
        5. Return structured data
```

## Key Design Decisions

### 1. Intent-Based Routing
- Messages are routed to agents based on keywords
- Allows modular, focused agents
- Future: Use LLM for better intent detection

### 2. Mock Data Architecture
- All agents support mock responses
- Real APIs can be swapped in without code changes
- Great for testing and development

### 3. Context Passing
- Trip context passed through all agents
- Enables multi-step conversations
- Stores: destination, dates, budget, preferences

### 4. Structured Responses
- Every agent returns consistent format
- Status, data, confidence, timestamp
- Frontend can handle any agent response

## Database Schema (Future)

```sql
-- Users
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255),
    name VARCHAR(255),
    preferences JSON,
    created_at TIMESTAMP
);

-- Trips
CREATE TABLE trips (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    destination VARCHAR(255),
    start_date DATE,
    end_date DATE,
    budget FLOAT,
    status VARCHAR(50),
    created_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Bookings
CREATE TABLE bookings (
    id VARCHAR(36) PRIMARY KEY,
    trip_id VARCHAR(36),
    type VARCHAR(50), -- flight, hotel, train, etc
    data JSON,
    status VARCHAR(50),
    created_at TIMESTAMP,
    FOREIGN KEY (trip_id) REFERENCES trips(id)
);

-- Messages/Chat History
CREATE TABLE messages (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36),
    trip_id VARCHAR(36),
    message TEXT,
    response JSON,
    agent VARCHAR(50),
    created_at TIMESTAMP
);
```

## Scalability Considerations

### Current (MVP)
- Single process backend
- In-memory data
- Mock APIs

### Short-term (Phase 2)
- Database backend
- Async tasks (Celery)
- Real API integrations
- Rate limiting

### Long-term (Phase 3)
- Microservices per agent
- Message queue (RabbitMQ)
- Caching layer (Redis)
- Multi-region deployment
- Mobile app backend

## Security Considerations

### API Keys
- Store in environment variables (.env)
- Never commit credentials
- Rotate regularly

### Gmail OAuth
- Use secure callback URLs
- Validate tokens before use
- Store encrypted refresh tokens

### User Data
- Encrypt stored credentials
- Hash passwords
- HTTPS only in production

## Testing Strategy

### Unit Tests
- Test each agent independently
- Mock all external APIs
- Validate response formats

### Integration Tests
- Test agent → API integration
- Test API response handling

### End-to-End Tests
- Frontend → Backend full flow
- Chat message → Response cycle

## Deployment

### Development
```bash
python main.py  # Backend
npm run dev     # Frontend
```

### Production
```bash
# Backend
gunicorn -w 4 -b 0.0.0.0:5000 main:create_app()

# Frontend
npm run build
serve -s dist
```

## Future Enhancements

1. **LLM-Powered Intent Detection** - Use GPT for complex queries
2. **Multi-Language Support** - Translate agent responses
3. **Voice Interface** - Speak instead of type
4. **ML-Based Recommendations** - Learn from user preferences
5. **Real-Time Notifications** - Price drop alerts, flight status
6. **Collaborative Planning** - Share trips with friends
7. **Blockchain Bookings** - Decentralized ticketing
8. **AR City Tour** - Augmented reality walking guides

---

For more details, see `travel_agent_plan.md` and `README.md`
