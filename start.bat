@echo off
REM Quick start script for Content Repurposing Agent (Windows)

echo Starting Content Repurposing Agent...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet

REM Check if .env exists
if not exist ".env" (
    echo Warning: .env file not found!
    echo Please copy .env.example to .env and add your Anthropic API key
    echo.
    copy .env.example .env
    echo Created .env file. Please edit it and add your API key.
    echo.
)

REM Start Streamlit
echo Launching Streamlit app...
echo.
streamlit run app.py
