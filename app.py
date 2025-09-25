from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import logging
import traceback
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from config import Config
from agents.free_orchestrator import FreeVisualOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.config.from_object(Config)

# Use threading mode instead of eventlet to avoid blocking issues
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode='eventlet',
    logger=False,  # Disable in production
    engineio_logger=False,
    ping_timeout=60,
    ping_interval=25
)
# Initialize FREE orchestrator
try:
    orchestrator = FreeVisualOrchestrator()
    logger.info("✅ Orchestrator initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize orchestrator: {e}")
    traceback.print_exc()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for Docker"""

    return {'status': 'healthy', 'service': 'AI Tutor'}, 200
@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    logger.info(f"Client {session_id} connected")
    emit('connected', {'session_id': session_id, 'tier': 'FREE'})

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    logger.info(f"Client {session_id} disconnected")

@socketio.on('user_question')
def handle_user_question(data):
    session_id = request.sid
    question = data.get('question', '')
    
    print(f"🎯 RECEIVED user_question: '{question}' from session: {session_id}")
    
    if not question:
        emit('error', {'message': 'No question provided'})
        return

    # Emit immediate confirmation
    emit('task_started', {'message': 'Processing your question...'})
    
    # Start background task with proper error handling
    socketio.start_background_task(safe_process_visual_generation, question, session_id)
    print(f"🚀 Background task started for: {question}")

def safe_process_visual_generation(question, session_id):
    """Wrapper for process_free_visual_generation with comprehensive error handling."""
    try:
        process_free_visual_generation(question, session_id)
    except Exception as e:
        print(f"💥 FATAL ERROR in background task: {e}")
        traceback.print_exc()
        
        # Try to emit error to frontend
        try:
            socketio.emit('error', {
                'message': f'System error: {str(e)}',
                'tier': 'FREE',
                'fatal': True
            }, room=session_id)
        except:
            print("❌ Could not emit error to frontend")

def process_free_visual_generation(question, session_id):
    """Process visual generation with robust error handling."""
    
    try:
        print(f"🎯 Starting generation for session: {session_id}")
        
        # Step 1: Emit planning status
        socketio.emit('status', {
            'step': 'planning', 
            'message': 'AI analyzing question...'
        }, room=session_id)
        
        # Get visual plan with timeout protection
        visual_plan = None
        try:
            visual_plan = orchestrator.create_visual_plan_free(question)
            print(f"📋 Visual plan created successfully")
        except Exception as e:
            print(f"❌ Visual plan creation failed: {e}")
            raise Exception(f"Planning failed: {str(e)}")
        
        if not visual_plan:
            raise Exception("Visual plan is None")
        
        # Send explanation
        socketio.emit('explanation_ready', {
            'explanation': visual_plan.get('explanation', 'Let me explain this topic...'),
            'visual_type': visual_plan.get('visual_type', 'canvas_drawing'),
            'free_tier': True
        }, room=session_id)
        print(f"✅ Explanation sent")
        
        # Step 2: Generate diagram
        if visual_plan.get('needs_image', False):
            print(f"🖼️ Generating SVG diagram...")
            socketio.emit('status', {
                'step': 'generating', 
                'message': 'Creating educational diagram...'
            }, room=session_id)
            
            try:
                image_result = orchestrator.generate_educational_diagram(question)
                
                if image_result and image_result.get('data'):
                    socketio.emit('image_ready', {
                        'image_data': image_result['data'],
                        'source': 'multi_agent_svg'
                    }, room=session_id)
                    
                    socketio.emit('canvas_instructions', {
                        'instructions': [],
                        'explanation': visual_plan['explanation'],
                        'composition_type': 'multi_agent_complete',
                        'svg_complete': True
                    }, room=session_id)
                    
                    print(f"✅ SVG diagram sent")
                else:
                    raise Exception("SVG generation returned empty result")
                    
            except Exception as svg_error:
                print(f"❌ SVG generation failed: {svg_error}")
                # Fall back to canvas only
                canvas_instructions = orchestrator.create_canvas_instructions(visual_plan)
                socketio.emit('canvas_instructions', {
                    'instructions': canvas_instructions or [],
                    'explanation': visual_plan['explanation'],
                    'composition_type': 'canvas_only_free',
                    'svg_complete': False
                }, room=session_id)
                print(f"✅ Canvas fallback sent")
        else:
            # Canvas only mode
            print(f"🎨 Using canvas-only mode")
            canvas_instructions = orchestrator.create_canvas_instructions(visual_plan)
            socketio.emit('canvas_instructions', {
                'instructions': canvas_instructions or [],
                'explanation': visual_plan['explanation'],
                'composition_type': 'canvas_only_free',
                'svg_complete': False
            }, room=session_id)
            print(f"✅ Canvas instructions sent")
        
        # Final completion signal
        socketio.emit('generation_complete', {
            'tier': 'FREE',
            'success': True
        }, room=session_id)
        
        print(f"🎉 Generation completed successfully for session {session_id}")
        
    except Exception as e:
        print(f"💥 Error in generation process: {e}")
        traceback.print_exc()
        
        socketio.emit('error', {
            'message': f'Generation failed: {str(e)}',
            'tier': 'FREE'
        }, room=session_id)

if __name__ == '__main__':
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"🚀 Starting AI Tutor server on {host}:{port}")
    
    socketio.run(
        app,
        host=host,
        port=port,
        debug=False,
        use_reloader=False,
        log_output=False
    )
