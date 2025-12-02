# Quick Reference Card

## 🚀 Quick Start Commands

```bash
# Setup (First time only)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
cp .env.example .env      # Then add your API key

# Run the app
streamlit run app.py

# Or use the start script
./start.sh               # Mac/Linux
start.bat                # Windows
```

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application |
| `scraper.py` | Web scraping logic |
| `llm_service.py` | Claude API integration |
| `config.py` | Configuration settings |
| `test.py` | Testing suite |
| `.env` | API key storage |

## 🔑 Environment Setup

```bash
# .env file format
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

## 🌐 Supported URLs

```
✅ Reddit:  https://www.reddit.com/r/subreddit/comments/...
⚠️ Twitter: https://twitter.com/user/status/...  (may fail)
⚠️ LinkedIn: https://www.linkedin.com/posts/...  (may fail)
```

## 🎯 Common Tasks

### Run the app
```bash
streamlit run app.py
```

### Test everything
```bash
python test.py
```

### Test scraper only
```bash
python scraper.py
```

### Test LLM service only
```bash
python llm_service.py
```

### Run examples
```bash
python examples.py
```

## 🛠️ Customization

### Change post length
Edit `llm_service.py` line ~95:
```python
7. Be between [YOUR_MIN]-[YOUR_MAX] words
```

### Change model
Edit `llm_service.py` line ~26:
```python
self.model = "claude-sonnet-4-20250514"  # or "claude-haiku-4-5-20251001"
```

### Change hashtag count
Edit `llm_service.py` line ~96:
```python
4. Include relevant hashtags ([MIN]-[MAX] hashtags)
```

### Adjust temperature (creativity)
Edit `llm_service.py` line ~60:
```python
temperature=0.7  # 0.0 = deterministic, 1.0 = creative
```

## 🐛 Quick Fixes

### Can't scrape
➡️ Use manual input tab

### API key not working
➡️ Check .env format: `ANTHROPIC_API_KEY=sk-ant-...`

### Port 8501 busy
➡️ `streamlit run app.py --server.port 8502`

### Module not found
➡️ Activate venv: `source venv/bin/activate`

### Slow generation
➡️ Switch to Haiku model or reduce max_tokens

## 📊 API Costs (Approximate)

| Model | Input | Output | Per Request |
|-------|-------|--------|-------------|
| Sonnet 4 | $3/M | $15/M | ~$0.05 |
| Haiku 4.5 | $1/M | $5/M | ~$0.02 |

*M = Million tokens*

## ⚡ Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Run script | `Ctrl+Enter` (in terminal) |
| Stop Streamlit | `Ctrl+C` |
| Clear terminal | `clear` or `cls` |
| Copy text | `Cmd+C` or `Ctrl+C` |

## 📚 File Locations

```
Project Root: /Users/aishitdharwal/Documents/AI Classroom/content-repurposing-agent/

Main Files:
- UI:          app.py
- Scraper:     scraper.py
- LLM:         llm_service.py
- Config:      config.py

Documentation:
- Setup:       SETUP.md
- Issues:      TROUBLESHOOTING.md
- Details:     PROJECT_SUMMARY.md
- Main:        README.md

Helpers:
- Tests:       test.py
- Examples:    examples.py
- Start:       start.sh / start.bat
```

## 🎨 UI Navigation

1. **Sidebar (Left)**
   - API Key input
   - Platform status
   - Instructions

2. **Main Area**
   - **Tab 1**: URL Input
   - **Tab 2**: Manual Input

3. **Results (Bottom)**
   - 3 columns with variations
   - Copy buttons
   - Editable text areas

## 💡 Best Practices

1. ✅ Test with Reddit first (most reliable)
2. ✅ Keep source content under 500 words
3. ✅ Review generated posts before using
4. ✅ Customize hashtags for your niche
5. ✅ Save your .env file (but don't commit it!)

## 🔗 Useful Links

- Anthropic Console: https://console.anthropic.com/
- Claude Docs: https://docs.anthropic.com/
- Streamlit Docs: https://docs.streamlit.io/

## 📞 Getting Help

1. Check TROUBLESHOOTING.md
2. Review examples.py
3. Run test.py for diagnostics
4. Enable debug in app.py

## 🎯 Workflow Cheatsheet

```
1. Start app → streamlit run app.py
2. Enter URL or text
3. Click generate
4. Review 3 variations
5. Copy favorite
6. Paste to LinkedIn
7. Success! 🎉
```

---

**Remember:** 
- Activate venv before running
- Set API key in .env
- Reddit works best for scraping
- Edit posts to match your voice

---

**Quick Commands Reference:**

```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app.py

# Test
python test.py

# Kill
Ctrl+C
```

---

Last Updated: December 2024
Version: 1.0.0
