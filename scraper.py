"""
Content scraper for Twitter, LinkedIn, and Reddit posts
"""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import re


class ContentScraper:
    """Scrapes content from various social media platforms"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def scrape(self, url: str) -> Dict[str, str]:
        """
        Main scraping method that routes to appropriate scraper based on URL
        
        Args:
            url: URL of the social media post
            
        Returns:
            Dictionary containing platform, content, and author information
        """
        if 'twitter.com' in url or 'x.com' in url:
            return self._scrape_twitter(url)
        elif 'linkedin.com' in url:
            return self._scrape_linkedin(url)
        elif 'reddit.com' in url:
            return self._scrape_reddit(url)
        else:
            raise ValueError(f"Unsupported platform. URL: {url}")
    
    def _scrape_twitter(self, url: str) -> Dict[str, str]:
        """
        Scrape Twitter/X post
        Note: Twitter requires authentication for most scraping. 
        This is a basic implementation that may not work for all cases.
        For production, consider using Twitter API or services like nitter.net
        """
        try:
            # Try to use nitter as a fallback (public Twitter frontend)
            nitter_url = url.replace('twitter.com', 'nitter.net').replace('x.com', 'nitter.net')
            
            response = requests.get(nitter_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract tweet content
            tweet_content = soup.find('div', class_='tweet-content')
            content = tweet_content.get_text(strip=True) if tweet_content else ""
            
            # Extract author
            author_elem = soup.find('a', class_='fullname')
            author = author_elem.get_text(strip=True) if author_elem else "Unknown"
            
            if not content:
                return {
                    'platform': 'twitter',
                    'content': 'Unable to scrape Twitter content. Please provide the tweet text manually.',
                    'author': 'Unknown',
                    'error': True
                }
            
            return {
                'platform': 'twitter',
                'content': content,
                'author': author,
                'error': False
            }
        except Exception as e:
            return {
                'platform': 'twitter',
                'content': f'Error scraping Twitter: {str(e)}. Please provide the tweet text manually.',
                'author': 'Unknown',
                'error': True
            }
    
    def _scrape_linkedin(self, url: str) -> Dict[str, str]:
        """
        Scrape LinkedIn post
        Note: LinkedIn heavily restricts scraping and requires authentication.
        This is a basic implementation for demonstration purposes.
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # LinkedIn's structure varies, this is a basic attempt
            # Look for meta tags that might contain the content
            og_description = soup.find('meta', property='og:description')
            content = og_description['content'] if og_description else ""
            
            # Try to find title/author
            og_title = soup.find('meta', property='og:title')
            author = og_title['content'] if og_title else "Unknown"
            
            if not content:
                return {
                    'platform': 'linkedin',
                    'content': 'Unable to scrape LinkedIn content due to authentication requirements. Please provide the post text manually.',
                    'author': 'Unknown',
                    'error': True
                }
            
            return {
                'platform': 'linkedin',
                'content': content,
                'author': author,
                'error': False
            }
        except Exception as e:
            return {
                'platform': 'linkedin',
                'content': f'Error scraping LinkedIn: {str(e)}. Please provide the post text manually.',
                'author': 'Unknown',
                'error': True
            }
    
    def _scrape_reddit(self, url: str) -> Dict[str, str]:
        """
        Scrape Reddit post
        Reddit is more scraping-friendly than other platforms
        """
        try:
            # Add .json to the URL to get JSON response
            json_url = url.rstrip('/') + '.json'
            
            # Update headers to look more like a real browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/html',
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            response = requests.get(json_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '')
            if 'json' not in content_type.lower():
                raise ValueError("Reddit returned HTML instead of JSON. The URL may be invalid or Reddit is blocking the request.")
            
            data = response.json()
            
            # Extract post data
            post_data = data[0]['data']['children'][0]['data']
            
            title = post_data.get('title', '')
            selftext = post_data.get('selftext', '')
            author = post_data.get('author', 'Unknown')
            
            # Combine title and selftext
            content = f"{title}\n\n{selftext}" if selftext else title
            
            return {
                'platform': 'reddit',
                'content': content,
                'author': f"u/{author}",
                'error': False
            }
        except Exception as e:
            return {
                'platform': 'reddit',
                'content': f'Error scraping Reddit: {str(e)}. Please provide the post text manually.',
                'author': 'Unknown',
                'error': True
            }


def test_scraper():
    """Test the scraper with sample URLs"""
    scraper = ContentScraper()
    
    # Test Reddit (most reliable)
    reddit_url = "https://www.reddit.com/r/Python/comments/example/"
    print("Testing Reddit scraper...")
    result = scraper.scrape(reddit_url)
    print(f"Platform: {result['platform']}")
    print(f"Content: {result['content'][:100]}...")
    print(f"Author: {result['author']}")
    print()


if __name__ == "__main__":
    test_scraper()
