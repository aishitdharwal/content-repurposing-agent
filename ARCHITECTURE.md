# System Architecture Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                     (Browser UI)                             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Input (URL/Text)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   STREAMLIT APP (app.py)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   Sidebar    │  │  Input Tabs  │  │  Output Display │  │
│  │  - API Key   │  │  - URL       │  │  - 3 Columns    │  │
│  │  - Settings  │  │  - Manual    │  │  - Copy Buttons │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└───────────┬──────────────────────────────────┬──────────────┘
            │                                   │
            │ URL                               │ Display
            ▼                                   │
┌─────────────────────────────────────────┐    │
│      SCRAPER MODULE (scraper.py)        │    │
│  ┌────────────────────────────────────┐ │    │
│  │   ContentScraper Class             │ │    │
│  │   - _scrape_twitter()              │ │    │
│  │   - _scrape_linkedin()             │ │    │
│  │   - _scrape_reddit()               │ │    │
│  └────────────────────────────────────┘ │    │
└───────────┬─────────────────────────────┘    │
            │                                   │
            │ Scraped Content                   │
            ▼                                   │
┌─────────────────────────────────────────┐    │
│    LLM SERVICE (llm_service.py)         │    │
│  ┌────────────────────────────────────┐ │    │
│  │   ContentRepurposer Class          │ │    │
│  │   - generate_linkedin_posts()      │ │    │
│  │   - _create_prompt()               │ │    │
│  │   - _parse_response()              │ │    │
│  └────────────────────────────────────┘ │    │
└───────────┬─────────────────────────────┘    │
            │                                   │
            │ API Request                       │
            ▼                                   │
┌─────────────────────────────────────────┐    │
│        ANTHROPIC CLAUDE API             │    │
│   (claude-sonnet-4-20250514)            │    │
└───────────┬─────────────────────────────┘    │
            │                                   │
            │ 3 Variations                      │
            └───────────────────────────────────┘
```

## Data Flow Diagram

```
┌─────────┐
│  User   │
│ Input   │
└────┬────┘
     │
     ├─── URL Input ────────────────┐
     │                              │
     │                              ▼
     │                    ┌──────────────────┐
     │                    │   URL Parser     │
     │                    └────────┬─────────┘
     │                             │
     │                             ▼
     │                    ┌──────────────────┐
     │                    │  Platform Detect │
     │                    │  - Twitter       │
     │                    │  - LinkedIn      │
     │                    │  - Reddit        │
     │                    └────────┬─────────┘
     │                             │
     │                             ▼
     │                    ┌──────────────────┐
     │                    │   HTTP Request   │
     │                    │  BeautifulSoup   │
     │                    └────────┬─────────┘
     │                             │
     └─── Manual Input ────────────┤
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  Content Extract │
                          │  - Text          │
                          │  - Author        │
                          │  - Platform      │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  Prompt Builder  │
                          │  - Context       │
                          │  - Instructions  │
                          │  - Examples      │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │   Claude API     │
                          │   Request        │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  API Response    │
                          │  Processing      │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  Parse 3         │
                          │  Variations      │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  Display in UI   │
                          │  3 Columns       │
                          └────────┬─────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  User Selection  │
                          │  Copy & Use      │
                          └──────────────────┘
```

## Module Interaction Diagram

```
┌────────────────────────────────────────────────────────┐
│                     app.py (Streamlit UI)              │
│                                                        │
│  ┌──────────────┐       ┌──────────────────────────┐ │
│  │  User Input  │       │   Session State          │ │
│  │  Component   │──────▶│   - generated_posts      │ │
│  └──────────────┘       │   - scraped_content      │ │
│         │               └──────────────────────────┘ │
│         │                                            │
│         ▼                                            │
│  ┌──────────────────────────────────────────────┐   │
│  │            Event Handlers                    │   │
│  │  - Button Click: Scrape & Generate           │   │
│  │  - Button Click: Manual Generate             │   │
│  │  - Button Click: Copy Variation              │   │
│  └──────────┬───────────────────────────────────┘   │
└─────────────┼────────────────────────────────────────┘
              │
              ├─────────────────────┬──────────────────┐
              │                     │                  │
              ▼                     ▼                  ▼
    ┌──────────────────┐  ┌──────────────────┐  ┌──────────┐
    │   scraper.py     │  │  llm_service.py  │  │ config.py│
    │                  │  │                  │  │          │
    │ ContentScraper   │  │ ContentRepurposer│  │ Settings │
    │   - scrape()     │  │   - generate()   │  │ Constants│
    │   - _scrape_*()  │  │   - _prompt()    │  │          │
    └──────────────────┘  └──────────────────┘  └──────────┘
              │                     │
              │                     │
              ▼                     ▼
        ┌──────────┐        ┌──────────────┐
        │ requests │        │  anthropic   │
        │ BS4      │        │  API client  │
        └──────────┘        └──────────────┘
```

## Component Responsibilities

```
┌─────────────────────────────────────────────────────┐
│                     app.py                          │
│  Responsibilities:                                  │
│  • UI rendering                                     │
│  • User input handling                              │
│  • State management                                 │
│  • Component orchestration                          │
│  • Display results                                  │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                  scraper.py                         │
│  Responsibilities:                                  │
│  • URL validation                                   │
│  • Platform detection                               │
│  • HTTP requests                                    │
│  • HTML parsing                                     │
│  • Content extraction                               │
│  • Error handling                                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                llm_service.py                       │
│  Responsibilities:                                  │
│  • API client initialization                        │
│  • Prompt construction                              │
│  • API request/response                             │
│  • Response parsing                                 │
│  • Variation extraction                             │
│  • Error handling                                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│                   config.py                         │
│  Responsibilities:                                  │
│  • Configuration constants                          │
│  • Model settings                                   │
│  • Platform definitions                             │
│  • Style configurations                             │
└─────────────────────────────────────────────────────┘
```

## State Flow

```
Initial State:
┌──────────────────────────┐
│ generated_posts: None    │
│ scraped_content: None    │
└──────────────────────────┘
            │
            │ User enters URL
            ▼
After Scraping:
┌──────────────────────────┐
│ generated_posts: None    │
│ scraped_content: {       │
│   platform: "reddit",    │
│   content: "...",        │
│   author: "u/username"   │
│ }                        │
└──────────────────────────┘
            │
            │ Generate posts
            ▼
After Generation:
┌──────────────────────────┐
│ generated_posts: [       │
│   "Variation 1...",      │
│   "Variation 2...",      │
│   "Variation 3..."       │
│ ]                        │
│ scraped_content: {...}   │
└──────────────────────────┘
            │
            │ User clicks "Start Over"
            ▼
Back to Initial State
```

## Error Handling Flow

```
User Input
    │
    ▼
┌────────────────┐
│ Validate Input │
└───────┬────────┘
        │
    ┌───┴───┐
    │ Valid?│
    └───┬───┘
        │
  ┌─────┴─────┐
  No          Yes
  │            │
  ▼            ▼
Display    Try Scrape
Error          │
          ┌────┴────┐
          │ Success?│
          └────┬────┘
               │
         ┌─────┴─────┐
         No          Yes
         │            │
         ▼            ▼
    Fallback to   Try Generate
    Manual Input      │
                 ┌────┴────┐
                 │ Success?│
                 └────┬────┘
                      │
                ┌─────┴─────┐
                No          Yes
                │            │
                ▼            ▼
           Show Error    Display
           + Retry      Results
```

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Development Environment         │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  Local Machine                 │    │
│  │  - Python 3.8+                 │    │
│  │  - Virtual Environment         │    │
│  │  - Dependencies installed      │    │
│  │  - .env file configured        │    │
│  └────────────────────────────────┘    │
│                 │                       │
│                 │ streamlit run app.py  │
│                 ▼                       │
│  ┌────────────────────────────────┐    │
│  │  Streamlit Server              │    │
│  │  localhost:8501                │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
                 │
                 │ HTTP Requests
                 ▼
┌─────────────────────────────────────────┐
│         External Services               │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  Anthropic API                 │    │
│  │  api.anthropic.com             │    │
│  └────────────────────────────────┘    │
│                                         │
│  ┌────────────────────────────────┐    │
│  │  Social Media Platforms        │    │
│  │  - reddit.com (JSON API)       │    │
│  │  - nitter.net (Twitter)        │    │
│  │  - linkedin.com (scraping)     │    │
│  └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

**Legend:**
- `┌─┐` Box: Component/Module
- `│` Line: Connection
- `▼` Arrow: Data flow direction
- `├─┤` Split: Multiple paths

---

Last Updated: December 2024
