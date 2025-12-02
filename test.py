"""
Test suite for Content Repurposing Agent
"""
import os
from dotenv import load_dotenv
from scraper import ContentScraper
from llm_service import ContentRepurposer

load_dotenv()


def test_scraper():
    """Test the content scraper"""
    print("=" * 60)
    print("TESTING SCRAPER")
    print("=" * 60)
    
    scraper = ContentScraper()
    
    # Test URLs (use real URLs for actual testing)
    test_urls = {
        'reddit': 'https://www.reddit.com/r/Python/comments/1h5wm7w/what_are_some_good_resources_to_learn_python/',
        # Add real Twitter and LinkedIn URLs here for testing
    }
    
    for platform, url in test_urls.items():
        print(f"\n📍 Testing {platform.upper()} scraper...")
        print(f"URL: {url}")
        try:
            result = scraper.scrape(url)
            print(f"\n✅ Success!")
            print(f"Platform: {result['platform']}")
            print(f"Author: {result['author']}")
            print(f"Content Preview: {result['content'][:200]}...")
            print(f"Error: {result.get('error', False)}")
        except Exception as e:
            print(f"\n❌ Failed: {str(e)}")
    
    print("\n" + "=" * 60)


def test_llm_service():
    """Test the LLM service"""
    print("=" * 60)
    print("TESTING LLM SERVICE")
    print("=" * 60)
    
    # Check if API key exists
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n❌ Error: ANTHROPIC_API_KEY not found in environment variables")
        print("Please set your API key in .env file")
        return
    
    print(f"\n✅ API Key found: {api_key[:10]}...")
    
    # Test content
    sample_content = """
    Just discovered something mind-blowing about productivity:
    
    The best developers don't write more code—they write LESS.
    
    Why? Because they:
    • Think deeply before coding
    • Use existing solutions smartly
    • Delete ruthlessly
    • Refactor constantly
    
    Quality > Quantity. Always.
    """
    
    try:
        print("\n🤖 Initializing ContentRepurposer...")
        repurposer = ContentRepurposer(api_key=api_key)
        
        print("📝 Generating LinkedIn posts...")
        posts = repurposer.generate_linkedin_posts(
            original_content=sample_content,
            platform='twitter',
            author='Test User'
        )
        
        print(f"\n✅ Successfully generated {len(posts)} variations!")
        
        for i, post in enumerate(posts, 1):
            print(f"\n{'=' * 60}")
            print(f"VARIATION {i}")
            print(f"{'=' * 60}")
            print(post)
            print(f"Character count: {len(post)}")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    print("\n" + "=" * 60)


def test_end_to_end():
    """Test the entire pipeline"""
    print("=" * 60)
    print("TESTING END-TO-END PIPELINE")
    print("=" * 60)
    
    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n❌ Error: ANTHROPIC_API_KEY not found")
        return
    
    # Use a real Reddit URL for testing (most reliable)
    test_url = 'https://www.reddit.com/r/Python/comments/1h5wm7w/what_are_some_good_resources_to_learn_python/'
    
    print(f"\n📍 Testing with URL: {test_url}")
    
    try:
        # Step 1: Scrape
        print("\n1️⃣ Scraping content...")
        scraper = ContentScraper()
        scraped_data = scraper.scrape(test_url)
        
        if scraped_data.get('error'):
            print(f"⚠️ Scraping warning: {scraped_data['content']}")
            return
        
        print(f"✅ Scraped from {scraped_data['platform']}")
        print(f"   Author: {scraped_data['author']}")
        print(f"   Content length: {len(scraped_data['content'])} characters")
        
        # Step 2: Generate posts
        print("\n2️⃣ Generating LinkedIn posts...")
        repurposer = ContentRepurposer(api_key=api_key)
        posts = repurposer.generate_linkedin_posts(
            original_content=scraped_data['content'],
            platform=scraped_data['platform'],
            author=scraped_data['author']
        )
        
        print(f"✅ Generated {len(posts)} variations")
        
        # Step 3: Display results
        print("\n3️⃣ Results:")
        for i, post in enumerate(posts, 1):
            print(f"\n{'─' * 60}")
            print(f"Variation {i}:")
            print(f"{'─' * 60}")
            print(post[:200] + "..." if len(post) > 200 else post)
        
        print("\n✅ END-TO-END TEST PASSED!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)


def main():
    """Run all tests"""
    print("\n🧪 CONTENT REPURPOSING AGENT - TEST SUITE\n")
    
    # Test 1: Scraper
    test_scraper()
    input("\n⏸️  Press Enter to continue to LLM tests...")
    
    # Test 2: LLM Service
    test_llm_service()
    input("\n⏸️  Press Enter to continue to end-to-end test...")
    
    # Test 3: End-to-end
    test_end_to_end()
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    main()
