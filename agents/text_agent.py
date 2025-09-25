import requests
import json
from typing import List, Dict, Any
from config import Config

class TextRenderingAgent:
    """Agent for rendering text overlays and simple shapes using external APIs."""
    
    def __init__(self):
        self.htmlcss_api_key = "your-htmlcss-api-key"  # Get from htmlcsstoimage.com
    
    def render_text_elements(self, text_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Render text overlays using HTML/CSS to Image API."""
        
        # Create HTML template for text rendering
        html_content = self._create_text_html(text_specs)
        
        try:
            return self._render_with_htmlcss_api(html_content)
        except Exception as e:
            # Fallback: Return text positioning data for frontend rendering
            return {
                'type': 'text_data',
                'elements': text_specs,
                'fallback': True
            }
    
    def create_shapes(self, shape_specs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create simple shapes using HTML/CSS."""
        
        html_content = self._create_shapes_html(shape_specs)
        
        try:
            return self._render_with_htmlcss_api(html_content)
        except Exception as e:
            return {
                'type': 'shape_data',
                'elements': shape_specs,
                'fallback': True
            }
    
    def _create_text_html(self, text_specs: List[Dict[str, Any]]) -> str:
        """Create HTML for text rendering."""
        
        html_elements = []
        for spec in text_specs:
            text = spec.get('text', '')
            position = spec.get('position', 'center')
            style = spec.get('style', 'normal')
            
            css_class = f"text-{position} text-{style}"
            html_elements.append(f'<div class="{css_class}">{text}</div>')
        
        css = f"""
        <style>
        body {{ 
            width: {Config.CANVAS_WIDTH}px; 
            height: {Config.CANVAS_HEIGHT}px; 
            margin: 0; 
            position: relative;
            background: transparent;
            font-family: Arial, sans-serif;
        }}
        .text-center {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); }}
        .text-top-left {{ position: absolute; top: 20px; left: 20px; }}
        .text-top-right {{ position: absolute; top: 20px; right: 20px; }}
        .text-title {{ font-size: 24px; font-weight: bold; color: #333; }}
        .text-label {{ font-size: 16px; color: #666; }}
        .text-bold {{ font-weight: bold; }}
        </style>
        """
        
        return f"{css}<body>{''.join(html_elements)}</body>"
    
    def _create_shapes_html(self, shape_specs: List[Dict[str, Any]]) -> str:
        """Create HTML/CSS for simple shapes."""
        
        shapes_html = []
        for spec in shape_specs:
            shape_type = spec.get('type', 'line')
            
            if shape_type == 'arrow':
                from_pos = spec.get('from', [100, 100])
                to_pos = spec.get('to', [200, 200])
                color = spec.get('color', 'red')
                
                # Create CSS arrow
                shapes_html.append(f'''
                <div class="arrow" style="
                    position: absolute;
                    left: {from_pos[0]}px;
                    top: {from_pos[1]}px;
                    width: {abs(to_pos[0] - from_pos[0])}px;
                    height: 2px;
                    background: {color};
                    transform-origin: left;
                "></div>
                ''')
        
        css = f"""
        <style>
        body {{ 
            width: {Config.CANVAS_WIDTH}px; 
            height: {Config.CANVAS_HEIGHT}px; 
            margin: 0; 
            background: transparent;
        }}
        </style>
        """
        
        return f"{css}<body>{''.join(shapes_html)}</body>"
    
    def _render_with_htmlcss_api(self, html_content: str) -> Dict[str, Any]:
        """Render HTML using external API."""
        
        url = "https://hcti.io/v1/image"
        
        data = {
            'html': html_content,
            'width': Config.CANVAS_WIDTH,
            'height': Config.CANVAS_HEIGHT,
            'device_scale_factor': 1
        }
        
        response = requests.post(
            url, 
            json=data,
            auth=(self.htmlcss_api_key, '')  # API key as username
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                'url': result['url'],
                'source': 'htmlcss_api'
            }
        else:
            raise Exception(f"HTML/CSS API error: {response.status_code}")

