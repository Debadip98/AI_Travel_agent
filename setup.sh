#!/bin/bash
# Quick setup script for AI Travel Agent

echo "🌍 AI Travel Agent - Setup Script"
echo "================================="
echo ""

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install it first."
    exit 1
fi
echo "✓ Python $(python3 --version | cut -d' ' -f2) found"

# Backend setup
echo ""
echo "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Setup environment
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp config/.env.example .env
    echo "⚠️  Please edit .env and add your API keys"
fi

cd ..

# Frontend setup
echo ""
echo "Setting up frontend..."
cd frontend

# Check Node
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed. Please install from https://nodejs.org/"
    echo "   Then run: npm install"
else
    echo "✓ Node $(node --version) found"
    echo "Installing npm dependencies..."
    npm install
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Start backend: cd backend && python main.py"
echo "3. Start frontend: cd frontend && npm run dev"
echo ""
echo "🚀 Frontend will be available at http://localhost:3000"
echo "🚀 Backend API will be available at http://localhost:5000"
