// Canvas Drawing Engine for AI Tutor

class CanvasEngine {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.backgroundImage = null;
        this.elements = [];
        this.isAnimating = false;
        this.brightColors = ["#FFD600", "#00E5FF", "#69F0AE", "#FF4081", "#FFAB40", "#FFFF8D"];
        
        this.setupCanvas();
        this.setupDrawingStyles();
        
        console.log('🎨 Canvas engine initialized');
    }

    pickBrightColor() {
        return this.brightColors[Math.floor(Math.random() * this.brightColors.length)];
    }

    setupCanvas() {
        // Set up high-DPI canvas
        const rect = this.canvas.getBoundingClientRect();
        const dpr = window.devicePixelRatio || 1;
        
        this.canvas.width = 1024 * dpr;
        this.canvas.height = 768 * dpr;
        
        this.ctx.scale(dpr, dpr);
        
        // Set canvas display size
        this.canvas.style.width = '1024px';
        this.canvas.style.height = '768px';
        
        // Enable smooth rendering
        this.ctx.imageSmoothingEnabled = true;
        this.ctx.imageSmoothingQuality = 'high';
    }

    setupDrawingStyles() {
        this.ctx.lineCap = 'round';
        this.ctx.lineJoin = 'round';
        this.ctx.textAlign = 'start';
        this.ctx.textBaseline = 'middle';
    }

    setBackgroundImage(imageData) {
        const img = new Image();
        img.onload = () => {
            this.backgroundImage = img;
            this.redraw();
            console.log('🖼️ Background image loaded');
        };
        img.onerror = () => {
            console.error('❌ Failed to load background image');
        };
        img.src = imageData;
    }

    executeInstructions(instructions, callbacks = {}) {
        if (this.isAnimating) {
            console.warn('⚠️ Already animating, skipping new instructions');
            return;
        }

        console.log('🎬 Starting canvas animation with', instructions.length, 'instructions');
        
        this.isAnimating = true;
        let currentStep = 0;
        
        if (callbacks.onStart) callbacks.onStart();

        const executeNextInstruction = () => {
            if (currentStep >= instructions.length) {
                this.isAnimating = false;
                if (callbacks.onComplete) callbacks.onComplete();
                return;
            }

            const instruction = instructions[currentStep];
            currentStep++;

            if (callbacks.onProgress) {
                callbacks.onProgress(currentStep, instructions.length);
            }

            // Execute the drawing instruction
            this.executeInstruction(instruction);

            // Schedule next instruction with delay for animation effect
            setTimeout(executeNextInstruction, 600);
        };

        // Start the animation sequence
        executeNextInstruction();
    }

    executeInstruction(instruction) {
        console.log('✏️ Executing:', instruction.action);
        
        switch (instruction.action) {
            case 'drawText':
                this.drawText(instruction);
                break;
            case 'drawArrow':
                this.drawArrow(instruction);
                break;
            case 'drawCircle':
                this.drawCircle(instruction);
                break;
            case 'drawRectangle':
                this.drawRectangle(instruction);
                break;
            case 'drawLine':
                this.drawLine(instruction);
                break;
            default:
                console.warn('⚠️ Unknown instruction:', instruction.action);
        }
        
        // Store element for redraw
        this.elements.push(instruction);
    }

    drawText(instruction) {
        const { content, x, y, fontSize, color, style } = instruction;
        this.ctx.save();
    
        // Calculate text properties
        const actualFontSize = fontSize || this.getFontSizeByStyle(style);
        const fontWeight = style === 'bold' || style === 'title' ? 'bold' : 'normal';
    
        // Set font first to measure text
        this.ctx.font = `${fontWeight} ${actualFontSize}px Inter, sans-serif`;
        this.ctx.textAlign = 'center'; // Center text on the x coordinate
        this.ctx.textBaseline = 'middle';
    
        // Measure text
        const textMetrics = this.ctx.measureText(content);
        const textWidth = textMetrics.width;
        const textHeight = actualFontSize;
    
        // Draw background box for better visibility
        const padding = 6;
        const boxX = x - textWidth/2 - padding;
        const boxY = y - textHeight/2 - padding;
        const boxWidth = textWidth + padding * 2;
        const boxHeight = textHeight + padding * 2;
    
        // Background
        this.ctx.fillStyle = 'rgba(255, 255, 255, 0.95)';
        this.ctx.fillRect(boxX, boxY, boxWidth, boxHeight);
    
        // Border
        this.ctx.strokeStyle = 'rgba(52, 73, 94, 0.3)';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(boxX, boxY, boxWidth, boxHeight);
    
        // Text with good contrast - ALWAYS BLACK
        this.ctx.fillStyle = "#000000";
        this.ctx.fillText(content, x, y);
    
        this.ctx.restore();
    
        console.log(`📝 Text "${content}" drawn at (${x}, ${y})`);
    }

    drawArrow(instruction) {
        const { x1, y1, x2, y2, color, width } = instruction;
        
        this.ctx.save();
        const arrowColor = this.pickBrightColor();
        this.ctx.strokeStyle = arrowColor;
        this.ctx.fillStyle = arrowColor;
        this.ctx.lineWidth = width || 2;
        
        // Draw arrow line
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
        
        // Calculate arrow head
        const angle = Math.atan2(y2 - y1, x2 - x1);
        const arrowLength = 12;
        const arrowAngle = Math.PI / 6;
        
        // Draw arrow head
        this.ctx.beginPath();
        this.ctx.moveTo(x2, y2);
        this.ctx.lineTo(
            x2 - arrowLength * Math.cos(angle - arrowAngle),
            y2 - arrowLength * Math.sin(angle - arrowAngle)
        );
        this.ctx.lineTo(
            x2 - arrowLength * Math.cos(angle + arrowAngle),
            y2 - arrowLength * Math.sin(angle + arrowAngle)
        );
        this.ctx.closePath();
        this.ctx.fill();
        
        this.ctx.restore();
        
        // Animate arrow drawing
        this.animateArrowDrawing(x1, y1, x2, y2);
    }

    drawCircle(instruction) {
        const { cx, cy, r, stroke, fill, strokeWidth } = instruction;
    
        // Validate required parameters
        if (typeof cx === 'undefined' || typeof cy === 'undefined' || typeof r === 'undefined') {
            console.error('❌ drawCircle: Missing required parameters (cx, cy, r):', instruction);
            return;
        }
    
        this.ctx.save();
        this.ctx.strokeStyle = stroke || '#000000';
        this.ctx.lineWidth = strokeWidth || 2;
    
        if (fill && fill !== 'none') {
            this.ctx.fillStyle = fill;
        }
    
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, r, 0, 2 * Math.PI);
    
        if (fill && fill !== 'none') {
            this.ctx.fill();
        }
    
        this.ctx.stroke();
        this.ctx.restore();
    
        // Animate circle drawing
        this.animateCircleDrawing(cx, cy, r);
    
        console.log(`🔵 Circle drawn at (${cx}, ${cy}) with radius ${r}`);
    }


    drawRectangle(instruction) {
        const { x, y, width, height, stroke, fill, strokeWidth } = instruction;
        
        this.ctx.save();
        const rectColor = this.pickBrightColor();
        this.ctx.strokeStyle = rectColor;
        this.ctx.lineWidth = strokeWidth || 2;
        
        if (fill && fill !== 'none') {
            // Use a lighter version of the bright color for fill
            this.ctx.fillStyle = rectColor + '40'; // Add transparency
            this.ctx.fillRect(x, y, width, height);
        }
        
        this.ctx.strokeRect(x, y, width, height);
        this.ctx.restore();
        console.log(`📝 Rectangle drawn at (${x}, ${y})`);
    }

    drawLine(instruction) {
        const { x1, y1, x2, y2, color, width } = instruction;
        
        this.ctx.save();
        this.ctx.strokeStyle = this.pickBrightColor();
        this.ctx.lineWidth = width || 2;
        
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
        
        this.ctx.restore();
    }

    // Animation helpers
    animateTextAppearance(x, y, fontSize) {
        // Simple pulse animation
        this.ctx.save();
        this.ctx.globalAlpha = 0.3;
        this.ctx.strokeStyle = '#4f46e5';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(x - 5, y - fontSize/2 - 5, 200, fontSize + 10);
        this.ctx.restore();
    }

    animateArrowDrawing(x1, y1, x2, y2) {
        // Create a subtle glow effect
        this.ctx.save();
        this.ctx.globalAlpha = 0.3;
        this.ctx.strokeStyle = '#ff0000';
        this.ctx.lineWidth = 6;
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
        this.ctx.restore();
    }

    animateCircleDrawing(cx, cy, r) {
        // Create a subtle highlight
        this.ctx.save();
        this.ctx.globalAlpha = 0.2;
        this.ctx.strokeStyle = '#4f46e5';
        this.ctx.lineWidth = 4;
        this.ctx.beginPath();
        this.ctx.arc(cx, cy, r + 2, 0, 2 * Math.PI);
        this.ctx.stroke();
        this.ctx.restore();
    }

    getFontSizeByStyle(style) {
        const sizeMap = {
            'title': 24,
            'subtitle': 20,
            'bold': 18,
            'normal': 16,
            'small': 12
        };
        return sizeMap[style] || 16;
    }

    redraw() {
        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw background image if available
        if (this.backgroundImage) {
            this.ctx.drawImage(
                this.backgroundImage, 
                0, 0, 
                1024, 768
            );
        }
        
        // Redraw all elements
        this.elements.forEach(element => {
            this.executeInstruction(element);
        });
    }

    clearCanvas() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.backgroundImage = null;
        this.elements = [];
        console.log('🧹 Canvas cleared');
    }

    saveCanvas() {
        const link = document.createElement('a');
        link.download = `ai-tutor-diagram-${Date.now()}.png`;
        link.href = this.canvas.toDataURL('image/png');
        link.click();
        console.log('💾 Canvas saved');
    }

    handleResize() {
        // Maintain aspect ratio on resize
        const container = this.canvas.parentElement;
        const containerWidth = container.clientWidth - 40; // Account for padding
        const containerHeight = container.clientHeight - 40;
        
        const canvasAspect = 1024 / 768;
        const containerAspect = containerWidth / containerHeight;
        
        if (containerAspect > canvasAspect) {
            // Container is wider, fit to height
            this.canvas.style.height = `${containerHeight}px`;
            this.canvas.style.width = `${containerHeight * canvasAspect}px`;
        } else {
            // Container is taller, fit to width
            this.canvas.style.width = `${containerWidth}px`;
            this.canvas.style.height = `${containerWidth / canvasAspect}px`;
        }
    }
}
