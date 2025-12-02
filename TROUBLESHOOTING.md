# Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Installation Issues

#### Problem: "python: command not found"
**Solution:**
```bash
# Check if Python is installed
python3 --version

# If not installed, download from python.org
# Or use:
# Mac: brew install python3
# Ubuntu: sudo apt-get install python3
```

#### Problem: "pip: command not found"
**Solution:**
```bash
# Use python3 -m pip instead
python3 -m pip install -r requirements.txt
```

#### Problem: Dependencies fail to install
**Solution:**
```bash
# Upgrade pip first
pip install --upgrade pip

# Try installing one by one
pip install streamlit
pip install anthropic
pip install beautifulsoup4
pip install requests
pip install python-dotenv
```

---

### 🔴 API Key Issues

#### Problem: "ANTHROPIC_API_KEY not found"
**Solutions:**

1. **Check .env file exists**
```bash
ls -la .env
# Should show .env file
```

2. **Verify .env format**
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```
Note: No spaces around the `=` sign

3. **Try entering in UI**
   - Open app
   - Look at sidebar
   - Paste key directly there

4. **Set environment variable manually**
```bash
# Mac/Linux
export ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows (Command Prompt)
set ANTHROPIC_API_KEY=sk-ant-your-key-here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

#### Problem: "Invalid API key"
**Solution:**
- Verify key starts with `sk-ant-`
- Check for extra spaces or characters
- Get a fresh key from https://console.anthropic.com/

---

### 🔴 Scraping Issues

#### Problem: "Unable to scrape Twitter content"
**Cause:** Twitter blocks most scraping attempts

**Solutions:**
1. Use manual input instead
2. Copy tweet text manually
3. Use Twitter's API (requires separate setup)

#### Problem: "Unable to scrape LinkedIn content"
**Cause:** LinkedIn requires authentication

**Solutions:**
1. Use manual input tab
2. Copy LinkedIn post text manually
3. For bulk: Consider LinkedIn API

#### Problem: Reddit scraping fails
**Cause:** Usually network or URL issues

**Solutions:**
1. Check URL format: `https://www.reddit.com/r/subreddit/comments/id/title/`
2. Ensure URL is publicly accessible
3. Try incognito/private browser first
4. Check internet connection

#### Problem: "Connection timeout"
**Solutions:**
```python
# In scraper.py, increase timeout:
response = requests.get(url, headers=self.headers, timeout=30)  # Changed from 10
```

---

### 🔴 Generation Issues

#### Problem: "Rate limit exceeded"
**Solutions:**
1. Wait 60 seconds between requests
2. Upgrade API plan
3. Implement rate limiting:
```python
import time
time.sleep(2)  # Wait 2 seconds between calls
```

#### Problem: Generated posts are too short/long
**Solution:**
Edit `llm_service.py` prompt:
```python
# Change this line:
"5. Be between 150-300 words"
# To:
"5. Be between 200-400 words"  # Or your preferred range
```

#### Problem: Hashtags not relevant
**Solution:**
Add to prompt in `llm_service.py`:
```python
f"""
...
4. Include relevant hashtags for {specific_industry}
...
"""
```

#### Problem: "Could not parse variations"
**Cause:** API response format changed

**Solution:**
Check response in `llm_service.py`:
```python
# Add debugging
print("Raw response:", response_text)
```

---

### 🔴 UI Issues

#### Problem: Streamlit won't start
**Solutions:**
1. Check port 8501 is free:
```bash
# Mac/Linux
lsof -i :8501
kill -9 <PID>

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

2. Use different port:
```bash
streamlit run app.py --server.port 8502
```

#### Problem: UI looks broken
**Solutions:**
1. Clear browser cache
2. Try different browser
3. Restart Streamlit:
```bash
# Kill all streamlit processes
pkill -f streamlit
streamlit run app.py
```

#### Problem: "Copy button doesn't work"
**Cause:** Browser security settings

**Solution:**
- Use HTTPS (for production)
- Manually select and copy text
- Use keyboard shortcut (Cmd+C or Ctrl+C)

---

### 🔴 Performance Issues

#### Problem: App is slow
**Solutions:**

1. **Reduce token usage:**
```python
# In llm_service.py
max_tokens=1500  # Instead of 2000
```

2. **Add caching:**
```python
import streamlit as st

@st.cache_data
def generate_posts(content):
    # Your generation code
    pass
```

3. **Check internet speed:**
```bash
# Test connection
ping api.anthropic.com
```

#### Problem: High API costs
**Solutions:**
1. Use Haiku model instead of Sonnet:
```python
# In llm_service.py
self.model = "claude-haiku-4-5-20251001"
```

2. Reduce max_tokens:
```python
max_tokens=1000  # Instead of 2000
```

3. Implement caching for repeated content

---

### 🔴 Environment Issues

#### Problem: Virtual environment not activating
**Solutions:**

**Mac/Linux:**
```bash
# Make sure you're in the right directory
cd content-repurposing-agent

# Activate
source venv/bin/activate

# Should see (venv) in prompt
```

**Windows:**
```bash
# Command Prompt
venv\Scripts\activate.bat

# PowerShell
venv\Scripts\Activate.ps1

# If PowerShell blocked:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Problem: "Module not found" after installation
**Solutions:**
1. Verify venv is activated (see `(venv)` in prompt)
2. Reinstall in venv:
```bash
pip install -r requirements.txt --force-reinstall
```

3. Check Python version:
```bash
python --version  # Should be 3.8+
```

---

### 🔴 Content Quality Issues

#### Problem: Generated posts don't match my style
**Solution:**
Customize prompt in `llm_service.py`:
```python
prompt = f"""
You are an expert content strategist who writes in [YOUR STYLE].

Example of preferred style:
[PASTE EXAMPLE OF YOUR WRITING]

Now transform this content...
"""
```

#### Problem: Posts lack personality
**Solution:**
Add to prompt:
```python
"""
Additional requirements:
- Use emojis sparingly
- Include personal anecdotes where appropriate
- Maintain an authentic, genuine tone
- Avoid corporate jargon
"""
```

#### Problem: Hashtags are generic
**Solution:**
Specify in prompt:
```python
f"""
Include hashtags specifically relevant to {industry}
Examples: #AI, #MachineLearning, #DataScience
Avoid generic tags like #MondayMotivation
"""
```

---

### 🔴 Testing Issues

#### Problem: Tests fail
**Solutions:**

1. **Check test.py has valid URLs:**
```python
# Update with real, working URLs
test_urls = {
    'reddit': 'https://www.reddit.com/r/Python/comments/VALID_ID/'
}
```

2. **Skip scraper tests:**
```python
# Comment out scraper test if problematic
# test_scraper()
```

3. **Run individual tests:**
```python
# Instead of python test.py
python -c "from test import test_llm_service; test_llm_service()"
```

---

## 🆘 Emergency Fixes

### Nuclear Option: Fresh Start
```bash
# 1. Backup your .env file
cp .env .env.backup

# 2. Remove everything
rm -rf venv/
rm -rf __pycache__/

# 3. Fresh install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Restore .env
cp .env.backup .env

# 5. Test
streamlit run app.py
```

### Quick Diagnostics
```bash
# Run this to check everything
python3 --version          # Check Python
pip list                   # Check installed packages
cat .env | grep ANTHROPIC  # Check API key (careful, this shows it!)
streamlit --version        # Check Streamlit
```

---

## 📞 Still Having Issues?

1. **Check logs:**
   - Streamlit logs in terminal
   - Error messages in browser console (F12)

2. **Enable debug mode:**
```python
# In app.py, add at top:
import streamlit as st
st.set_option('client.showErrorDetails', True)
```

3. **Get help:**
   - Check GitHub issues
   - Review PROJECT_SUMMARY.md
   - Ask in community forums

---

## 💡 Pro Tips

1. **Keep a test script:**
```python
# test_basic.py
from llm_service import ContentRepurposer

repurposer = ContentRepurposer()
posts = repurposer.generate_linkedin_posts("test content", "twitter")
print(posts[0])
```

2. **Monitor API usage:**
   - Check Anthropic console regularly
   - Set up billing alerts
   - Track token usage

3. **Version control:**
```bash
git init
git add .
git commit -m "Initial setup"
# Before major changes:
git commit -am "Before customization"
```

---

Last Updated: December 2024
