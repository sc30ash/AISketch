# AI Tutor Sketchpad

A real-time AI-powered educational platform that teaches concepts through synchronized text explanations and interactive visual sketching.

## Project Overview

**Timebox:** 48 hours - Full implementation with advanced multi-agent architecture and multiple AI model integration.

This project demonstrates a sophisticated real-time AI tutor that explains educational concepts through synchronized text and visual sketching. The system uses a multi-agent architecture with dual AI models to generate comprehensive educational diagrams that appear progressively on an interactive canvas.

## Setup Instructions

### Prerequisites
- Python 3.11+
- Docker (optional)
- Modern web browser with HTML5 Canvas support
- API keys for:
  - Google Gemini
  - Perplexity AI
  - HuggingFace (optional)

### Installation

1. **Clone the repository**

2. **Set up environment variables**
Edit `.env` with your API keys:
GEMINI_API_KEY=your_gemini_key_here
PERPLEXITY_API_KEY=your_perplexity_key_here
HUGGINGFACE_API_KEY=your_huggingface_key_here
USE_PERPLEXITY_FOR_CONTENT=true
USE_PERPLEXITY_FOR_LAYOUT=true


3. **Install Python dependencies**
```
pip install -r requirements.txt
```

4. **Run the application**
```
python app.py
```

### Docker Setup (Alternative)
```
docker-compose up --build
```

**Access the application at:** `http://localhost:5000`

## Technical Architecture

### Design Choices

**Multi-Agent Architecture:** Implemented a specialized agent system for enhanced educational content generation:
- **Content Agent** (Perplexity Sonar): Analyzes topics using advanced reasoning capabilities
- **Layout Agent** (Perplexity + Gemini): Optimizes spatial arrangement for learning clarity  
- **Visual Agent** (Gemini): Determines optimal colors, shapes, and visual metaphors
- **SVG Renderer**: Generates high-quality scalable educational diagrams

**Dual AI Model Strategy:**
- **Perplexity Sonar**: Reasoning-focused tasks (content analysis, layout optimization)
- **Google Gemini**: Creative and generative tasks (visual design, fallback operations)

**Real-time Architecture:**
- **Frontend**: Vanilla JavaScript with Socket.IO for real-time communication
- **Backend**: Flask-SocketIO with multi-threading support  
- **Canvas Engine**: Custom progressive animation system
- **Communication**: WebSocket-based with comprehensive error handling

### Technical Stack
- **Backend**: Python/Flask, Flask-SocketIO, multi-agent orchestration
- **Frontend**: HTML5 Canvas, vanilla JavaScript, Socket.IO client
- **AI Models**: Google Gemini, Perplexity Sonar
- **Real-time**: WebSockets via Socket.IO
- **Containerization**: Docker with production-ready configuration

### Project Structure
```bash
ai-tutor-sketchpad/
├── agents/ # Multi-agent system
│ ├── content_agent.py # Topic analysis
│ ├── layout_agent.py # Spatial optimization
│ ├── visual_agent.py # Visual design
│ └── free_orchestrator.py # Agent coordination
├── services/ # External API services
│ ├── gemini_service.py # Google Gemini integration
│ ├── perplexity_service.py # Perplexity AI integration
│ └── svg_renderer_service.py # SVG generation
├── static/ # Frontend assets
│ ├── js/
│ │ ├── app.js # Main application
│ │ ├── canvas-engine.js # Drawing system
│ │ └── chat-interface.js # Chat UI
│ └── css/
│ └── style.css # Styling
├── templates/
│ └── index.html # Main UI template
├── app.py # Flask application
├── config.py # Configuration
├── requirements.txt # Python dependencies
├── Dockerfile # Container configuration
└── docker-compose.yml # Multi-service setup
```

## Assumptions

- **API Access**: Valid API keys provided for Gemini and Perplexity services
- **Network**: Stable internet connection for AI model access
- **Browser**: Modern browser with HTML5 Canvas and WebSocket support
- **Target Audience**: K-12 educational concepts and explanations
- **Language**: English-language explanations and content
- **Performance**: Optimized for desktop/laptop usage (responsive design included)

## Demo Guide

### Recommended Test Questions:

**1. "Explain photosynthesis"**
- **Expected:** Multi-agent SVG generation with biological process visualization
- **Features:** Chloroplasts, sunlight, CO2/O2 exchange, glucose production

**2. "Show me the water cycle"**  
- **Expected:** Complex process flows with natural phenomena
- **Features:** Evaporation, condensation, precipitation arrows and cycles

**3. "How does a circuit work?"**
- **Expected:** Physics concepts with electrical component relationships  
- **Features:** Battery, wires, resistors, current flow indicators

**4. "Explain the Pythagorean theorem"**
- **Expected:** Mathematical concept with geometric visualization
- **Features:** Right triangles, mathematical formulas, side relationships

**5. "Show me how breathing works"**
- **Expected:** Biological process with anatomical elements
- **Features:** Lungs, diaphragm, oxygen/carbon dioxide exchange

### Expected Behavior:
1. **Text Animation**: AI provides conversational explanation with gradual character-by-character typing
2. **SVG Generation**: System generates comprehensive educational diagram using multi-agent analysis
3. **Progressive Drawing**: Canvas elements appear with smooth animations (circles grow, arrows draw progressively)
4. **Smart Positioning**: Arrows connect element edges (not centers) with readable text labels
5. **Visual Optimization**: All text remains black for readability, bright colors for visual elements
6. **Responsive Design**: Interface adapts to different screen sizes with scrollable canvas

## Key Features

- **Progressive Animation**: Text types gradually, followed by synchronized canvas drawing
- **Multi-Modal AI**: Combines reasoning (Perplexity) and generation (Gemini) capabilities  
- **Educational Optimization**: Specialized layout algorithms designed for learning effectiveness
- **Production Ready**: Comprehensive error handling, logging, and Docker containerization
- **Scalable Architecture**: Multi-agent design supports easy expansion and customization
- **Real-time Sync**: WebSocket-based communication for immediate response
- **Smart Visuals**: Automatic canvas fitting, edge-to-edge arrow connections, readable text positioning

## Advanced Features

### Multi-Agent Workflow:
1. **Content Analysis**: Perplexity Sonar analyzes educational requirements
2. **Layout Optimization**: Spatial arrangement optimized for learning clarity  
3. **Visual Design**: Colors and shapes chosen for educational impact
4. **SVG Rendering**: High-quality scalable diagrams with proper text positioning
5. **Progressive Animation**: Coordinated text and canvas timing for optimal UX

### Technical Innovations:
- **Dual AI Strategy**: Leverages different model strengths for optimal results
- **Canvas Auto-fitting**: Automatically scales content to fit available space
- **Edge-aware Arrows**: Arrows connect to element boundaries, not centers
- **Readable Text Angles**: Prevents upside-down arrow labels
- **Production Architecture**: Docker containerization with health checks and logging

---

**Submitted for:** YoLearn.AI AI Engineer Candidate Task  
**Completion Time:** 48 hours
