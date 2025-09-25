import requests
import json
from typing import Dict, Any
from config import Config

class CompositionAgent:
    """Agent for composing final visual from multiple elements."""
    
    def __init__(self):
        self.bannerbear_api_key = "your-bannerbear-api-key"  # Get from bannerbear.com
    
    def create_composition(self, visual_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Compose final visual using external composition API."""
        
        try:
            return self._compose_with_bannerbear(visual_elements)
        except Exception as e:
            # Fallback: Return elements for frontend composition
            return {
                'type': 'frontend_composition',
                'elements': visual_elements,
                'canvas_size': [Config.CANVAS_WIDTH, Config.CANVAS_HEIGHT],
                'fallback': True
            }
    
    def _compose_with_bannerbear(self, visual_elements: Dict[str, Any]) -> Dict[str, Any]:
        """Use Bannerbear API for professional composition."""
        
        # Create composition template
        template_data = {
            "width": Config.CANVAS_WIDTH,
            "height": Config.CANVAS_HEIGHT,
            "layers": []
        }
        
        # Add background if available
        if visual_elements.get('background'):
            template_data['layers'].append({
                "name": "background",
                "src": visual_elements['background']['url'],
                "x": 0,
                "y": 0
            })
        
        # Add text elements
        if visual_elements.get('text_elements') and not visual_elements['text_elements'].get('fallback'):
            template_data['layers'].append({
                "name": "text_overlay",
                "src": visual_elements['text_elements']['url'],
                "x": 0,
                "y": 0
            })
        
        # Add shapes
        if visual_elements.get('shapes') and not visual_elements['shapes'].get('fallback'):
            template_data['layers'].append({
                "name": "shapes",
                "src": visual_elements['shapes']['url'],
                "x": 0,
                "y": 0
            })
        
        # Call Bannerbear API
        url = "https://api.bannerbear.com/v2/images"
        headers = {
            "Authorization": f"Bearer {self.bannerbear_api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, headers=headers, json=template_data)
        
        if response.status_code == 200:
            result = response.json()
            return {
                'url': result['image_url'],
                'layers': template_data['layers'],
                'metadata': {
                    'composition_id': result['uid'],
                    'created_at': result['created_at']
                }
            }
        else:
            raise Exception(f"Bannerbear API error: {response.status_code}")

