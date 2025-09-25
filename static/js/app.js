// Main Application Controller - AI Tutor Sketchpad

class AITutorApp {
    constructor() {
        this.socket = null;
        this.isConnected = false;
        this.isGenerating = false;
        this.currentSession = null;
        this.generationStartTime = null;
        
        this.initializeApp();
        this.setupEventListeners();
        this.connectSocket();
    }

    initializeApp() {
        console.log('🚀 Initializing AI Tutor Sketchpad...');
        
        // Initialize components
        this.chatInterface = new ChatInterface();
        this.canvasEngine = new CanvasEngine('drawing-canvas');
        
        // Setup UI elements
        this.questionInput = document.getElementById('question-input');
        this.sendBtn = document.getElementById('send-btn');
        this.statusText = document.getElementById('status-text');
        this.connectionStatus = document.getElementById('connection-status');
        this.generationTime = document.getElementById('generation-time');
        this.layerCount = document.getElementById('layer-count');
        this.loadingText = document.getElementById('loading-text');
        
        // Set initial state
        this.updateStatus('Ready to learn!');
        this.updateConnectionStatus('connecting');
    }

    setupEventListeners() {
        // Input handling
        this.questionInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.askQuestion();
            }
        });

        this.sendBtn.addEventListener('click', () => this.askQuestion());

        // Prevent form submission
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target === this.questionInput) {
                e.preventDefault();
            }
        });

        // Auto-resize canvas on window resize
        window.addEventListener('resize', () => {
            this.canvasEngine.handleResize();
        });
    }

    connectSocket() {
        console.log('🔌 Connecting to socket...');
    
        // Add connection options for better reliability
        this.socket = io('http://localhost:5000', {
            transports: ['websocket', 'polling'],
            timeout: 10000,
            reconnection: true,
            reconnectionAttempts: 5,
            reconnectionDelay: 1000
        });

        this.socket.on('connect', () => {
            console.log('✅ Connected to AI Tutor server');
            this.isConnected = true;
            this.updateConnectionStatus('connected');
        });

        this.socket.on('disconnect', (reason) => {
            console.log('❌ Disconnected from server:', reason);
            this.isConnected = false;
            this.updateConnectionStatus('disconnected');
            this.updateStatus('Connection lost. Reconnecting...');
        });

        this.socket.on('connect_error', (error) => {
            console.error('❌ Connection error:', error);
            this.updateStatus('Connection failed. Please refresh the page.');
        });

        this.socket.on('reconnect', (attemptNumber) => {
            console.log('✅ Reconnected after', attemptNumber, 'attempts');
            this.updateStatus('Reconnected to server');
        });

        // AI Response events
        this.socket.on('explanation_ready', (data) => {
            console.log('💬 Explanation received');
            this.chatInterface.addAIMessage(data.explanation);
            this.updateStatus('Explanation ready. Generating visuals...');
        });

        this.socket.on('image_ready', (data) => {
            console.log('🖼️ Background image ready');
            this.canvasEngine.setBackgroundImage(data.image_data);
            this.updateStatus('Background image loaded. Creating diagram...');
        });

        // In app.js, update the canvas_instructions handler:
        this.socket.on('canvas_instructions', (data) => {
            console.log('📐 Canvas instructions received:', data);
    
            if (data.svg_complete) {
                // SVG diagram is complete - no canvas overlays needed
                console.log('✅ Complete SVG diagram - skipping canvas overlays');
                this.updateStatus('Educational diagram complete!', 'success');
            } else {
                // Normal canvas overlay mode
                if (data.instructions && data.instructions.length > 0) {
                    console.log('🎨 Drawing canvas overlays...');
                    this.canvasEngine.executeInstructions(data.instructions);
                }
            }
    
            this.isGenerating = false;
        });


        this.socket.on('generation_complete', (data) => {
            console.log('✅ Generation complete');
            this.onGenerationComplete();
        });

        // Status and progress events
        this.socket.on('status', (data) => {
            console.log('📊 Status:', data.message);
            this.updateStatus(data.message);
            this.updateLoadingText(data.message);
        });

        this.socket.on('generation_progress', (data) => {
            console.log('⏳ Progress:', data.message);
            this.updateLoadingText(data.message);
        });

        // Error handling
        this.socket.on('error', (data) => {
            console.error('❌ Error:', data.message);
            this.chatInterface.addErrorMessage(data.message);
            this.onGenerationComplete();
            this.updateStatus('Error occurred. Please try again.');
        });

        this.socket.on('canvas_cleared', () => {
            console.log('🧹 Canvas cleared');
            this.canvasEngine.clearCanvas();
        });
    }

    askQuestion() {
        const question = this.questionInput.value.trim();
        
        if (!question) return;
        if (!this.isConnected) {
            this.chatInterface.addErrorMessage('Not connected to server. Please wait...');
            return;
        }
        if (this.isGenerating) {
            this.chatInterface.addErrorMessage('Please wait for the current explanation to complete.');
            return;
        }

        console.log('🤔 User question:', question);
        
        //clear canvas for new question
        this.canvasEngine.clearCanvas();

        // Add user message to chat
        this.chatInterface.addUserMessage(question);
        
        // Clear input
        this.questionInput.value = '';
        
        // Start generation
        this.startGeneration();
        
        // Send to backend
        this.socket.emit('user_question', { question: question });
        
        // Update UI state
        this.updateStatus('Processing your question...');
        this.updateLoadingText('AI is analyzing your question...');
    }

    executeCanvasInstructions(instructions) {
        console.log('🎬 Executing canvas instructions');
        this.canvasEngine.executeInstructions(instructions, {
            onStart: () => {
                this.showAIIndicator();
                this.updateStatus('AI is drawing...');
            },
            onProgress: (step, total) => {
                this.updateStatus(`Drawing step ${step}/${total}...`);
                this.updateLayerCount(step);
            },
            onComplete: () => {
                this.hideAIIndicator();
                this.updateStatus('Visual explanation complete!');
                this.updateLayerCount(instructions.length);
            }
        });
    }

    startGeneration() {
        this.isGenerating = true;
        this.generationStartTime = Date.now();
        this.sendBtn.disabled = true;
        this.showCanvasOverlay();
        this.updateGenerationTime('--');
        this.updateLayerCount('0 layers');
    }

    onGenerationComplete() {
        this.isGenerating = false;
        this.sendBtn.disabled = false;
        this.hideCanvasOverlay();
        this.hideAIIndicator();
        
        // Calculate generation time
        if (this.generationStartTime) {
            const elapsed = ((Date.now() - this.generationStartTime) / 1000).toFixed(1);
            this.updateGenerationTime(`${elapsed}s`);
        }
        
        this.updateStatus('Ready for your next question!');
    }

    // UI Update Methods
    updateStatus(text) {
        this.statusText.textContent = text;
    }

    updateConnectionStatus(status) {
        const statusEl = this.connectionStatus;
        const icon = statusEl.querySelector('i');
        
        statusEl.classList.remove('connected', 'connecting', 'disconnected');
        statusEl.classList.add(status);
        
        switch(status) {
            case 'connected':
                statusEl.innerHTML = '<i class="fas fa-circle"></i> Connected';
                break;
            case 'connecting':
                statusEl.innerHTML = '<i class="fas fa-circle"></i> Connecting...';
                break;
            case 'disconnected':
                statusEl.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
                break;
        }
    }

    updateLoadingText(text) {
        if (this.loadingText) {
            this.loadingText.textContent = text;
        }
    }

    updateGenerationTime(time) {
        this.generationTime.textContent = time;
    }

    updateLayerCount(count) {
        const text = typeof count === 'number' ? `${count} layers` : count;
        this.layerCount.textContent = text;
    }

    showCanvasOverlay() {
        const overlay = document.getElementById('canvas-overlay');
        if (overlay) overlay.classList.add('active');
    }

    hideCanvasOverlay() {
        const overlay = document.getElementById('canvas-overlay');
        if (overlay) overlay.classList.remove('active');
    }

    showAIIndicator() {
        const indicator = document.getElementById('ai-indicator');
        if (indicator) indicator.classList.add('active');
    }

    hideAIIndicator() {
        const indicator = document.getElementById('ai-indicator');
        if (indicator) indicator.classList.remove('active');
    }
}

// Global Functions (for onclick handlers)
function askSuggestedQuestion(question) {
    if (window.aiTutorApp) {
        window.aiTutorApp.questionInput.value = question;
        window.aiTutorApp.askQuestion();
    }
}

function clearCanvas() {
    if (window.aiTutorApp && window.aiTutorApp.socket) {
        window.aiTutorApp.socket.emit('clear_canvas');
        window.aiTutorApp.canvasEngine.clearCanvas();
        window.aiTutorApp.chatInterface.addSystemMessage('Canvas cleared');
        window.aiTutorApp.updateLayerCount('0 layers');
    }
}

function saveCanvas() {
    if (window.aiTutorApp && window.aiTutorApp.canvasEngine) {
        window.aiTutorApp.canvasEngine.saveCanvas();
        window.aiTutorApp.chatInterface.addSystemMessage('Canvas saved successfully!');
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.aiTutorApp = new AITutorApp();
    console.log('🎓 AI Tutor Sketchpad ready!');
});
