import google.generativeai as genai
from config import Config
import json
import base64
from PIL import Image
import io  


class FreeGeminiService:
    """FREE Google Gemini API service."""
    
    def __init__(self):
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def generate_response(self, question: str, system_prompt: str) -> str:
        """Generate response using FREE Gemini API."""
        try:
            # Combine system prompt with question
            full_prompt = f"{system_prompt}\n\nUser Question: {question}"
            
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            raise Exception(f"FREE Gemini API error: {str(e)}")

    def analyze_image_for_positioning(self, image_data: str, concept: str) -> dict:
        """Analyze generated image to determine optimal element positioning."""
        
        # Convert base64 to PIL Image for Gemini
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        prompt = f"""Analyze this educational image about "{concept}".

                    Canvas dimensions: 1024x768 pixels.

                    Identify and return JSON with exact coordinates:
                    {{
                        "main_elements": [
                        {{"name": "ocean", "center": [x, y], "bounds": [x1, y1, x2, y2]}},
                        {{"name": "mountains", "center": [x, y], "bounds": [x1, y1, x2, y2]}},
                        {{"name": "sky", "center": [x, y], "bounds": [x1, y1, x2, y2]}}
                        ],
                        "text_positions": [
                        {{"label": "EVAPORATION", "optimal_xy": [x, y], "region": "near_ocean"}},
                        {{"label": "CONDENSATION", "optimal_xy": [x, y], "region": "near_clouds"}}
                        ],
                        "arrow_paths": [
                        {{"from": [x1, y1], "to": [x2, y2], "purpose": "evaporation_flow"}}
                        ]
                    }}

                    Be precise with coordinates. Avoid placing text over complex image areas."""

        try:
            response = self.model.generate_content([prompt, image])
            return json.loads(response.text)
        except Exception as e:
            # Fallback to basic positioning
            return {
                "main_elements": [
                    {"name": "center", "center": [512, 384], "bounds": [0, 0, 1024, 768]}
                ],
                "text_positions": [
                    {"label": "TITLE", "optimal_xy": [512, 100], "region": "top_center"}
                ],
                "arrow_paths": []
            }
