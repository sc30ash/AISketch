import os
import base64
import io
from typing import Dict, Any
from huggingface_hub import InferenceClient
from config import Config

class FreeHuggingFaceService:
    """FREE HuggingFace Inference API service using InferenceClient."""
    
    def __init__(self):
        # Use the modern InferenceClient
        self.client = InferenceClient(
            api_key=Config.HUGGINGFACE_TOKEN  # Will use HF_TOKEN env var
        )
    
    def generate_image(self, prompt: str) -> Dict[str, Any]:
        """Generate image using FREE HuggingFace InferenceClient."""
        
        # Enhanced prompt for educational content
        enhanced_prompt = f"Educational diagram, simple illustration, {prompt}, white background, clean art style"
        
        try:
            print(f"🎨 Generating image with HF InferenceClient: {enhanced_prompt}")
            
            # Use the modern text_to_image method
            pil_image = self.client.text_to_image(
                enhanced_prompt,
                model=Config.STABLE_DIFFUSION_MODEL
            )
            
            print("✅ PIL Image generated successfully")
            
            # Convert PIL Image to base64
            buffer = io.BytesIO()
            pil_image.save(buffer, format='PNG')
            buffer.seek(0)
            
            image_data = base64.b64encode(buffer.getvalue()).decode()
            print("✅ Image converted to base64")
            
            return {
                'data': f"data:image/png;base64,{image_data}",
                'source': 'huggingface_free',
                'prompt': enhanced_prompt,
                'model': Config.STABLE_DIFFUSION_MODEL
            }
            
        except Exception as e:
            error_msg = f"FREE HuggingFace InferenceClient error: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

    
    def query_text_model(self, prompt: str, model: str = "microsoft/DialoGPT-medium") -> str:
        """Query FREE text model if needed."""
        model_url = f"{self.base_url}{model}"
        
        payload = {"inputs": prompt}
        response = requests.post(model_url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        else:
            raise Exception(f"Text model error: {response.status_code}")
