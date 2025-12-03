"""
FastAPI application for Content Repurposing Agent
"""
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from scraper import ContentScraper
from llm_service import ContentRepurposer
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Content Repurposing Agent")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize services
scraper = ContentScraper()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/scrape")
async def scrape_content(url: str = Form(...)):
    """Scrape content from URL"""
    try:
        result = scraper.scrape(url)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )

@app.post("/api/generate")
async def generate_posts(
    content: str = Form(...),
    platform: str = Form(...),
    author: str = Form(default="Unknown"),
    api_key: str = Form(...)
):
    """Generate LinkedIn posts from content"""
    try:
        repurposer = ContentRepurposer(api_key=api_key)
        posts = repurposer.generate_linkedin_posts(
            original_content=content,
            platform=platform,
            author=author
        )
        return JSONResponse(content={"posts": posts})
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )

@app.post("/api/scrape-and-generate")
async def scrape_and_generate(
    url: str = Form(None),
    manual_content: str = Form(None),
    platform: str = Form(...),
    api_key: str = Form(...)
):
    """Combined endpoint - scrape URL or use manual content, then generate posts"""
    try:
        # Get content
        if url:
            scraped_data = scraper.scrape(url)
            if scraped_data.get('error'):
                return JSONResponse(
                    content={"error": scraped_data['content']},
                    status_code=400
                )
            content = scraped_data['content']
            platform = scraped_data['platform']
            author = scraped_data['author']
        else:
            content = manual_content
            author = "Manual Input"
        
        # Generate posts
        repurposer = ContentRepurposer(api_key=api_key)
        posts = repurposer.generate_linkedin_posts(
            original_content=content,
            platform=platform,
            author=author
        )
        
        return JSONResponse(content={
            "success": True,
            "scraped_content": content,
            "platform": platform,
            "author": author,
            "posts": posts
        })
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=400
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
