@echo off
echo 🚀 Starting CopyBot...
echo ━━━━━━━━━━━━━━━━━━━━━

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Create virtual environment if needed
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

echo 📦 Activating virtual environment...
call venv\Scripts\activate

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo ━━━━━━━━━━━━━━━━━━━━━
echo ✅ Starting bot...
python bot.py

pause