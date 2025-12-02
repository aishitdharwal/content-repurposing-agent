# Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- Anthropic API key

## Setup Steps

### 1. Get Your Anthropic API Key
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-...`)

### 2. Install Dependencies

**Option A: Using the start script (easiest)**
```bash
# On Mac/Linux:
chmod +x start.sh
./start.sh

# On Windows:
start.bat
```

**Option B: Manual installation**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

**Option A: Environment variable**
```bash
# Create .env file
cp .env.example .env

# Edit .env and add your key:
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

**Option B: Enter in UI**
You can also enter your API key directly in the Streamlit sidebar when you run the app.

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Testing

To verify everything works:

```bash
python test.py
```

This will test:
- Scraper functionality
- LLM service
- End-to-end pipeline

## Common Issues

### Issue: "Module not found"
**Solution:** Make sure you activated the virtual environment and installed dependencies

### Issue: "API key not found"
**Solution:** Double-check your `.env` file or enter the key in the UI sidebar

### Issue: "Scraping failed"
**Solution:** 
- Twitter/LinkedIn often block scraping - use manual input instead
- Reddit should work reliably
- Check if the URL is publicly accessible

### Issue: "Rate limit exceeded"
**Solution:** Wait a few minutes or upgrade your Anthropic API plan

## Next Steps

1. Try the example URLs in `examples.py`
2. Customize prompts in `llm_service.py` for your use case
3. Adjust settings in `config.py` if needed

## Need Help?

- Check the main README.md for detailed documentation
- Review examples.py for usage patterns
- Open an issue on GitHub if you encounter problems
