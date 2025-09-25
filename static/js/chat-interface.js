// Chat Interface Controller

class ChatInterface {
    constructor() {
        this.messagesContainer = document.getElementById('messages-container');
        this.messageCount = 0;
        this.isTyping = false;
    }

    addUserMessage(text) {
        const messageEl = this.createMessage('user', text);
        this.appendMessage(messageEl);
        console.log('👤 User message added:', text.substring(0, 50));
    }

    addAIMessage(text) {
        this.showTypingIndicator();
        
        // Simulate typing delay for better UX
        setTimeout(() => {
            this.hideTypingIndicator();
            const messageEl = this.createMessage('ai', text);
            this.appendMessage(messageEl);
            console.log('🤖 AI message added:', text.substring(0, 50));
        }, 800);
    }

    addSystemMessage(text) {
        const messageEl = this.createMessage('system', text);
        this.appendMessage(messageEl);
    }

    addErrorMessage(text) {
        const messageEl = this.createMessage('error', text);
        this.appendMessage(messageEl);
    }

    createMessage(type, content) {
        const messageEl = document.createElement('div');
        messageEl.className = `${type}-message`;
        
        const avatar = document.createElement('div');
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        switch(type) {
            case 'user':
                avatar.className = 'user-avatar';
                avatar.innerHTML = '<i class="fas fa-user"></i>';
                messageContent.innerHTML = `<p>${this.escapeHtml(content)}</p>`;
                messageEl.appendChild(messageContent);
                messageEl.appendChild(avatar);
                break;
                
            case 'ai':
                avatar.className = 'ai-avatar';
                avatar.innerHTML = '<i class="fas fa-robot"></i>';
                messageContent.innerHTML = this.formatAIMessage(content);
                messageEl.appendChild(avatar);
                messageEl.appendChild(messageContent);
                break;
                
            case 'system':
                messageEl.className = 'system-message';
                messageEl.innerHTML = `
                    <div class="system-content">
                        <i class="fas fa-info-circle"></i>
                        <span>${this.escapeHtml(content)}</span>
                    </div>
                `;
                break;
                
            case 'error':
                messageEl.className = 'error-message';
                messageEl.innerHTML = `
                    <div class="error-content">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span>${this.escapeHtml(content)}</span>
                    </div>
                `;
                break;
        }
        
        this.messageCount++;
        return messageEl;
    }

    formatAIMessage(content) {
        // Convert markdown-style formatting to HTML
        let formatted = content
            // Bold text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // Italic text
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // Code inline
            .replace(/`(.*?)`/g, '<code>$1</code>')
            // Line breaks
            .replace(/\n/g, '<br>');
            
        // Split into paragraphs
        const paragraphs = formatted.split('<br><br>').map(p => 
            p.trim() ? `<p>${p}</p>` : ''
        ).filter(p => p);
        
        return paragraphs.join('');
    }

    appendMessage(messageEl) {
        // Remove welcome message if it's the first real message
        if (this.messageCount === 1) {
            const welcomeMsg = this.messagesContainer.querySelector('.welcome-message');
            if (welcomeMsg && !messageEl.classList.contains('system-message')) {
                welcomeMsg.style.opacity = '0.5';
            }
        }
        
        this.messagesContainer.appendChild(messageEl);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const typingEl = document.createElement('div');
        typingEl.className = 'ai-message typing-message';
        typingEl.innerHTML = `
            <div class="ai-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="typing-indicator">
                    AI is thinking
                    <span class="typing-dots">
                        <span>.</span><span>.</span><span>.</span>
                    </span>
                </div>
            </div>
        `;
        
        this.messagesContainer.appendChild(typingEl);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingMsg = this.messagesContainer.querySelector('.typing-message');
        if (typingMsg) {
            typingMsg.remove();
        }
        this.isTyping = false;
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    clear() {
        this.messagesContainer.innerHTML = '';
        this.messageCount = 0;
    }
}

// Additional CSS for chat features (add to style.css)
const additionalChatStyles = `
.system-message, .error-message {
    margin: 12px 0;
    text-align: center;
}

.system-content, .error-content {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    border-radius: var(--radius-sm);
    font-size: 13px;
    font-weight: 500;
}

.system-content {
    background: var(--bg-tertiary);
    color: var(--text-secondary);
    border: 1px solid var(--border-color);
}

.error-content {
    background: #fef2f2;
    color: var(--danger-color);
    border: 1px solid #fecaca;
}

.typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-muted);
    font-style: italic;
}

.typing-dots {
    display: flex;
    gap: 2px;
}

.typing-dots span {
    width: 4px;
    height: 4px;
    background: var(--text-muted);
    border-radius: 50%;
    animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typingBounce {
    0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

.message-content code {
    background: var(--bg-tertiary);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'SF Mono', Monaco, monospace;
    font-size: 12px;
}

.message-content strong {
    font-weight: 600;
}

.message-content em {
    font-style: italic;
}
`;

// Inject additional styles
const styleEl = document.createElement('style');
styleEl.textContent = additionalChatStyles;
document.head.appendChild(styleEl);
