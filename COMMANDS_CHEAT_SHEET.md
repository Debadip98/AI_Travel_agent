# 🚀 AI Travel Agent - Command Cheat Sheet

## ⚡ Quick Start (Copy & Paste)

### First Time Setup
```bash
# Clone/Navigate to project
cd /workspaces/AI_Travel_agent

# Run setup
chmod +x setup.sh
./setup.sh

# This will:
# ✓ Create Python virtual environment
# ✓ Install backend dependencies
# ✓ Install frontend dependencies
# ✓ Create .env file
```

### Run Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Browser:**
```
http://localhost:3000
```

---

## 🔧 Development Commands

### Python/Backend
```bash
# Activate virtual environment
source backend/venv/bin/activate

# Install new package
pip install package-name

# Freeze requirements
pip freeze > backend/requirements.txt

# Run Flask in debug mode
export FLASK_ENV=development
export FLASK_DEBUG=True
python backend/main.py

# Run tests
pytest backend/tests/
```

### JavaScript/Frontend
```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview build
npm run preview

# Install new package
npm install package-name
```

---

## 📝 Configuration

### Add API Keys
```bash
# Copy example
cp backend/config/.env.example backend/.env

# Edit with your keys
nano backend/.env  # or use your editor
```

### Common API Setup
```env
#Free - No key needed!
# Open-Meteo Weather: https://open-meteo.com/
# ExchangeRate: https://exchangerate-api.com/

# Flight APIs
AMADEUS_API_KEY=your_key_here
SKYSCANNER_API_KEY=your_key_here

# Maps
GOOGLE_MAPS_API_KEY=your_key_here

# AI
OPENAI_API_KEY=your_key_here

# Gmail
GMAIL_CLIENT_ID=your_id
GMAIL_CLIENT_SECRET=your_secret
```

---

## 🐳 Docker Commands

### Build & Run with Docker
```bash
# Build images
docker-compose build

# Start services
docker-compose up

# Stop services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Run command in container
docker-compose exec backend python main.py
```

---

## 🧪 Testing

### Test Backend
```bash
cd backend
source venv/bin/activate

# Test flight agent
python -c "from agents import FlightAgent; a = FlightAgent(); print(a.process('Find flights to Paris', {}))"

# Test visa agent
python -c "from agents import VisaAgent; a = VisaAgent(); print(a.process('France visa', {'destination': 'France'}))"

# Test all agents
python -m pytest
```

### Test Frontend
```bash
cd frontend

# Run dev server and test manually
npm run dev

# Then visit http://localhost:3000
# Try the chat, fill forms, etc.
```

---

## 🔍 Debugging

### Backend Issues
```bash
# Check Python version
python3 --version

# Check Flask
python -c "import flask; print(flask.__version__)"

# Clear Python cache
find . -type d -name "__pycache__" -exec rm -r {} +

# Recreate virtual env
rm -rf backend/venv
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend Issues
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf frontend/node_modules frontend/package-lock.json
cd frontend
npm install

# Check Node version
node --version
npm --version
```

### Port Already in Use
```bash
# Kill process on port 5000 (backend)
lsof -ti:5000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9

# Or use different ports
# Backend: python main.py --port 5001
# Frontend: npm run dev -- --port 3001
```

---

## 📦 Project Structure Commands

### View project tree
```bash
# With tree command
tree -L 3 -I 'node_modules|venv|__pycache__'

# Or with find
find . -type d -not -path '*/\.*' | head -20
```

### Count files
```bash
# Python files
find backend -name "*.py" | wc -l

# JavaScript files
find frontend -name "*.js" | wc -l

# All code
find . -name "*.py" -o -name "*.js" | wc -l
```

---

## 🔐 Environment & Secrets

### Create .env file
```bash
cp backend/config/.env.example backend/.env
```

### Sample .env
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key

# APIs (optional for testing)
AMADEUS_API_KEY=
GOOGLE_MAPS_API_KEY=
OPENAI_API_KEY=

# Gmail OAuth
GMAIL_CLIENT_ID=
GMAIL_CLIENT_SECRET=
GMAIL_CALLBACK_URL=http://localhost:5000/auth/gmail/callback

# Database
DATABASE_URL=sqlite:///travel_agent.db

# Frontend
FRONTEND_URL=http://localhost:3000
```

### Don't commit secrets!
```bash
# Already in .gitignore:
echo "backend/.env" >> .gitignore
echo "*.pyc" >> .gitignore
```

---

## 📚 File Navigation

### Quick edits
```bash
# Edit Flask main app
nano backend/main.py

# Edit React main app
nano frontend/src/App.js

# Edit agents
nano backend/agents/flight_agent.py
nano backend/agents/visa_agent.py
nano backend/agents/email_agent.py
nano backend/agents/guide_agent.py

# Edit integrations
nano backend/integrations/apis.py
nano backend/integrations/gmail.py
nano backend/integrations/local_search.py

# Edit frontend components
nano frontend/src/components/ChatInterface.js
nano frontend/src/components/ChatMessage.js
nano frontend/src/components/InputBox.js

# Edit styles
nano frontend/src/styles/ChatInterface.css
nano frontend/src/App.css
```

---

## 🚀 Deployment

### Production Build
```bash
# Backend
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 main:create_app()

# Frontend
cd frontend
npm run build
# Deploy dist/ folder to web server
```

### Docker Deploy
```bash
# Build for production
docker-compose -f docker-compose.yml build

# Run
docker-compose up -d

# Scale replicas
docker-compose up --scale backend=3
```

### Cloud Deployment
```bash
# Heroku
heroku create travel-agent
git push heroku main

# AWS
aws deploy create-deployment --application-name travel-agent

# Google Cloud
gcloud app deploy

# Azure
az webapp up --name travel-agent
```

---

## 📊 Monitoring & Logs

### View logs
```bash
# Backend logs
tail -f backend/logs/app.log

# Docker logs
docker-compose logs -f

# Real-time
docker-compose logs -f --tail=50
```

### Performance
```bash
# Check memory usage
docker stats

# CPU usage
top

# Network
netstat -an | grep 5000
```

---

## 🧹 Cleanup

### Remove virtual environment
```bash
rm -rf backend/venv
```

### Remove node modules
```bash
rm -rf frontend/node_modules
```

### Clean Python cache
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Clear database
```bash
rm backend/*.db
rm backend/travel_agent.db
```

### Full reset
```bash
# Remove generated files
rm -rf backend/venv frontend/node_modules
rm -rf backend/__pycache__ frontend/dist
rm backend/.env

# Start fresh
./setup.sh
```

---

## 📖 Useful References

| Topic | Command |
|-------|---------|
| Git status | `git status` |
| View diff | `git diff backend/main.py` |
| Commit changes | `git add . && git commit -m "message"` |
| Push to repo | `git push origin main` |
| View commits | `git log --oneline` |
| Create branch | `git checkout -b feature-name` |

---

## ❓ Troubleshooting Commands

```bash
# Verify Python installation
python3 --version && pip3 --version

# Verify Node installation
node --version && npm --version

# Test backend connectivity
curl http://localhost:5000/health

# Test frontend connectivity
curl http://localhost:3000

# View all running processes
ps aux | grep python
ps aux | grep node

# Kill all Python processes
pkill -f python

# Kill all Node processes
pkill -f node
```

---

## 🎯 Common Workflows

### Add a new agent
```bash
# Create new file
touch backend/agents/booking_agent.py

# Add to __init__.py
nano backend/agents/__init__.py
# Add: from .booking_agent import BookingAgent

# Import in main.py
nano backend/main.py
# Add: from agents import BookingAgent
```

### Add a new API integration
```bash
# Create integration file
touch backend/integrations/new_api.py

# Add to __init__.py
nano backend/integrations/__init__.py
```

### Add new React component
```bash
# Create component
touch frontend/src/components/NewComponent.js

# Import in parent component
nano frontend/src/App.js
# Add: import NewComponent from './components/NewComponent'
```

---

**Keep this sheet handy! 📎**

Save to bookmark for quick reference during development.
