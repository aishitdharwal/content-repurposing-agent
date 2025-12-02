"""
Example usage of the Content Repurposing Agent
"""
from scraper import ContentScraper
from llm_service import ContentRepurposer
import os
from dotenv import load_dotenv

load_dotenv()


def example_1_scrape_and_generate():
    """Example: Scrape from URL and generate posts"""
    print("Example 1: Scraping and Generating from URL")
    print("=" * 60)
    
    # Initialize
    scraper = ContentScraper()
    repurposer = ContentRepurposer()
    
    # Your URL here
    url = "https://www.reddit.com/r/Python/comments/example/"
    
    # Scrape
    print(f"Scraping: {url}")
    content_data = scraper.scrape(url)
    
    # Generate
    print(f"\nGenerating LinkedIn posts from {content_data['platform']}...")
    posts = repurposer.generate_linkedin_posts(
        original_content=content_data['content'],
        platform=content_data['platform'],
        author=content_data['author']
    )
    
    # Display
    for i, post in enumerate(posts, 1):
        print(f"\n--- Variation {i} ---")
        print(post)


def example_2_manual_input():
    """Example: Generate from manual input"""
    print("Example 2: Generating from Manual Input")
    print("=" * 60)
    
    repurposer = ContentRepurposer()
    
    # Your content
    content = """
    Hot take: Most productivity advice is terrible.
    
    People say "wake up at 5am" or "hustle 24/7"
    
    But the real productivity hack?
    
    → Work on the right things
    → Say no to everything else
    → Rest when you need to
    
    Focus beats hustle. Every. Single. Time.
    """
    
    # Generate
    print("Generating LinkedIn posts...")
    posts = repurposer.generate_linkedin_posts(
        original_content=content,
        platform='twitter',
        author='Productivity Expert'
    )
    
    # Display
    for i, post in enumerate(posts, 1):
        print(f"\n--- Variation {i} ---")
        print(post)


def example_3_customize_prompt():
    """Example: Customize the generation (advanced)"""
    print("Example 3: Custom Generation")
    print("=" * 60)
    
    # For advanced users who want to customize the prompts
    # You can modify the _create_prompt method in llm_service.py
    # or create a custom repurposer class
    
    print("To customize prompts, edit the _create_prompt method in llm_service.py")
    print("You can adjust:")
    print("- Tone and style")
    print("- Post length")
    print("- Number of hashtags")
    print("- Call-to-action types")
    print("- Industry-specific terminology")


if __name__ == "__main__":
    print("\n🚀 Content Repurposing Agent - Examples\n")
    
    choice = input("Select example (1/2/3): ")
    
    if choice == "1":
        example_1_scrape_and_generate()
    elif choice == "2":
        example_2_manual_input()
    elif choice == "3":
        example_3_customize_prompt()
    else:
        print("Invalid choice. Running example 2...")
        example_2_manual_input()
