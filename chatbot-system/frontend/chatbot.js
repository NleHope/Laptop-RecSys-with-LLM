class ChatBot {
    constructor() {
        this.apiUrl = 'http://localhost:8000';
        this.sessionId = null;
        this.isOpen = false;
        this.isMinimized = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.createNewSession();
        this.updateTime();
    }
    
    initializeElements() {
        this.chatWidget = document.getElementById('chatWidget');
        this.chatToggle = document.getElementById('chatToggle');
        this.chatHeader = document.getElementById('chatHeader');
        this.minimizeBtn = document.getElementById('minimizeBtn');
        this.chatMessages = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendBtn = document.getElementById('sendBtn');
        this.notificationBadge = document.getElementById('notificationBadge');
    }
    
    setupEventListeners() {
        // Toggle chat widget
        this.chatToggle.addEventListener('click', () => this.toggleChat());
        
        // Minimize/maximize
        this.chatHeader.addEventListener('click', () => this.toggleMinimize());
        this.minimizeBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.toggleMinimize();
        });
        
        // Send message
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Auto-resize input
        this.chatInput.addEventListener('input', () => {
            this.sendBtn.disabled = this.chatInput.value.trim() === '';
        });
    }
    
    async createNewSession() {
        try {
            const response = await fetch(`${this.apiUrl}/session/new`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            const data = await response.json();
            this.sessionId = data.session_id;
            console.log('New session created:', this.sessionId);
        } catch (error) {
            console.error('Error creating session:', error);
            // Fallback to random session ID
            this.sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
        }
    }
    
    toggleChat() {
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            this.chatWidget.classList.add('open');
            this.chatToggle.style.display = 'none';
            this.notificationBadge.classList.add('hidden');
            this.chatInput.focus();
        } else {
            this.chatWidget.classList.remove('open');
            this.chatToggle.style.display = 'flex';
            if (this.isMinimized) {
                this.chatWidget.classList.remove('minimized');
                this.isMinimized = false;
            }
        }
    }
    
    toggleMinimize() {
        if (!this.isOpen) return;
        
        this.isMinimized = !this.isMinimized;
        
        if (this.isMinimized) {
            this.chatWidget.classList.add('minimized');
            this.minimizeBtn.innerHTML = '+';
        } else {
            this.chatWidget.classList.remove('minimized');
            this.minimizeBtn.innerHTML = '−';
            this.chatInput.focus();
        }
    }
    
    async sendMessage() {
        const message = this.chatInput.value.trim();
        if (!message || !this.sessionId) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.chatInput.value = '';
        this.sendBtn.disabled = true;
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    session_id: this.sessionId
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            // Add bot response
            this.addMessage(data.reply, 'bot');
            
            // Show product recommendations if available
            if (data.recommended_products && data.recommended_products.length > 0) {
                this.showProductRecommendations(data.recommended_products);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.addMessage('Sorry, I\'m having trouble connecting right now. Please try again later.', 'bot');
        }
        
        this.scrollToBottom();
    }
    
    addMessage(content, sender, isHTML = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (isHTML) {
            messageContent.innerHTML = content;
        } else {
            messageContent.textContent = content;
        }
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        messageDiv.appendChild(messageContent);
        messageDiv.appendChild(messageTime);
        
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Show notification if chat is closed
        if (!this.isOpen && sender === 'bot') {
            this.showNotification();
        }
    }
    
    showProductRecommendations(products) {
        const recommendationsDiv = document.createElement('div');
        recommendationsDiv.className = 'message bot-message';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        const title = document.createElement('div');
        title.innerHTML = '<strong>📱 Recommended Products:</strong>';
        contentDiv.appendChild(title);
        
        const productsContainer = document.createElement('div');
        productsContainer.className = 'product-recommendations';
        
        products.forEach(product => {
            const productCard = this.createProductCard(product);
            productsContainer.appendChild(productCard);
        });
        
        contentDiv.appendChild(productsContainer);
        
        const messageTime = document.createElement('div');
        messageTime.className = 'message-time';
        messageTime.textContent = this.getCurrentTime();
        
        recommendationsDiv.appendChild(contentDiv);
        recommendationsDiv.appendChild(messageTime);
        
        this.chatMessages.appendChild(recommendationsDiv);
        this.scrollToBottom();
    }
    
    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card-mini';
        card.onclick = () => this.showProductDetails(product);
        
        card.innerHTML = `
            <div class="product-name">${product.name}</div>
            <div class="product-price">$${product.price.toFixed(2)}</div>
            <div class="product-specs">
                ${product.ram}GB RAM • ${product.storage}GB Storage • ${product.weight}kg
                ${product.processor ? ' • ' + product.processor : ''}
            </div>
        `;
        
        return card;
    }
    
    showProductDetails(product) {
        const details = `
            <strong>${product.name}</strong><br>
            💰 Price: $${product.price.toFixed(2)}<br>
            💾 RAM: ${product.ram}GB<br>
            💿 Storage: ${product.storage}GB<br>
            ⚖️ Weight: ${product.weight}kg<br>
            🖥️ Screen: ${product.screen_size}"<br>
            🔧 Processor: ${product.processor}<br>
            🔋 Battery: ${product.battery_life} hours<br>
            ${product.description}<br><br>
            Would you like more information about this product or see other options?
        `;
        
        this.addMessage(details, 'bot', true);
    }
    
    showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.innerHTML = `
            <div class="message-content typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
    }
    
    hideTypingIndicator() {
        const typingMessage = this.chatMessages.querySelector('.typing-message');
        if (typingMessage) {
            typingMessage.remove();
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    updateTime() {
        const initialTime = document.getElementById('initialTime');
        if (initialTime) {
            initialTime.textContent = this.getCurrentTime();
        }
    }
    
    showNotification() {
        this.notificationBadge.classList.remove('hidden');
        this.notificationBadge.textContent = '!';
        
        // Optional: Add a gentle shake animation
        this.chatToggle.style.animation = 'pulse 0.5s ease-in-out';
        setTimeout(() => {
            this.chatToggle.style.animation = '';
        }, 500);
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new ChatBot();
});

// Add pulse animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);
