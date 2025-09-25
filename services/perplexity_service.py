import os
import json
import time
from typing import Dict, Any
from perplexity import Perplexity

class PerplexityService:
    """Perplexity API service using the official Perplexity SDK."""
    
    def __init__(self):
        self.api_key = os.environ.get("PERPLEXITY_API_KEY")
        self.client = Perplexity(api_key=self.api_key)
        self.model = "sonar-pro"  # Latest Perplexity model
        self.last_call_time = 0
        self.rate_limit_delay = 1.0  # 1 second between calls
    
    def generate_content(self, prompt: str, system_prompt: str = None) -> Dict[str, Any]:
        """Generate content using Perplexity Sonar reasoning."""
        
        # Rate limiting
        current_time = time.time()
        time_since_last = current_time - self.last_call_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            # Use official Perplexity SDK
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.1,  # Lower temperature for more consistent reasoning
                max_tokens=4000,
                top_p=0.9
            )
            
            content = completion.choices[0].message.content
            
            # Try to parse as JSON, fallback to string
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                return {"content": content, "raw_response": True}
                
        except Exception as e:
            print(f"Perplexity API error: {e}")
            # Fallback response
            return {
                "error": "API call failed",
                "fallback": True,
                "content": f"Analysis of topic failed due to API error: {e}"
            }
        finally:
            self.last_call_time = time.time()
    
    def analyze_educational_content(self, topic: str) -> Dict[str, Any]:
        """Specialized method for educational content analysis with reasoning."""
        
        system_prompt = """You are an expert educational content analyst with access to current information. 
        Your task is to break down topics into comprehensive visual learning components.
        
        Use your reasoning capabilities to:
        1. Research the topic thoroughly
        2. Identify all key educational components
        3. Determine optimal learning relationships
        4. Structure for visual representation
        
        Always return valid JSON format."""
        
        user_prompt = f"""
        Analyze "{topic}" for educational diagram creation. Use step-by-step reasoning:
        
        STEP 1: Research and gather comprehensive information about {topic}
        STEP 2: Identify all key components that students need to understand
        STEP 3: Determine relationships and connections between components
        STEP 4: Structure for optimal visual learning
        
        Return JSON:
        {{
          "main_concept": "Primary concept name",
          "reasoning_process": "Your step-by-step analysis",
          "visual_elements": [
            {{"name": "element1", "type": "object|process|connection", "importance": "high|medium|low", "description": "detailed description"}},
            {{"name": "element2", "type": "object|process|connection", "importance": "high|medium|low", "description": "detailed description"}}
          ],
          "relationships": [
            {{"from": "element1", "to": "element2", "type": "flow|cause|part_of|transforms", "label": "relationship description"}}
          ],
          "educational_goal": "What students should understand",
          "complexity_level": "elementary|middle|high",
          "diagram_type": "flow|cycle|structure|comparison|timeline",
          "current_context": "Any recent developments or current information"
        }}
        
        Ensure comprehensive analysis with at least 4-6 visual elements and 2+ relationships.
        """
        
        return self.generate_content(user_prompt, system_prompt)
    
    def validate_and_enhance_content(self, content: dict, topic: str) -> Dict[str, Any]:
        """Use Perplexity to validate and enhance existing content analysis."""
        
        validation_prompt = f"""
        Review and enhance this educational analysis for "{topic}":
        
        {json.dumps(content, indent=2)}
        
        As an educational expert with access to current information:
        1. Is this analysis comprehensive enough for student learning?
        2. Are there any missing key components?
        3. Are the relationships accurate and complete?
        4. Can you add any recent developments or current context?
        
        Return an improved JSON with the same structure, adding missing elements and correcting any issues.
        Ensure at least 4-6 visual elements and 2+ relationships for effective learning.
        """
        
        system_prompt = "You are an educational content validator and enhancer with access to current information. Improve educational analyses for maximum student comprehension."
        
        return self.generate_content(validation_prompt, system_prompt)
