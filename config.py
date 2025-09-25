import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
    HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_TOKEN')
    PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

    # Canvas settings
    CANVAS_WIDTH = 1024
    CANVAS_HEIGHT = 768
    
    # Models
    GEMINI_MODEL = "gemini-2.5-flash"
    STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
    USE_PERPLEXITY_FOR_CONTENT = True  # Toggle to enable/disable
    USE_PERPLEXITY_FOR_CONTENT = True
    USE_PERPLEXITY_FOR_LAYOUT = True
    
    # Rate limits (FREE tier)
    GEMINI_RATE_LIMIT = 15
    HF_RATE_LIMIT = 300



    
    
    
    # Model selection
    PERPLEXITY_MODEL = "llama-3.1-sonar-huge-128k-online"
    
    # Rate limiting
    PERPLEXITY_RATE_LIMIT = 1.0  # seconds between calls
