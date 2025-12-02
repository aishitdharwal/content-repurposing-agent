"""
Configuration settings for Content Repurposing Agent
"""

# LLM Settings
DEFAULT_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 2000
TEMPERATURE = 0.7

# Post Generation Settings
MIN_POST_LENGTH = 150  # words
MAX_POST_LENGTH = 300  # words
NUM_VARIATIONS = 3
HASHTAG_COUNT_RANGE = (2, 5)

# Scraping Settings
REQUEST_TIMEOUT = 10  # seconds
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'

# Platform-specific settings
PLATFORMS = {
    'twitter': {
        'name': 'Twitter/X',
        'fallback_domain': 'nitter.net',
        'requires_auth': True
    },
    'linkedin': {
        'name': 'LinkedIn',
        'requires_auth': True
    },
    'reddit': {
        'name': 'Reddit',
        'requires_auth': False
    }
}

# Variation Styles
VARIATION_STYLES = {
    1: {
        'name': 'Storytelling',
        'icon': '🎭',
        'description': 'Personal, narrative-driven approach'
    },
    2: {
        'name': 'Analytical',
        'icon': '📊',
        'description': 'Data-driven, insights-focused approach'
    },
    3: {
        'name': 'Conversational',
        'icon': '💬',
        'description': 'Casual, question-driven approach'
    }
}
