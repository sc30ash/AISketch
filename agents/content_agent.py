# Create: agents/content_agent.py
from services.gemini_service import FreeGeminiService
import json

class ContentAnalysisAgent:
    """Agent that identifies key educational components from a topic."""
    
    def __init__(self):
        self.gemini = FreeGeminiService()
    
    def analyze_topic(self, topic: str) -> dict:
        """Extract educational elements and relationships."""
        
        system_prompt = """You are an educational content expert. Analyze topics and identify key components for visual learning.

Your job: Break down the topic into visual elements that need to be shown in an educational diagram.

Respond with JSON:
{
  "main_concept": "Primary concept being taught",
  "visual_elements": [
    {"name": "element1", "type": "object|process|connection", "importance": "high|medium|low", "description": "what it represents"},
    {"name": "element2", "type": "object|process|connection", "importance": "high|medium|low", "description": "what it represents"}
  ],
  "relationships": [
    {"from": "element1", "to": "element2", "type": "flow|cause|part_of|transforms", "label": "relationship description"}
  ],
  "educational_goal": "What should students understand after seeing this?",
  "complexity_level": "elementary|middle|high",
  "diagram_type": "flow|cycle|structure|comparison|timeline"
}


Now analyze {topic} step-by-step:
    1. Core concept identification
    2. Component analysis  
    3. Relationship mapping
    4. Educational completeness check

Make sure there is only one connection between two distinct elements.
Focus on elements that NEED to be visually represented. Don't include everything - only what helps learning."""

        try:
            response = self.gemini.generate_response(topic, system_prompt)
            # Extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
            else:
                # Fallback
                return self._create_fallback_analysis(topic)
                
        except Exception as e:
            print(f"Content analysis error: {e}")
            return self._create_fallback_analysis(topic)
    
    def _create_fallback_analysis(self, topic: str) -> dict:
        """Simple fallback when JSON parsing fails."""
        return {
            "main_concept": topic,
            "visual_elements": [
                {"name": "main_element", "type": "object", "importance": "high", "description": f"Main component of {topic}"}
            ],
            "relationships": [],
            "educational_goal": f"Understand {topic}",
            "complexity_level": "elementary",
            "diagram_type": "structure"
        }
