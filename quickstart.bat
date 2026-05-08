@echo off
REM Quick Start Script for OneLink Portfolio (Windows)

echo.
echo 🚀 OneLink Portfolio - Quick Start
echo ==================================
echo.

REM Check if Node.js is installed
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    pause
    exit /b 1
)

setlocal enabledelayedexpansion

echo.
echo 📦 Setting up Backend...
cd backend

REM Create Python virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo Installing Python dependencies...
    pip install -q -r requirements.txt
) else (
    echo ⚠️  requirements.txt not found in backend directory
)

REM Check if .env exists, if not create it
if not exist ".env" (
    echo Creating .env file...
    (
        echo # Database
        echo DATABASE_URL=sqlite:///./portfolio.db
        echo.
        echo # GitHub OAuth - CHANGE THESE VALUES
        echo GITHUB_CLIENT_ID=your_github_app_id
        echo GITHUB_CLIENT_SECRET=your_github_app_secret
        echo GITHUB_OAUTH_REDIRECT_URI=http://localhost:8000/auth/callback
        echo.
        echo # JWT
        echo SECRET_KEY=your-secret-key-change-this-in-production
        echo ALGORITHM=HS256
        echo.
        echo # CORS
        echo ALLOWED_ORIGINS=http://localhost:3000
        echo.
        echo # API
        echo API_URL=http://localhost:8000
    ) > .env
    echo ⚠️  .env file created. Please update with your GitHub OAuth credentials!
)

echo ✅ Backend setup complete

cd ..

echo.
echo 📦 Setting up Frontend...
cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install -q
)

REM Check if .env.local exists, if not create it
if not exist ".env.local" (
    echo Creating .env.local file...
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
    ) > .env.local
    echo ✅ .env.local file created
)

echo ✅ Frontend setup complete

echo.
echo ==================================
echo ✨ Setup Complete!
echo ==================================
echo.
echo 📝 Next Steps:
echo.
echo 1️⃣  Configure GitHub OAuth (if not already done):
echo    - Go to https://github.com/settings/developers
echo    - Create a new OAuth App
echo    - Add to backend\.env:
echo       GITHUB_CLIENT_ID=your_app_id
echo       GITHUB_CLIENT_SECRET=your_app_secret
echo.
echo 2️⃣  Start Backend Server (PowerShell or CMD):
echo    cd backend
echo    venv\Scripts\activate.bat
echo    uvicorn app.main:app --reload
echo.
echo 3️⃣  Start Frontend Server (in another terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4️⃣  Open Browser:
echo    http://localhost:3000
echo.
echo 5️⃣  API Documentation:
echo    http://localhost:8000/docs
echo.
echo ==================================
echo.
pause
