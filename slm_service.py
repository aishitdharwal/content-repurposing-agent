"""
SLM service for content repurposing using local Small Language Models via Ollama
"""
import requests
from typing import List, Dict
import json


class ContentRepurposerSLM:
    """Uses local SLM via Ollama to repurpose content for LinkedIn"""
    
    def __init__(self, model_name: str = "llama3.2", base_url: str = "http://localhost:11434"):
        """
        Initialize the content repurposer with local SLM
        
        Args:
            model_name: Name of the Ollama model to use (default: llama3.2)
            base_url: Ollama API base URL (default: http://localhost:11434)
        """
        self.model_name = model_name
        self.base_url = base_url
        self.api_endpoint = f"{base_url}/api/generate"
        
        # Test connection to Ollama
        self._test_connection()
    
    def _test_connection(self):
        """Test if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Cannot connect to Ollama at {self.base_url}. "
                f"Please ensure Ollama is running. Error: {str(e)}"
            )
    
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
            response = self._call_ollama(prompt)
            
            # Parse the three variations
            posts = self._parse_response(response)
            
            return posts
            
        except Exception as e:
            raise Exception(f"Error generating content: {str(e)}")
    
    def _call_ollama(self, prompt: str) -> str:
        """
        Call Ollama API to generate response
        
        Args:
            prompt: The prompt to send to the model
            
        Returns:
            Generated text response
        """
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 2000
            }
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=120  # Longer timeout for local models
            )
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', '')
            
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. The model might be taking too long to respond.")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling Ollama API: {str(e)}")
    
    def _create_prompt(self, content: str, platform: str, author: str = None) -> str:
        """Create the prompt for the SLM"""
        
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
        """Parse the SLM response into 3 separate posts"""
        
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
    
    def list_available_models(self) -> List[str]:
        """
        List all available models in Ollama
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            response.raise_for_status()
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except Exception as e:
            raise Exception(f"Error listing models: {str(e)}")


def test_repurposer_slm():
    """Test the SLM content repurposer"""
    try:
        # Initialize with default settings
        repurposer = ContentRepurposerSLM()
        
        # List available models
        print("Available models:")
        models = repurposer.list_available_models()
        for model in models:
            print(f"  - {model}")
        print()
        
        sample_content = """
        Just learned that 80% of software bugs come from 20% of the code. 
        This Pareto principle applies everywhere! Focus on the critical 20% that matters most.
        """
        
        print(f"Generating LinkedIn posts using {repurposer.model_name}...")
        print("This may take a moment with local models...\n")
        
        posts = repurposer.generate_linkedin_posts(sample_content, "twitter", "Tech Influencer")
        
        for i, post in enumerate(posts, 1):
            print(f"\n{'='*50}")
            print(f"VARIATION {i}:")
            print(f"{'='*50}")
            print(post)
            print()
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nMake sure Ollama is installed and running:")
        print("  1. Install Ollama from https://ollama.ai")
        print("  2. Run: ollama pull llama3.2")
        print("  3. Start Ollama service")


if __name__ == "__main__":
    test_repurposer_slm()
