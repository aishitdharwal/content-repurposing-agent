# Content Repurposing Agent 🔄

A powerful tool to transform your social media content into engaging LinkedIn posts using AI.

## Features

- 🔗 **Multi-Platform Support**: Scrape content from Twitter/X, LinkedIn, and Reddit
- 🤖 **AI-Powered**: Uses Claude API to generate professional LinkedIn content
- 📝 **3 Variations**: Get 3 different styles of LinkedIn posts for each input
- 🎨 **Clean UI**: Easy-to-use Streamlit interface
- ✏️ **Editable**: Customize generated posts before copying

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd content-repurposing-agent
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
   - Copy `.env.example` to `.env`
   - Add your Anthropic API key to `.env`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Get your API key from: https://console.anthropic.com/

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser to `http://localhost:8501`

3. Enter your content:
   - **Option 1**: Paste a URL from Twitter, LinkedIn, or Reddit
   - **Option 2**: Manually paste content if scraping doesn't work

4. Click "Scrape & Generate" or "Generate from Manual Input"

5. Review the 3 generated LinkedIn post variations

6. Copy your favorite version and post to LinkedIn!

## Post Variations

The system generates 3 distinct styles:

1. **Storytelling**: Personal, narrative-driven approach
2. **Analytical**: Data-driven, insights-focused approach
3. **Conversational**: Casual, question-driven approach

## Architecture

```
content-repurposing-agent/
├── app.py              # Streamlit UI
├── scraper.py          # Web scraping logic
├── llm_service.py      # Claude API integration
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md          # This file
```

## Supported Platforms

- ✅ **Twitter/X**: Via nitter.net fallback
- ✅ **LinkedIn**: Basic scraping (may require manual input)
- ✅ **Reddit**: Full JSON API support

**Note**: Due to authentication requirements on Twitter and LinkedIn, some posts may require manual content input. Reddit works most reliably.

## Technology Stack

- **Frontend**: Streamlit
- **Scraping**: BeautifulSoup, Requests
- **AI Model**: Claude (Anthropic API)
- **Python**: 3.8+

## Limitations

- Twitter and LinkedIn heavily restrict scraping without authentication
- Some posts may require manual content input
- Rate limits apply based on your Anthropic API plan

## Tips for Best Results

- Use high-quality, insightful source content
- Content with clear value propositions works best
- Include data or statistics for credibility
- Shorter posts (150-300 words) perform better on LinkedIn

## Contributing

Feel free to submit issues or pull requests!

## License

MIT License

## Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ using Claude AI
