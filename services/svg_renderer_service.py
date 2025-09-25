# Create: services/svg_renderer_service.py
import base64
from typing import Dict, Any
import math

class SVGEducationalRenderer:
    """Renders educational diagrams from multi-agent specifications."""
    
    def __init__(self):
        self.canvas_width = 1200
        self.canvas_height = 800
    
    def render_educational_diagram(self, content_analysis: dict, layout_plan: dict, visual_design: dict) -> dict:
        """Combine all agent outputs into a final educational SVG."""
        
        svg_content = self._build_svg(content_analysis, layout_plan, visual_design)
        
        # Convert to base64 for web use
        svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        data_url = f"data:image/svg+xml;base64,{svg_b64}"
        
        return {
            'data': data_url,
            'source': 'multi_agent_svg',
            'svg_content': svg_content,
            'metadata': {
                'topic': content_analysis.get('main_concept'),
                'diagram_type': content_analysis.get('diagram_type'),
                'educational_goal': content_analysis.get('educational_goal')
            }
        }
    
    def _build_svg(self, content: dict, layout: dict, visuals: dict) -> str:
        """Build the complete SVG from specifications."""
    
        # FIRST: Fit all elements within canvas bounds
        self._fit_elements_to_canvas(layout)
    
        # Start SVG with proper viewBox
        svg_parts = [
            f'<svg viewBox="0 0 {self.canvas_width} {self.canvas_height}" '
            f'width="{self.canvas_width}" height="{self.canvas_height}" '
            f'xmlns="http://www.w3.org/2000/svg">',
            '<defs>',
            self._create_gradients(),
            self._create_arrow_markers(),
            '</defs>',
            f'<rect width="{self.canvas_width}" height="{self.canvas_height}" fill="#FFFFFF"/>', # Clean background
        ]

        # Add main elements
        svg_parts.extend(self._render_elements(layout, visuals))
    
        # Add connections/arrows
        svg_parts.extend(self._render_connections(content, layout, visuals))
    
        # Add text and labels
        svg_parts.extend(self._render_text(content, layout, visuals))
    
        # Close SVG
        svg_parts.append('</svg>')
    
        return '\n'.join(svg_parts)

    def _create_arrow_markers(self) -> str:
            """Create arrow markers for connections."""
            return '''
            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
                <polygon points="0 0, 10 3.5, 0 7" fill="#2C3E50" />
            </marker>'''

    def _create_gradients(self) -> str:
            """Create reusable gradient definitions."""
            return '''
            <linearGradient id="blueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#4A90E2;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#357ABD;stop-opacity:1" />
            </linearGradient>
            <linearGradient id="greenGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#50C878;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#3E9F5F;stop-opacity:1" />
            </linearGradient>'''


    def _fit_elements_to_canvas(self, layout: dict):
        """Automatically fit all elements within canvas boundaries."""
        elements = layout.get('element_positions', [])
        if not elements:
            return
    
        # Find the bounding box of all elements
        min_x = min(el['x'] for el in elements)
        max_x = max(el['x'] + el.get('width', 100) for el in elements)
        min_y = min(el['y'] for el in elements)
        max_y = max(el['y'] + el.get('height', 60) for el in elements)
    
        # Calculate current dimensions
        current_width = max_x - min_x
        current_height = max_y - min_y
    
        # Calculate safe canvas area (with padding)
        padding = 40
        safe_width = self.canvas_width - (padding * 2)
        safe_height = self.canvas_height - (padding * 2)
    
        # Calculate scaling factors
        scale_x = safe_width / current_width if current_width > safe_width else 1.0
        scale_y = safe_height / current_height if current_height > safe_height else 1.0
    
        # Use the smaller scale to maintain aspect ratio
        scale = min(scale_x, scale_y, 1.0)  # Don't scale up, only down
    
        # Calculate new dimensions and centering offset
        new_width = current_width * scale
        new_height = current_height * scale
        offset_x = (self.canvas_width - new_width) / 2 - min_x * scale
        offset_y = (self.canvas_height - new_height) / 2 - min_y * scale
    
        # Apply transformation to all elements
        for element in elements:
            element['x'] = element['x'] * scale + offset_x
            element['y'] = element['y'] * scale + offset_y
            element['width'] = element.get('width', 100) * scale
            element['height'] = element.get('height', 60) * scale

    
    
    def _render_elements(self, layout: dict, visuals: dict) -> list:
        """Render main visual elements."""
        svg_parts = []
        
        # Create lookup for visual styles
        visual_lookup = {v['name']: v for v in visuals.get('visual_elements', [])}
        
        for element in layout.get('element_positions', []):
            name = element['name']
            x, y = element['x'], element['y']
            width, height = element.get('width', 100), element.get('height', 60)
            
            visual = visual_lookup.get(name, {})
            shape = visual.get('shape', 'rectangle')
            fill = visual.get('fill_color', '#4A90E2')
            stroke = visual.get('stroke_color', '#2C3E50')
            stroke_width = visual.get('stroke_width', 2)
            
            if shape == 'rectangle':
                svg_parts.append(f'''<rect x="{x}" y="{y}" width="{width}" height="{height}" 
                                    fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" rx="8"/>''')
            elif shape == 'circle':
                r = min(width, height) // 2
                cx, cy = x + width//2, y + height//2
                svg_parts.append(f'''<circle cx="{cx}" cy="{cy}" r="{r}" 
                                    fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>''')
            elif shape == 'ellipse':
                rx, ry = width//2, height//2
                cx, cy = x + width//2, y + height//2
                svg_parts.append(f'''<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" 
                                    fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}"/>''')
        
        return svg_parts
    
    def _render_connections(self, content: dict, layout: dict, visuals: dict) -> list:
        """Render arrows shortened by 20% from both sides to avoid overlapping element text."""
        svg_parts = []
    
        # Create position lookup
        pos_lookup = {el['name']: el for el in layout.get('element_positions', [])}
    
        for connection in content.get('relationships', []):
            from_name = connection['from']
            to_name = connection['to']
        
            if from_name in pos_lookup and to_name in pos_lookup:
                from_el = pos_lookup[from_name]
                to_el = pos_lookup[to_name]
            
                # Calculate original center-to-center connection points
                original_x1 = from_el['x'] + from_el.get('width', 100) // 2
                original_y1 = from_el['y'] + from_el.get('height', 60) // 2
                original_x2 = to_el['x'] + to_el.get('width', 100) // 2
                original_y2 = to_el['y'] + to_el.get('height', 60) // 2
            
                # Calculate direction vector
                dx = original_x2 - original_x1
                dy = original_y2 - original_y1
            
                # Calculate the shortened arrow coordinates
                # Move start point 20% closer to end point
                x1 = original_x1 + dx * 0.2
                y1 = original_y1 + dy * 0.2
            
                # Move end point 20% closer to start point
                x2 = original_x2 - dx * 0.2
                y2 = original_y2 - dy * 0.2
            
                svg_parts.append(f'''<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" 
                                   stroke="#2C3E50" stroke-width="2" marker-end="url(#arrowhead)"/>''')
    
        return svg_parts

    
    def _render_text(self, content: dict, layout: dict, visuals: dict) -> list:
        """Render all text elements and labels."""
        svg_parts = []
    
        # Main title - larger font
        main_concept = content.get('main_concept', 'Educational Diagram')
        svg_parts.append(f'''
        <text x="{self.canvas_width//2}" y="40" 
              text-anchor="middle" 
              font-family="Inter, sans-serif" 
              font-size="32" 
              font-weight="bold" 
              fill="#2C3E50">
        {main_concept}</text>''')
    
        # Element labels - BLACK TEXT
        pos_lookup = {el['name']: el for el in layout.get('element_positions', [])}
        for element in layout.get('element_positions', []):
            name = element['name']
            x = element['x'] + element.get('width', 100) // 2
            y = element['y'] + element.get('height', 60) // 2
        
            # Clean up name for display
            display_name = name.replace('_', ' ').title()
        
            svg_parts.append(f'''
            <text x="{x}" y="{y}" 
                  text-anchor="middle" 
                  font-family="Inter, sans-serif" 
                  font-size="16" 
                  fill="black">
            {display_name}</text>''')

    
        # Connection labels - CORRECTED VERSION with readable angle
        for connection in content.get('relationships', []):
            if connection['from'] in pos_lookup and connection['to'] in pos_lookup:
                from_el = pos_lookup[connection['from']]
                to_el = pos_lookup[connection['to']]
            
                # Calculate proper arrow start/end points (edge to edge)
                x1, y1, x2, y2 = self._calculate_edge_connection_points(from_el, to_el)
            
                # Calculate true midpoint
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
            
                # Calculate angle and ensure text is never upside down
                angle = math.atan2(y2 - y1, x2 - x1) * 180 / math.pi
                angle = self._normalize_text_angle(angle)
            
                # Get label from connection
                label = connection.get('label', connection.get('type', ''))
            
                if label:
                    svg_parts.append(f'''
                    <text x="{mid_x:.1f}" y="{mid_y-10:.1f}" 
                          text-anchor="middle" 
                          font-family="Inter, sans-serif" 
                          font-size="12" 
                          fill="black" 
                          transform="rotate({angle:.1f} {mid_x:.1f} {mid_y:.1f})"
                          style="dominant-baseline: central;">
                        {label}
                    </text>''')
    
        return svg_parts

    def _calculate_edge_connection_points(self, from_el: dict, to_el: dict) -> tuple:
        """Calculate connection points on element edges, not centers."""
    
        # Element boundaries
        from_left = from_el['x']
        from_right = from_el['x'] + from_el.get('width', 100)
        from_top = from_el['y']
        from_bottom = from_el['y'] + from_el.get('height', 60)
        from_center_x = from_left + from_el.get('width', 100) / 2
        from_center_y = from_top + from_el.get('height', 60) / 2
    
        to_left = to_el['x']
        to_right = to_el['x'] + to_el.get('width', 100)
        to_top = to_el['y']
        to_bottom = to_el['y'] + to_el.get('height', 60)
        to_center_x = to_left + to_el.get('width', 100) / 2
        to_center_y = to_top + to_el.get('height', 60) / 2
    
        # Calculate direction from source to target center
        dx = to_center_x - from_center_x
        dy = to_center_y - from_center_y
    
        # Find exit point on source element edge
        if abs(dx) > abs(dy):  # Horizontal connection preferred
            if dx > 0:  # Going right
                x1 = from_right
                y1 = from_center_y
            else:  # Going left
                x1 = from_left
                y1 = from_center_y
        else:  # Vertical connection preferred
            if dy > 0:  # Going down
                x1 = from_center_x
                y1 = from_bottom
            else:  # Going up
                x1 = from_center_x
                y1 = from_top
    
        # Find entry point on target element edge
        if abs(dx) > abs(dy):  # Horizontal connection
            if dx > 0:  # Coming from left
                x2 = to_left
                y2 = to_center_y
            else:  # Coming from right
                x2 = to_right
                y2 = to_center_y
        else:  # Vertical connection
            if dy > 0:  # Coming from above
                x2 = to_center_x
                y2 = to_top
            else:  # Coming from below
                x2 = to_center_x
                y2 = to_bottom

        return x1, y1, x2, y2


    def _normalize_text_angle(self, angle: float) -> float:
        """Ensure text is never upside down by normalizing angle."""
    
        # Normalize angle to -180 to 180 range
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
    
        # If text would be upside down (between 90 and 270 degrees), flip it
        if angle > 90:
            angle -= 180
        elif angle < -90:
            angle += 180
    
        return angle

