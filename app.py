"""
Streamlit UI for Content Repurposing Agent
"""
import streamlit as st
from scraper import ContentScraper
from llm_service import ContentRepurposer
import os
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Content Repurposing Agent",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #0077B5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .variation-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #0077B5;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #0077B5;
        color: white;
        font-weight: bold;
    }
    .success-message {
        padding: 10px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    .error-message {
        padding: 10px;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'generated_posts' not in st.session_state:
    st.session_state.generated_posts = None
if 'scraped_content' not in st.session_state:
    st.session_state.scraped_content = None


def main():
    # Header
    st.markdown('<h1 class="main-header">🔄 Content Repurposing Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform your social media content into engaging LinkedIn posts</p>', unsafe_allow_html=True)
    
    # Sidebar for API key configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        api_key = st.text_input(
            "Anthropic API Key",
            value=os.getenv('ANTHROPIC_API_KEY', ''),
            type="password",
            help="Enter your Anthropic API key. You can get one at https://console.anthropic.com/"
        )
        
        st.markdown("---")
        st.markdown("### Supported Platforms")
        st.markdown("✅ Twitter/X")
        st.markdown("✅ LinkedIn")
        st.markdown("✅ Reddit")
        
        st.markdown("---")
        st.markdown("### How to Use")
        st.markdown("1. Paste a URL from Twitter, LinkedIn, or Reddit")
        st.markdown("2. Click 'Scrape & Generate'")
        st.markdown("3. Review 3 variations of LinkedIn posts")
        st.markdown("4. Copy your favorite version")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📎 Input Content")
        
        # Tab for URL or Manual input
        tab1, tab2 = st.tabs(["🔗 URL Input", "✍️ Manual Input"])
        
        with tab1:
            url = st.text_input(
                "Enter Social Media URL",
                placeholder="https://twitter.com/username/status/... or https://reddit.com/r/...",
                help="Paste the URL of the tweet, LinkedIn post, or Reddit thread you want to repurpose"
            )
            
            if st.button("🔍 Scrape & Generate", key="scrape_btn", use_container_width=True):
                if not url:
                    st.error("⚠️ Please enter a URL")
                elif not api_key:
                    st.error("⚠️ Please enter your Anthropic API key in the sidebar")
                else:
                    with st.spinner("Scraping content..."):
                        try:
                            scraper = ContentScraper()
                            scraped_data = scraper.scrape(url)
                            st.session_state.scraped_content = scraped_data
                            
                            if scraped_data.get('error'):
                                st.warning(f"⚠️ {scraped_data['content']}")
                            else:
                                st.success(f"✅ Successfully scraped content from {scraped_data['platform'].upper()}")
                                
                                # Display scraped content
                                with st.expander("📄 View Scraped Content", expanded=True):
                                    st.markdown(f"**Platform:** {scraped_data['platform'].upper()}")
                                    st.markdown(f"**Author:** {scraped_data['author']}")
                                    st.markdown("**Content:**")
                                    st.text_area("", scraped_data['content'], height=150, disabled=True)
                                
                                # Generate LinkedIn posts
                                with st.spinner("Generating LinkedIn variations..."):
                                    repurposer = ContentRepurposer(api_key=api_key)
                                    posts = repurposer.generate_linkedin_posts(
                                        original_content=scraped_data['content'],
                                        platform=scraped_data['platform'],
                                        author=scraped_data['author']
                                    )
                                    st.session_state.generated_posts = posts
                                    st.success("✅ Generated 3 LinkedIn post variations!")
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        with tab2:
            manual_content = st.text_area(
                "Paste Content Manually",
                height=200,
                placeholder="If scraping doesn't work, paste the content here manually..."
            )
            
            platform_manual = st.selectbox(
                "Select Source Platform",
                ["twitter", "linkedin", "reddit"]
            )
            
            if st.button("✨ Generate from Manual Input", key="manual_btn", use_container_width=True):
                if not manual_content:
                    st.error("⚠️ Please enter some content")
                elif not api_key:
                    st.error("⚠️ Please enter your Anthropic API key in the sidebar")
                else:
                    with st.spinner("Generating LinkedIn variations..."):
                        try:
                            repurposer = ContentRepurposer(api_key=api_key)
                            posts = repurposer.generate_linkedin_posts(
                                original_content=manual_content,
                                platform=platform_manual,
                                author="Manual Input"
                            )
                            st.session_state.generated_posts = posts
                            st.success("✅ Generated 3 LinkedIn post variations!")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
    
    with col2:
        st.subheader("ℹ️ Tips")
        st.info("""
        **Best Practices:**
        - Use high-quality, insightful content
        - Shorter posts work better
        - Content with clear value propositions convert better
        - Include data or statistics for credibility
        """)
    
    # Display generated posts
    if st.session_state.generated_posts:
        st.markdown("---")
        st.subheader("📝 Generated LinkedIn Posts")
        st.markdown("Choose your favorite variation and customize as needed:")
        
        # Display 3 variations side by side
        cols = st.columns(3)
        
        for i, (col, post) in enumerate(zip(cols, st.session_state.generated_posts), 1):
            with col:
                st.markdown(f"### Variation {i}")
                
                variation_style = ["🎭 Storytelling", "📊 Analytical", "💬 Conversational"]
                st.caption(variation_style[i-1])
                
                # Display post in a text area for easy editing
                edited_post = st.text_area(
                    f"Post {i}",
                    value=post,
                    height=400,
                    key=f"post_{i}",
                    label_visibility="collapsed"
                )
                
                # Copy button
                if st.button(f"📋 Copy Variation {i}", key=f"copy_{i}", use_container_width=True):
                    st.code(edited_post, language=None)
                    st.success(f"Variation {i} ready to copy!")
        
        # Add a reset button
        if st.button("🔄 Start Over", use_container_width=True):
            st.session_state.generated_posts = None
            st.session_state.scraped_content = None
            st.rerun()


if __name__ == "__main__":
    main()
