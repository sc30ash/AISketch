# Create: agents/visual_agent.py
from services.gemini_service import FreeGeminiService
import json

class VisualStyleAgent:
    """Agent that determines colors, shapes, and visual metaphors for educational impact."""
    
    def __init__(self):
        self.gemini = FreeGeminiService()
        self.educational_colors = {
            'primary': '#4A90E2',      # Professional blue
            'secondary': '#50C878',    # Educational green  
            'accent': '#FF6B6B',       # Attention red
            'process': '#FFD700',      # Process yellow
            'neutral': '#8E8E93',      # Supporting gray
            'background': '#F8F9FA'    # Clean background
        }
    
    def design_visuals(self, content_analysis: dict, layout_plan: dict) -> dict:
        """Choose optimal visual elements for educational clarity."""
        
        system_prompt = f"""You are a visual design expert for educational content.

CONTENT: {json.dumps(content_analysis, indent=2)}
LAYOUT: {json.dumps(layout_plan, indent=2)}

Choose the best visual representation for each element to maximize learning.

Available shapes: circle, rectangle, ellipse, triangle, polygon, path
Available patterns: solid, gradient, dashed, dotted
Educational color palette: {json.dumps(self.educational_colors)}
Make sure that the shape elements are always light color, and arrows, lines and text are always black or dark color.

Respond with JSON:
{{
  "visual_elements": [
    {{
      "name": "element_name",
      "shape": "circle|rectangle|ellipse|triangle|custom_path",
      "fill_color": "#color_hex",
      "stroke_color": "#color_hex", 
      "stroke_width": 2,
      "pattern": "solid|gradient|dashed",
      "visual_metaphor": "what this shape represents",
      "educational_purpose": "why this visual choice helps learning"
    }}
  ],
  "connection_styles": [
    {{
      "from": "element1", 
      "to": "element2",
      "arrow_style": "simple|curved|double|dashed",
      "color": "#color_hex",
      "thickness": 2,
      "animation_hint": "none|flow|pulse|grow"
    }}
  ],
  "text_styles": [
    {{
      "type": "title|label|annotation",
      "font_size": 16,
      "color": "#color_hex",
      "weight": "normal|bold",
      "emphasis": "none|highlight|callout"
    }}
  ],
  "overall_theme": "modern|friendly|scientific|playful",
  "accessibility_notes": "Color blind considerations, contrast ratios"
}}

Prioritize educational clarity over visual complexity."""

        try:
            response = self.gemini.generate_response("", system_prompt)
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                return self._create_fallback_visuals(layout_plan)
                
        except Exception as e:
            print(f"Visual design error: {e}")
            return self._create_fallback_visuals(layout_plan)
    
    def _create_fallback_visuals(self, layout_plan: dict) -> dict:
        """Clean, simple visual defaults."""
        elements = layout_plan.get('element_positions', [])
        visual_elements = []
        
        color_cycle = ['#4A90E2', '#50C878', '#FF6B6B', '#FFD700', '#8E8E93']
        
        for i, element in enumerate(elements):
            visual_elements.append({
                "name": element['name'],
                "shape": "rectangle",
                "fill_color": color_cycle[i % len(color_cycle)],
                "stroke_color": "#2C3E50",
                "stroke_width": 2,
                "pattern": "solid",
                "visual_metaphor": "Educational block",
                "educational_purpose": "Clear visual separation"
            })
        
        return {
            "visual_elements": visual_elements,
            "connection_styles": [],
            "text_styles": [
                {"type": "title", "font_size": 24, "color": "#2C3E50", "weight": "bold"},
                {"type": "label", "font_size": 14, "color": "#34495E", "weight": "normal"}
            ],
            "overall_theme": "clean",
            "accessibility_notes": "High contrast, colorblind safe"
        }
