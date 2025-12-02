"""
LLM service for content repurposing using Anthropic's Claude API
"""
import anthropic
from typing import List, Dict
import os
from dotenv import load_dotenv

load_dotenv()


class ContentRepurposer:
    """Uses Claude API to repurpose content for LinkedIn"""
    
    def __init__(self, api_key: str = None):
        """
        Initialize the content repurposer
        
        Args:
            api_key: Anthropic API key (if not provided, reads from environment)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("Anthropic API key not found. Set ANTHROPIC_API_KEY environment variable.")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def generate_linkedin_posts(self, original_content: str, platform: str, author: str = None) -> List[str]:
        """
        Generate 3 variations of LinkedIn posts from the original content
        
        Args:
            original_content: The scraped content from social media
            platform: Source platform (twitter, linkedin, reddit)
            author: Original author name
            
        Returns:
            List of 3 repurposed LinkedIn posts
        """
        
        prompt = self._create_prompt(original_content, platform, author)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract the response text
            response_text = response.content[0].text
            
            # Parse the three variations
            posts = self._parse_response(response_text)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")
    
    def _create_prompt(self, content: str, platform: str, author: str = None) -> str:
        """Create the prompt for Claude"""
        
        author_info = f" by {author}" if author else ""
        
        prompt = f"""You are an expert content strategist specializing in LinkedIn content creation. 

I have a post from {platform.upper()}{author_info} that I want to repurpose for LinkedIn.

Original content:
---
{content}
---

Please create 3 different variations of this content optimized for LinkedIn. Each variation should:

1. Be professional yet engaging
2. Maintain the core message and insights from the original
3. Use LinkedIn-appropriate formatting (short paragraphs, line breaks for readability)
4. Include relevant hashtags (2-5 hashtags)
5. Have a strong hook in the first line
6. Be between 150-300 words
7. Have a clear call-to-action or thought-provoking question at the end

Make each variation distinct in style:
- **Variation 1**: Storytelling approach (personal, narrative-driven)
- **Variation 2**: Analytical approach (data-driven, insights-focused)
- **Variation 3**: Conversational approach (casual, question-driven)

Format your response EXACTLY as follows:

VARIATION 1:
[Your first LinkedIn post here]

VARIATION 2:
[Your second LinkedIn post here]

VARIATION 3:
[Your third LinkedIn post here]

Do not include any additional text outside of these three variations."""

        return prompt
    
    def _parse_response(self, response_text: str) -> List[str]:
        """Parse the Claude response into 3 separate posts"""
        
        # Split by variation markers
        variations = []
        
        # Try to split by VARIATION markers
        parts = response_text.split('VARIATION')
        
        for part in parts[1:]:  # Skip the first empty part
            # Remove the variation number and colon
            lines = part.strip().split('\n', 1)
            if len(lines) > 1:
                post_content = lines[1].strip()
                variations.append(post_content)
        
        # Ensure we have exactly 3 variations
        if len(variations) != 3:
            # Fallback: try to split by double newlines
            parts = response_text.split('\n\n\n')
            variations = [part.strip() for part in parts if part.strip()]
        
        # If we still don't have 3, pad or truncate
        while len(variations) < 3:
            variations.append("Error: Could not generate variation. Please try again.")
        
        variations = variations[:3]
        
        return variations


def test_repurposer():
    """Test the content repurposer"""
    repurposer = ContentRepurposer()
    
    sample_content = """
    Just learned that 80% of software bugs come from 20% of the code. 
    This Pareto principle applies everywhere! Focus on the critical 20% that matters most.
    """
    
    print("Generating LinkedIn posts...")
    posts = repurposer.generate_linkedin_posts(sample_content, "twitter", "Tech Influencer")
    
    for i, post in enumerate(posts, 1):
        print(f"\n{'='*50}")
        print(f"VARIATION {i}:")
        print(f"{'='*50}")
        print(post)
        print()


if __name__ == "__main__":
    test_repurposer()
