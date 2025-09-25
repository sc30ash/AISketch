from typing import List, Dict, Any

class ClientSideCanvasGenerator:
    """Generate client-side canvas drawing instructions (FREE)."""
    
    def generate_instructions(self, canvas_elements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert canvas elements to client-side drawing instructions."""
        
        instructions = []
        
        for element in canvas_elements:
            element_type = element.get('type', '')
            
            if element_type == 'text':
                instructions.append({
                    'action': 'drawText',
                    'content': element.get('content', ''),
                    'x': element.get('x', 100),
                    'y': element.get('y', 100),
                    'style': element.get('style', 'normal'),
                    'color': element.get('color', '#000000'),
                    'fontSize': self._get_font_size(element.get('style', 'normal'))
                })
            
            elif element_type == 'arrow':
                instructions.append({
                    'action': 'drawArrow',
                    'x1': element.get('x1', 0),
                    'y1': element.get('y1', 0),
                    'x2': element.get('x2', 100),
                    'y2': element.get('y2', 100),
                    'color': element.get('color', 'red'),
                    'width': element.get('width', 2)
                })
            
            elif element_type == 'circle':
                instructions.append({
                    'action': 'drawCircle',
                    'cx': element.get('cx', 100),
                    'cy': element.get('cy', 100),
                    'r': element.get('r', 50),
                    'stroke': element.get('stroke', 'black'),
                    'fill': element.get('fill', 'none'),
                    'strokeWidth': element.get('strokeWidth', 2)
                })
            
            elif element_type == 'rectangle':
                instructions.append({
                    'action': 'drawRectangle',
                    'x': element.get('x', 0),
                    'y': element.get('y', 0),
                    'width': element.get('width', 100),
                    'height': element.get('height', 50),
                    'stroke': element.get('stroke', 'black'),
                    'fill': element.get('fill', 'none'),
                    'strokeWidth': element.get('strokeWidth', 2)
                })
            
            elif element_type == 'line':
                instructions.append({
                    'action': 'drawLine',
                    'x1': element.get('x1', 0),
                    'y1': element.get('y1', 0),
                    'x2': element.get('x2', 100),
                    'y2': element.get('y2', 100),
                    'color': element.get('color', 'black'),
                    'width': element.get('width', 2)
                })
        
        return instructions
    
    def _get_font_size(self, style: str) -> int:
        """Get font size based on style."""
        style_map = {
            'title': 24,
            'subtitle': 20,
            'bold': 18,
            'normal': 16,
            'small': 12
        }
        return style_map.get(style, 16)
