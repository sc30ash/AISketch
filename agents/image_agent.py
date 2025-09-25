import replicate
import requests
import base64
from typing import Dict, Any
from config import Config

class ImageGenerationAgent:
    """Agent for generating images using external APIs."""
    
    def __init__(self):
        self.replicate_client = replicate.Client(api_token=Config.REPLICATE_API_TOKEN)
        self.stability_api_key = Config.STABILITY_API_KEY
    
    def generate_image(self, image_spec: Dict[str, Any]) -> Dict[str, Any]:
        """Generate image using Replicate or Stability AI."""
        prompt = image_spec.get('prompt', '')
        style = image_spec.get('style', 'educational')
        
        # Enhance prompt based on style
        enhanced_prompt = self._enhance_prompt(prompt, style)
        
        try:
            # Try Replicate first (Stable Diffusion 3)
            return self._generate_with_replicate(enhanced_prompt)
        except Exception as e:
            try:
                # Fallback to Stability AI
                return self._generate_with_stability(enhanced_prompt)
            except Exception as e2:
                raise Exception(f"All image generation failed: Replicate: {e}, Stability: {e2}")
    
    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """Enhance prompt based on educational context."""
        style_prefixes = {
            'educational': 'Clean educational diagram, simple illustration, ',
            'realistic': 'Photorealistic, high quality, detailed, ',
            'sketch': 'Hand-drawn sketch style, black and white, simple lines, '
        }
        
        prefix = style_prefixes.get(style, '')
        return f"{prefix}{prompt}, white background, educational content"
    
    def _generate_with_replicate(self, prompt: str) -> Dict[str, Any]:
        """Generate image using Replicate API."""
        output = self.replicate_client.run(
            Config.STABLE_DIFFUSION_MODEL,
            input={
                "prompt": prompt,
                "width": Config.CANVAS_WIDTH,
                "height": Config.CANVAS_HEIGHT,
                "num_outputs": 1
            }
        )
        
        return {
            'url': output[0] if isinstance(output, list) else output,
            'source': 'replicate',
            'prompt': prompt
        }
    
    def _generate_with_stability(self, prompt: str) -> Dict[str, Any]:
        """Generate image using Stability AI API."""
        url = "https://api.stability.ai/v2beta/stable-image/generate/ultra"
        
        headers = {
            "Authorization": f"Bearer {self.stability_api_key}",
            "Accept": "image/*"
        }
        
        data = {
            "prompt": prompt,
            "width": Config.CANVAS_WIDTH,
            "height": Config.CANVAS_HEIGHT,
            "output_format": "png"
        }
        
        response = requests.post(url, headers=headers, data=data)
        
        if response.status_code == 200:
            # Convert binary to base64 data URL
            image_data = base64.b64encode(response.content).decode()
            return {
                'url': f"data:image/png;base64,{image_data}",
                'source': 'stability',
                'prompt': prompt
            }
        else:
            raise Exception(f"Stability API error: {response.status_code}")

