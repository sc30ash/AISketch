# Create: agents/layout_agent.py
from services.gemini_service import FreeGeminiService
from services.perplexity_service import PerplexityService
import json
from config import Config
import re

class LayoutDesignAgent:
    """Agent that determines optimal spatial arrangement for educational clarity."""
    
    def __init__(self):
        self.gemini = FreeGeminiService()
        self.perplexity = PerplexityService()
        self.use_perplexity = getattr(Config, 'USE_PERPLEXITY_FOR_LAYOUT', True)
    
    def design_layout(self, content_analysis: dict) -> dict:
        """Create spatial layout plan for maximum educational impact."""
        
        system_prompt = f"""You are a visual design expert specializing in educational diagrams.

Given this content analysis, design the optimal spatial layout:

CONTENT ANALYSIS:
{json.dumps(content_analysis, indent=2)}

Design a layout that maximizes learning. Consider:
- Information hierarchy (most important elements prominent)
- Reading flow (left-to-right, top-to-bottom for processes)  
- Visual balance and clarity
- Appropriate spacing to avoid clutter
- Logical grouping of related elements
- Spread out elements to use canvas effectively
- Text should be easily readable at normal zoom levels

Canvas size: 1024x768 pixels

Respond with JSON:
{{
  "layout_strategy": "center_focus|left_to_right|top_to_bottom|circular|radial",
  "element_positions": [
    {{"name": "element_name", "x": 100, "y": 150, "width": 120, "height": 80, "priority": "primary|secondary|tertiary"}},
    {{"name": "element2", "x": 300, "y": 200, "width": 100, "height": 60, "priority": "primary|secondary|tertiary"}}
  ],
  "connection_paths": [
    {{"from": "element1", "to": "element2", "path_type": "straight|curved|stepped", "control_points": [[x1,y1], [x2,y2]]}},
  ],
  "text_zones": [
    {{"type": "title", "x": 400, "y": 50, "max_width": 300}},
    {{"type": "label", "element": "element1", "position": "above|below|left|right", "offset": 20}}
  ],
  "visual_hierarchy": ["most_important_element", "second_important", "supporting_elements"]
}}

Ensure no overlapping elements and clear visual flow."""

        try:
            # First get initial layout from Gemini
            initial_response = self.gemini.generate_response("", system_prompt)
            
            # Use Perplexity for spatial optimization review
            if self.use_perplexity and self.perplexity.api_key:
                print("🧠 Using Perplexity for layout optimization...")
                
                reflection_prompt = f"""
                Review and improve this spatial layout analysis:
                
                Initial Layout:
                {json.dumps(initial_response, indent=2)}
                
                As a spatial design expert with access to current educational research:
                1. Is this layout non-overlapping with clear element separation?
                2. Are the shapes optimally placed for educational clarity?
                3. Does it use the full 1200x800 canvas effectively?
                4. Is the reading flow intuitive (left-to-right for processes)?
                
                If improvements are needed, provide an enhanced layout.
                If the original is optimal, return it unchanged.
                
                CRITICAL: Return ONLY the JSON layout object, no other text or analysis.
                """
                
                #optimized_response = self.perplexity.generate_content(reflection_prompt, system_prompt)
                
                # Extract JSON from Perplexity response
                layout_json = self._extract_json_from_response(initial_response)
                
                if layout_json:
                    print("✅ Perplexity layout optimization successful")
                    return layout_json
                else:
                    print("⚠️ Failed to parse Perplexity response, using Gemini fallback")
                    return initial_response
            else:
                return initial_response
                
        except Exception as e:
            print(f"❌ Layout generation error: {e}")
            return self._create_fallback_layout(content_analysis)
    
    def _extract_json_from_response(self, response) -> dict:
        """Extract JSON from various response formats."""
        
        # Handle different response types
        if isinstance(response, dict):
            if 'content' in response:
                content = response['content']
            elif 'raw_response' in response:
                content = response.get('content', '')
            else:
                # Response might already be the JSON we need
                if self._validate_layout_structure(response):
                    return response
                content = str(response)
        else:
            content = str(response)
        
        # Try to find JSON in the content
        json_patterns = [
            # Look for JSON code blocks
            r'``````',
            r'``````',
            # Look for standalone JSON objects
            r'(\{[^{}]*"layout_strategy"[^{}]*\{.*?\}[^{}]*\})',
            # Look for any JSON-like structure
            r'(\{.*?"element_positions".*?\})',
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                try:
                    # Clean up the JSON string
                    json_str = match.strip()
                    # Remove any trailing text after the closing brace
                    brace_count = 0
                    end_pos = 0
                    for i, char in enumerate(json_str):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_pos = i + 1
                                break
                    
                    if end_pos > 0:
                        json_str = json_str[:end_pos]
                    
                    parsed_json = json.loads(json_str)
                    if self._validate_layout_structure(parsed_json):
                        return parsed_json
                except json.JSONDecodeError:
                    continue
        
        # If no JSON found, try to extract key information from text
        return self._extract_layout_from_text(content)
    
    def _extract_layout_from_text(self, content: str) -> dict:
        """Extract layout information from text content as fallback."""
        
        # Look for element positions mentioned in text
        element_positions = []
        
        # Simple regex patterns to find coordinates
        position_pattern = r'"([^"]+)".*?x["\s:]*(\d+).*?y["\s:]*(\d+).*?width["\s:]*(\d+).*?height["\s:]*(\d+)'
        matches = re.findall(position_pattern, content, re.IGNORECASE | re.DOTALL)
        
        for match in matches:
            try:
                element_positions.append({
                    "name": match[0],
                    "x": int(match[1]),
                    "y": int(match[2]),
                    "width": int(match[3]),
                    "height": int(match[4]),
                    "priority": "primary"
                })
            except ValueError:
                continue
        
        if element_positions:
            return {
                "layout_strategy": "optimized",
                "element_positions": element_positions,
                "connection_paths": [],
                "text_zones": [
                    {"type": "title", "x": 600, "y": 50, "max_width": 400}
                ],
                "visual_hierarchy": [pos["name"] for pos in element_positions]
            }
        
        return None
    
    def _validate_layout_structure(self, layout: dict) -> bool:
        """Validate that layout has required structure."""
        if not isinstance(layout, dict):
            return False
        
        required_fields = ['layout_strategy', 'element_positions']
        if not all(field in layout for field in required_fields):
            return False
        
        if not isinstance(layout['element_positions'], list):
            return False
        
        # Check that each position has required fields
        for pos in layout['element_positions']:
            if not all(field in pos for field in ['name', 'x', 'y', 'width', 'height']):
                return False
        
        return True
    
    def _create_fallback_layout(self, content_analysis: dict) -> dict:
        """Simple grid-based fallback layout."""
        elements = content_analysis.get('visual_elements', [])
        positions = []
        
        # Improved spacing for larger canvas
        cols = 3
        start_x, start_y = 150, 120  # More left padding, less top padding
        spacing_x, spacing_y = 300, 200  # Increased horizontal and vertical spacing
        
        for i, element in enumerate(elements[:6]):
            col = i % cols
            row = i // cols
            positions.append({
                "name": element['name'],
                "x": start_x + col * spacing_x,
                "y": start_y + row * spacing_y,
                "width": 180,  # Larger elements
                "height": 100,  # Taller elements
                "priority": element.get('importance', 'secondary')
            })
        
        return {
            "layout_strategy": "grid_fallback",
            "element_positions": positions,
            "connection_paths": [],
            "text_zones": [
                {"type": "title", "x": 600, "y": 50, "max_width": 400}  # Centered for wider canvas
            ],
            "visual_hierarchy": [el['name'] for el in elements]
        }
