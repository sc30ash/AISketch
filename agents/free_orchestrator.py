import json
from typing import Dict, List, Any, Callable
import time
from concurrent.futures import ThreadPoolExecutor
import traceback

from services.gemini_service import FreeGeminiService
from services.huggingface_service import FreeHuggingFaceService
from agents.canvas_generator import ClientSideCanvasGenerator
from services.perplexity_service import PerplexityService


from agents.content_agent import ContentAnalysisAgent
from agents.layout_agent import LayoutDesignAgent  
from agents.visual_agent import VisualStyleAgent
from services.svg_renderer_service import SVGEducationalRenderer

class FreeVisualOrchestrator:
    """Orchestrator using only FREE APIs and client-side rendering."""
    
    def __init__(self):
        self.gemini = FreeGeminiService()
        self.huggingface = FreeHuggingFaceService()
        self.perplexity = PerplexityService()  # Add this line
        self.canvas_gen = ClientSideCanvasGenerator()
    
        # Rate limiting for FREE tiers
        self.last_gemini_call = 0
        self.last_hf_call = 0
        self.last_perplexity_call = 0  # Add this line
    
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.content_agent = ContentAnalysisAgent()
        self.layout_agent = LayoutDesignAgent()
        self.visual_agent = VisualStyleAgent()
        self.svg_renderer = SVGEducationalRenderer()

    def generate_educational_diagram(self, topic: str) -> dict:
        """Generate educational diagram using multi-agent system."""
        
        print(f"🎯 Starting multi-agent diagram generation for: {topic}")
        
        # Step 1: Content Analysis
        print("📋 Content Agent analyzing topic...")
        content_analysis = self.content_agent.analyze_topic(topic)
        
        # Step 2: Layout Design  
        print("📐 Layout Agent designing spatial arrangement...")
        layout_plan = self.layout_agent.design_layout(content_analysis)
        
        # Step 3: Visual Design
        print("🎨 Visual Agent choosing colors and shapes...")
        visual_design = self.visual_agent.design_visuals(content_analysis, layout_plan)
        
        # Step 4: SVG Rendering
        print("🖼️ SVG Renderer assembling final diagram...")
        final_diagram = self.svg_renderer.render_educational_diagram(
            content_analysis, layout_plan, visual_design
        )
        
        print("✅ Multi-agent diagram generation complete!")
        
        return final_diagram

    def _extract_explanation_from_raw_response(self, raw_response: str) -> str:
        """Extract clean explanation from raw JSON response."""
        try:
            # Try to find explanation in raw text
            if '"explanation":' in raw_response:
                start = raw_response.find('"explanation":')
                start = raw_response.find('"', start + 14) + 1  # Find opening quote
                end = raw_response.find('",', start)  # Find closing quote
                if end > start:
                    return raw_response[start:end]
        except:
            pass
    
        # Ultimate fallback - return first reasonable sentence
        sentences = raw_response.split('. ')
        for sentence in sentences:
            if len(sentence) > 50 and not sentence.startswith('{'):
                return sentence + '.'
    
        return "I can help explain this concept. Please try asking again."
    
    def create_visual_plan_free(self, question: str) -> Dict[str, Any]:
        """Create visual plan using FREE Google Gemini."""
        
        # Respect rate limits
        self._wait_for_rate_limit('gemini')
        
        system_prompt = """## ROLE & PERSONA
You are Buddy, a smart AI tutor who creates perfect visual lessons using interactive canvas diagrams. You're enthusiastic and speak like you're talking to a curious 8-12 year old.

## CORE PRINCIPLE: CANVAS-ONLY VISUAL EDUCATION
Everything is created using canvas drawings - no background images! You create engaging diagrams, flowcharts, graphs, and visual explanations entirely with canvas elements.

## CANVAS ELEMENT TYPES AVAILABLE
- **text**: Labels, titles, equations, definitions
- **arrow**: Directional indicators, process flows, relationships
- **line**: Connections, borders, structural elements  
- **circle**: Nodes, cycles, emphasis points, atoms, cells
- **rectangle**: Boxes, containers, process blocks, frames

## VISUAL DESIGN RULES (CRITICAL FOR VISIBILITY)
✅ **Text Rules**: 
- ALL text and arrows must use BLACK color (#000000) or dark color for maximum readability
- Use clear, simple labels - avoid long sentences in text elements
- Position text away from busy areas for clarity
- Use font sizes between 16px and 32px depending on importance
- For text along arrows, keep it short (1-10 words) and calculate centering position around arrow midpoint

✅ **Element Rules**:
- ALL non-text elements (circles, rectangles) must use BRIGHT/LIGHT colors
- Recommended bright colors: #FFD600 (yellow), #00E5FF (cyan), #69F0AE (lime), #FF4081 (pink), #FFAB40 (orange), #FFFF8D (light yellow)
- Use varied colors to distinguish different concepts or process steps
- Make stroke widths bold enough to be visible (minimum 3px)

## CANVAS DIMENSIONS & POSITIONING
- Canvas size: 1024px width × 768px height
- Safe positioning zones:
  - Text: x: 50-974, y: 50-718 (avoid edges)
  - Shapes: Keep 25px margin from all edges
- Center point: x: 512, y: 384 (use for main focal points)

## TOPIC DECISION FRAMEWORK
✅ **Perfect for Canvas Diagrams**:
- **Math concepts**: Geometry, algebra, trigonometry, calculus
- **Science processes**: Chemical reactions, physics laws, biological processes
- **Flowcharts**: Decision trees, algorithms, step-by-step processes
- **Structures**: Atomic models, molecular diagrams, organizational charts
- **Comparisons**: Venn diagrams, before/after, pros/cons
- **Systems**: Solar system, food chains, economic cycles

✅ **Canvas Creation Strategy**:
- Start with main concept in center
- Use arrows to show flow/relationships
- Create clear visual hierarchy with different element sizes
- Group related concepts using color coding
- Add step numbers for processes

## EXPLANATION WRITING STYLE
✅ **DO**: "Hey! Great question! Let me show you something super cool about [topic]..."
✅ **DO**: Use encouraging words: awesome, amazing, cool, neat, fun, easy, fantastic
✅ **DO**: Break complex topics into simple, exciting discoveries
❌ **DON'T**: Use formal academic language or intimidating terminology
❌ **DON'T**: Create wall-of-text explanations

## JSON OUTPUT FORMAT
{
  "explanation": "Hey there! [enthusiastic kid-friendly explanation in 2-3 simple sentences]",
  "needs_image": true,
  "visual_type": "canvas_drawing",
  "canvas_elements": [
    {"type": "text", "content": "[simple label]", "x": 100, "y": 200, "fontSize": 24, "color": "#000000"},
    {"type": "arrow", "x1": 50, "y1": 100, "x2": 200, "y2": 200, "color": "#FFD600", "width": 4},
    {"type": "circle", "cx": 300, "cy": 200, "r": 50, "stroke": "#00E5FF", "fill": "none", "strokeWidth": 3},
    {"type": "rectangle", "x": 400, "y": 150, "width": 100, "height": 50, "stroke": "#69F0AE", "fill": "none", "strokeWidth": 3},
    {"type": "line", "x1": 100, "y1": 300, "x2": 500, "y2": 300, "color": "#FF4081", "width": 3}
  ]
}

## EXAMPLE: PYTHAGOREAN THEOREM
{
  "explanation": "Hey! Want to learn a super cool math trick? The Pythagorean theorem helps you find the longest side of a right triangle! If you know the two shorter sides, you can find the third one using: a² + b² = c². It's like magic math!",
  "visual_type": "canvas_drawing",
  "canvas_elements": [
    {"type": "line", "x1": 200, "y1": 400, "x2": 400, "y2": 400, "color": "#FFD600", "width": 4},
    {"type": "line", "x1": 400, "y1": 400, "x2": 400, "y2": 200, "color": "#00E5FF", "width": 4},
    {"type": "line", "x1": 200, "y1": 400, "x2": 400, "y2": 200, "color": "#69F0AE", "width": 4},
    {"type": "text", "content": "a", "x": 300, "y": 420, "fontSize": 24, "color": "#000000"},
    {"type": "text", "content": "b", "x": 420, "y": 300, "fontSize": 24, "color": "#000000"},
    {"type": "text", "content": "c", "x": 280, "y": 280, "fontSize": 24, "color": "#000000"},
    {"type": "text", "content": "a² + b² = c²", "x": 512, "y": 150, "fontSize": 28, "color": "#000000"}
  ]
}

## EXAMPLE: WATER CYCLE PROCESS
{
  "explanation": "Hey! Want to see how water travels around our planet? It's like a never-ending adventure! Water goes up to the clouds as vapor, then comes back down as rain, and starts the journey all over again!",
  "visual_type": "canvas_drawing", 
  "canvas_elements": [
    {"type": "circle", "cx": 200, "cy": 500, "r": 80, "stroke": "#00E5FF", "fill": "none", "strokeWidth": 4},
    {"type": "text", "content": "OCEAN", "x": 200, "y": 500, "fontSize": 20, "color": "#000000"},
    {"type": "arrow", "x1": 250, "y1": 450, "x2": 400, "y2": 300, "color": "#FFAB40", "width": 4},
    {"type": "text", "content": "EVAPORATION ☀️", "x": 350, "y": 350, "fontSize": 18, "color": "#000000"},
    {"type": "circle", "cx": 500, "cy": 200, "r": 60, "stroke": "#69F0AE", "fill": "none", "strokeWidth": 4},
    {"type": "text", "content": "CLOUDS", "x": 500, "y": 200, "fontSize": 20, "color": "#000000"},
    {"type": "arrow", "x1": 460, "y1": 250, "x2": 300, "y2": 400, "color": "#FF4081", "width": 4},
    {"type": "text", "content": "RAIN 🌧️", "x": 350, "y": 450, "fontSize": 18, "color": "#000000"}
  ]
}

## DESIGN PRINCIPLES
1. **Clarity First**: Every element should have a clear purpose
2. **Visual Hierarchy**: Use size and color to guide attention  
3. **Logical Flow**: Arrange elements to tell a visual story
4. **Age-Appropriate**: Simple, colorful, engaging for kids
5. **Educational Value**: Each visual element should teach something

Remember: You're creating interactive learning experiences that make complex topics fun and understandable through beautiful, clear canvas diagrams!"""




        try:
            response = self.gemini.generate_response(question, system_prompt)
        
            # Try to extract JSON from response
            json_str = self._extract_json_from_response(response)
            plan = json.loads(json_str)
        
            print(f"✅ Successfully parsed JSON: needs_image={plan.get('needs_image')}")  # DEBUG
        
            self.last_gemini_call = time.time()
            return plan
        
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"❌ Raw response that failed: {response}")
            traceback.print_exc()
            # Try to extract at least the explanation 
            try:
                # Look for explanation in the response
                if '"explanation":' in response:
                    start = response.find('"explanation":') + 14
                    start = response.find('"', start) + 1
                    end = response.find('",', start)
                    if end == -1:
                        end = response.find('"', start + 1)
                    explanation = response[start:end] if end > start else "I can help explain this concept!"
                else:
                    explanation = "Let me help you understand this topic!"
            
                print(f"🔄 Using fallback with extracted explanation")
            
                # Return fallback but force image generation for testing
                return {
                    "explanation": explanation,
                    "visual_type": "image_with_overlays",  # ✅ Force image generation
                    "needs_image": True,  # ✅ Force image generation
                    "image_prompt": f"Educational illustration about {question}, simple colorful diagram",
                    "canvas_elements": [
                        {"type": "text", "content": "Educational Concept", "x": 512, "y": 300, "style": "title"}
                    ]
                }
            except:
                print(f"🆘 Complete fallback")
                return {
                    "explanation": "Let me help you learn about this topic!",
                    "visual_type": "image_with_overlays",
                    "needs_image": True,
                    "image_prompt": f"Simple educational diagram about {question}",
                    "canvas_elements": [
                        {"type": "text", "content": "Learning Topic", "x": 512, "y": 300, "style": "title"}
                    ]
                }

    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON from Gemini response that might have extra text."""
    
        # Find JSON block
        start = response.find('{')
        end = response.rfind('}') + 1
    
        if start != -1 and end > start:
            return response[start:end]
        else:
            # If no JSON found, assume entire response is JSON
            return response
    
    def generate_image_free(self, image_prompt: str) -> Dict[str, Any]:
        """Generate image using FREE HuggingFace API."""
        
        # Respect rate limits
        self._wait_for_rate_limit('huggingface')
        
        try:
            result = self.huggingface.generate_image(image_prompt)
            self.last_hf_call = time.time()
            return result
        except Exception as e:
            print(f"FREE image generation failed: {e}")
            return None
    
    def create_canvas_instructions(self, visual_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create client-side canvas instructions (always FREE)."""
        return self.canvas_gen.generate_instructions(visual_plan.get('canvas_elements', []))
    
    def _wait_for_rate_limit(self, service: str):
        """Respect FREE tier rate limits."""
        current_time = time.time()
        
        if service == 'gemini':
            # Gemini: 15 requests per minute = 4 seconds between calls
            time_since_last = current_time - self.last_gemini_call
            if time_since_last < 4:
                time.sleep(4 - time_since_last)
        
        elif service == 'huggingface':
            # HuggingFace: 300 requests per hour = 12 seconds between calls
            time_since_last = current_time - self.last_hf_call
            if time_since_last < 12:
                time.sleep(12 - time_since_last)

    def execute_parallel_generation(self, instructions: Dict[str, Any], 
                                  progress_callback: Callable = None) -> Dict[str, Any]:
        """Execute all visual generation tasks with image feedback loop."""
        
        results = {}
        
        # Step 1: Generate background image first
        if instructions.get('background_image'):
            if progress_callback:
                progress_callback("Generating background image...")
            
            image_result = self.image_agent.generate_image(instructions['background_image'])
            results['background'] = image_result
            
            # Step 2: NEW - Analyze image for smart positioning
            if image_result and progress_callback:
                progress_callback("Analyzing image for optimal positioning...")
            
            positioning_analysis = self.gemini.analyze_image_for_positioning(
                image_result['data'], 
                instructions.get('concept', 'educational diagram')
            )
            results['positioning'] = positioning_analysis
        
        # Step 3: Generate other elements (now we have positioning context)
        futures = {}
        
        if instructions.get('text_overlays'):
            futures['text_elements'] = self.executor.submit(
                self.text_agent.render_text_elements,
                instructions['text_overlays'],
                results.get('positioning')  # Pass positioning data
            )
        
        if instructions.get('shapes'):
            futures['shapes'] = self.executor.submit(
                self.text_agent.create_shapes,
                instructions['shapes'],
                results.get('positioning')  # Pass positioning data
            )
        
        # Collect results
        for name, future in futures.items():
            try:
                results[name] = future.result(timeout=30)
                if progress_callback:
                    progress_callback(f"Completed {name} with smart positioning")
            except Exception as e:
                results[name] = None
                if progress_callback:
                    progress_callback(f"Failed {name}: {str(e)}")
        
        return results
    
    # ADD THIS NEW METHOD
    def create_smart_canvas_instructions(self, canvas_elements: List[Dict[str, Any]], 
                                       positioning_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create canvas instructions using image analysis feedback."""
        
        if not positioning_data:
            # Fallback to basic positioning
            return self.canvas_gen.generate_instructions(canvas_elements)
        
        # Use analyzed positions for smart placement
        smart_elements = []
        text_positions = positioning_data.get('text_positions', [])
        arrow_paths = positioning_data.get('arrow_paths', [])
        
        for element in canvas_elements:
            if element['type'] == 'text':
                # Find optimal position for this text
                optimal_pos = self._find_optimal_text_position(
                    element['content'], 
                    text_positions
                )
                if optimal_pos:
                    element['x'] = optimal_pos[0]
                    element['y'] = optimal_pos[1]
            
            elif element['type'] == 'arrow':
                # Find optimal arrow path
                optimal_arrow = self._find_optimal_arrow_path(arrow_paths)
                if optimal_arrow:
                    element['x1'] = optimal_arrow['from'][0]
                    element['y1'] = optimal_arrow['from'][1] 
                    element['x2'] = optimal_arrow['to'][0]
                    element['y2'] = optimal_arrow['to'][1]
            
            smart_elements.append(element)
        
        return self.canvas_gen.generate_instructions(smart_elements)
    
    # ADD HELPER METHODS
    def _find_optimal_text_position(self, text_content: str, positions: List[Dict]) -> tuple:
        """Find best position for text based on image analysis."""
        for pos in positions:
            if text_content.upper() in pos.get('label', '').upper():
                return pos['optimal_xy']
        
        # Fallback to first available position
        if positions:
            return positions[0]['optimal_xy']
        return None
    
    def _find_optimal_arrow_path(self, arrow_paths: List[Dict]) -> Dict:
        """Find best arrow path from image analysis."""
        if arrow_paths:
            return arrow_paths[0]  # Use first suggested path
        return None
    
    # ✅ ADD missing method  
    def analyze_image_positioning(self, image_data: str, concept: str):
        return self.gemini.analyze_image_for_positioning(image_data, concept)