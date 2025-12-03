# Changes Summary - LLM/SLM Selection Feature

## Overview
Added functionality to allow users to choose between LLM (Cloud-based Anthropic Claude) and SLM (Local Ollama on EC2) for content generation.

## Files Modified

### 1. `templates/index.html`
**Changes:**
- Added radio button selection for "LLM" vs "SLM" model types
- Made API Key field conditional (only shows when LLM is selected)
- Added Base URL field (only shows when SLM is selected)
- Added `toggleModelFields()` JavaScript function to handle field visibility
- Updated `generatePosts()` function to:
  - Validate based on selected model type
  - Send `model_type` parameter to backend
  - Send either `api_key` (for LLM) or `base_url` (for SLM)

**UI Changes:**
- Radio buttons for model selection (LLM/SLM)
- Dynamic form fields that show/hide based on selection
- Default value for Base URL: `http://localhost:11434`
- Helper text for EC2 IP address input

### 2. `main.py`
**Changes:**
- Updated `/api/scrape-and-generate` endpoint signature:
  - Added `model_type: str = Form(...)`
  - Changed `api_key: str = Form(None)` (now optional)
  - Added `base_url: str = Form(None)`
- Added logic to instantiate the correct repurposer based on `model_type`:
  - If `model_type == "llm"`: Use `ContentRepurposer(api_key=api_key)`
  - If `model_type == "slm"`: Use `ContentRepurposerSLM(base_url=base_url)`
- Added validation to ensure required fields are provided for each model type

### 3. `slm_service.py` (Already Created)
**Features:**
- `ContentRepurposerSLM` class with same interface as `ContentRepurposer`
- Uses Ollama REST API for local model inference
- Configurable base URL for remote EC2 deployment
- Same methods: `generate_linkedin_posts()`, `_create_prompt()`, `_parse_response()`
- Additional method: `list_available_models()`

## How It Works

### User Flow:
1. User selects model type (LLM or SLM) via radio buttons
2. Based on selection:
   - **LLM selected**: API Key field appears
   - **SLM selected**: Base URL field appears
3. User enters their content and clicks "Generate"
4. Frontend sends `model_type` + appropriate credentials to backend
5. Backend routes to correct service (LLM or SLM)
6. Posts are generated and displayed

### Backend Logic:
```python
if model_type == "llm":
    repurposer = ContentRepurposer(api_key=api_key)
else:  # slm
    repurposer = ContentRepurposerSLM(base_url=base_url)

posts = repurposer.generate_linkedin_posts(...)
```

## Deployment Notes

### App Runner (Frontend)
- No changes needed to deployment configuration
- Both `llm_service.py` and `slm_service.py` must be deployed
- `requirements.txt` already includes `requests` library

### EC2 (SLM Backend)
- Ollama must be running on specified port (default: 11434)
- Security group must allow inbound traffic on port 11434
- User enters EC2 public IP in format: `http://YOUR-EC2-IP:11434`

## Testing

### Test LLM Mode:
1. Select "LLM (Cloud - Anthropic Claude)"
2. Enter valid Anthropic API key
3. Paste content and generate

### Test SLM Mode:
1. Select "SLM (Local - Ollama)"
2. Enter EC2 base URL (e.g., `http://3.110.232.158:11434`)
3. Paste content and generate

## Benefits
- **Flexibility**: Users can choose between cloud and local models
- **Cost Control**: Option to use local SLM to save on API costs
- **No Breaking Changes**: Existing LLM functionality remains intact
- **Clean Architecture**: Both services implement the same interface
