#!/bin/bash
# Quick Start Script for OneLink Portfolio (macOS/Linux)

echo "🚀 OneLink Portfolio - Quick Start"
echo "=================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo ""
echo "📦 Setting up Backend..."
cd "$SCRIPT_DIR/backend"

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -q -r requirements.txt
else
    echo "⚠️  requirements.txt not found in backend directory"
fi

# Check if .env exists, if not create it
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cat > .env << 'EOF'
# Database
DATABASE_URL=sqlite:///./portfolio.db

# GitHub OAuth - CHANGE THESE VALUES
GITHUB_CLIENT_ID=your_github_app_id
GITHUB_CLIENT_SECRET=your_github_app_secret
GITHUB_OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256

# CORS
ALLOWED_ORIGINS=http://localhost:3000

# API
API_URL=http://localhost:8000
EOF
    echo "⚠️  .env file created. Please update with your GitHub OAuth credentials!"
fi

echo "✅ Backend setup complete"

echo ""
echo "📦 Setting up Frontend..."
cd "$SCRIPT_DIR/frontend"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install -q
fi

# Check if .env.local exists, if not create it
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF
    echo "✅ .env.local file created"
fi

echo "✅ Frontend setup complete"

echo ""
echo "=================================="
echo "✨ Setup Complete!"
echo "=================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1️⃣  Configure GitHub OAuth (if not already done):"
echo "   - Go to https://github.com/settings/developers"
echo "   - Create a new OAuth App"
echo "   - Add to backend/.env:"
echo "      GITHUB_CLIENT_ID=your_app_id"
echo "      GITHUB_CLIENT_SECRET=your_app_secret"
echo ""
echo "2️⃣  Start Backend Server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "3️⃣  Start Frontend Server (in another terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4️⃣  Open Browser:"
echo "   http://localhost:3000"
echo ""
echo "5️⃣  API Documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "=================================="
