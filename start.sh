#!/bin/bash

# Quick start script for Content Repurposing Agent

echo "🚀 Starting Content Repurposing Agent..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt --quiet

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "📝 Please copy .env.example to .env and add your Anthropic API key"
    echo ""
    read -p "Do you want to create .env now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it and add your API key."
        echo ""
    fi
fi

# Start Streamlit
echo "🌟 Launching Streamlit app..."
echo ""
streamlit run app.py
