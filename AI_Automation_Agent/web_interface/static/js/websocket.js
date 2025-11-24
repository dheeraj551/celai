/**
 * AI Automation Agent - WebSocket Manager
 * Real-time communication and updates
 */

class WebSocketManager {
    constructor(url = null, options = {}) {
        this.url = url || this.getDefaultURL();
        this.options = {
            reconnectInterval: 1000,
            maxReconnectAttempts: 5,
            heartbeatInterval: 30000,
            ...options
        };
        
        this.ws = null;
        this.reconnectAttempts = 0;
        this.isConnecting = false;
        this.heartbeatTimer = null;
        this.listeners = new Map();
        this.messageQueue = [];
        this.connectionState = 'disconnected';
        
        this.bindMethods();
    }

    bindMethods() {
        this.handleOpen = this.handleOpen.bind(this);
        this.handleMessage = this.handleMessage.bind(this);
        this.handleClose = this.handleClose.bind(this);
        this.handleError = this.handleError.bind(this);
        this.sendHeartbeat = this.sendHeartbeat.bind(this);
        this.reconnect = this.reconnect.bind(this);
    }

    getDefaultURL() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.host;
        return `${protocol}//${host}/ws`;
    }

    /**
     * Connect to WebSocket
     */
    connect() {
        if (this.isConnecting || (this.ws && this.ws.readyState === WebSocket.OPEN)) {
            return Promise.resolve();
        }

        this.isConnecting = true;
        this.updateConnectionState('connecting');

        return new Promise((resolve, reject) => {
            try {
                this.ws = new WebSocket(this.url);
                
                this.ws.onopen = (event) => {
                    this.handleOpen(event);
                    resolve(event);
                };

                this.ws.onmessage = (event) => {
                    this.handleMessage(event);
                };

                this.ws.onclose = (event) => {
                    this.handleClose(event);
                };

                this.ws.onerror = (error) => {
                    this.handleError(error);
                    reject(error);
                };

            } catch (error) {
                this.isConnecting = false;
                this.updateConnectionState('error');
                reject(error);
            }
        });
    }

    /**
     * Disconnect WebSocket
     */
    disconnect() {
        this.clearHeartbeat();
        
        if (this.ws) {
            this.ws.close(1000, 'Manual disconnect');
            this.ws = null;
        }
        
        this.reconnectAttempts = 0;
        this.updateConnectionState('disconnected');
    }

    /**
     * Handle connection open
     */
    handleOpen(event) {
        console.log('WebSocket connected');
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.updateConnectionState('connected');
        
        // Start heartbeat
        this.startHeartbeat();
        
        // Flush message queue
        this.flushMessageQueue();
        
        // Emit connected event
        this.emit('connected', { event, timestamp: Date.now() });
    }

    /**
     * Handle incoming messages
     */
    handleMessage(event) {
        try {
            const data = JSON.parse(event.data);
            
            // Handle ping/pong for heartbeat
            if (data.type === 'ping') {
                this.send('pong', { timestamp: Date.now() });
                return;
            }
            
            if (data.type === 'pong') {
                // Update last heartbeat time
                this.lastHeartbeat = Date.now();
                return;
            }
            
            // Emit message to listeners
            this.emit(data.type || 'message', data.data || data);
            
            // Log debug info in development
            if (window.location.hostname === 'localhost') {
                console.log('WebSocket message received:', data);
            }
            
        } catch (error) {
            console.error('Failed to parse WebSocket message:', error);
            console.log('Raw message:', event.data);
        }
    }

    /**
     * Handle connection close
     */
    handleClose(event) {
        console.log('WebSocket closed:', event.code, event.reason);
        
        this.isConnecting = false;
        this.ws = null;
        this.clearHeartbeat();
        
        if (event.code !== 1000) { // Not a normal closure
            this.updateConnectionState('disconnected');
            this.emit('disconnected', { event, code: event.code, reason: event.reason });
            
            // Attempt to reconnect
            if (this.reconnectAttempts < this.options.maxReconnectAttempts) {
                setTimeout(() => {
                    this.reconnectAttempts++;
                    this.reconnect();
                }, this.options.reconnectInterval * this.reconnectAttempts);
            } else {
                this.updateConnectionState('failed');
                this.emit('failed', { attempts: this.reconnectAttempts });
            }
        } else {
            this.updateConnectionState('disconnected');
        }
    }

    /**
     * Handle connection error
     */
    handleError(error) {
        console.error('WebSocket error:', error);
        this.isConnecting = false;
        this.updateConnectionState('error');
        this.emit('error', { error });
    }

    /**
     * Attempt to reconnect
     */
    reconnect() {
        if (this.reconnectAttempts >= this.options.maxReconnectAttempts) {
            console.error('Max reconnection attempts reached');
            return;
        }
        
        console.log(`Attempting to reconnect... (${this.reconnectAttempts}/${this.options.maxReconnectAttempts})`);
        this.connect().catch(() => {
            // Reconnection failed, will retry automatically
        });
    }

    /**
     * Send message through WebSocket
     */
    send(type, data = {}) {
        const message = JSON.stringify({ type, data, timestamp: Date.now() });
        
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(message);
            return true;
        } else {
            // Queue message for when connection is established
            this.messageQueue.push({ type, data, timestamp: Date.now() });
            return false;
        }
    }

    /**
     * Flush queued messages
     */
    flushMessageQueue() {
        while (this.messageQueue.length > 0) {
            const message = this.messageQueue.shift();
            this.send(message.type, message.data);
        }
    }

    /**
     * Start heartbeat to keep connection alive
     */
    startHeartbeat() {
        this.clearHeartbeat();
        this.heartbeatTimer = setInterval(this.sendHeartbeat, this.options.heartbeatInterval);
    }

    /**
     * Clear heartbeat timer
     */
    clearHeartbeat() {
        if (this.heartbeatTimer) {
            clearInterval(this.heartbeatTimer);
            this.heartbeatTimer = null;
        }
    }

    /**
     * Send heartbeat ping
     */
    sendHeartbeat() {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.send('ping', { timestamp: Date.now() });
        }
    }

    /**
     * Add event listener
     */
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
        
        // Return unsubscribe function
        return () => this.off(event, callback);
    }

    /**
     * Remove event listener
     */
    off(event, callback) {
        if (this.listeners.has(event)) {
            const callbacks = this.listeners.get(event);
            const index = callbacks.indexOf(callback);
            if (index > -1) {
                callbacks.splice(index, 1);
            }
            
            // Clean up empty event arrays
            if (callbacks.length === 0) {
                this.listeners.delete(event);
            }
        }
    }

    /**
     * Add one-time event listener
     */
    once(event, callback) {
        const onceCallback = (data) => {
            callback(data);
            this.off(event, onceCallback);
        };
        return this.on(event, onceCallback);
    }

    /**
     * Emit event to listeners
     */
    emit(event, data) {
        if (this.listeners.has(event)) {
            this.listeners.get(event).forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    console.error('Error in WebSocket event listener:', error);
                }
            });
        }
    }

    /**
     * Update connection state
     */
    updateConnectionState(state) {
        this.connectionState = state;
        this.emit('stateChange', { state, timestamp: Date.now() });
        
        // Update UI status indicator if it exists
        const statusIndicator = document.getElementById('agentStatus');
        if (statusIndicator) {
            const statusDot = statusIndicator.querySelector('.status-dot');
            const statusText = statusIndicator.querySelector('.status-text');
            
            if (statusDot && statusText) {
                statusDot.className = `status-dot status-${state}`;
                statusText.textContent = this.getStateLabel(state);
            }
        }
    }

    /**
     * Get human-readable state label
     */
    getStateLabel(state) {
        const labels = {
            connecting: 'Connecting...',
            connected: 'Connected',
            disconnected: 'Disconnected',
            error: 'Error',
            failed: 'Failed'
        };
        return labels[state] || 'Unknown';
    }

    /**
     * Check if connected
     */
    isConnected() {
        return this.ws && this.ws.readyState === WebSocket.OPEN;
    }

    /**
     * Get connection state
     */
    getConnectionState() {
        return this.connectionState;
    }

    /**
     * Get queue size
     */
    getQueueSize() {
        return this.messageQueue.length;
    }

    /**
     * Clear message queue
     */
    clearQueue() {
        this.messageQueue = [];
    }

    /**
     * Get statistics
     */
    getStats() {
        return {
            connectionState: this.connectionState,
            reconnectAttempts: this.reconnectAttempts,
            queueSize: this.messageQueue.length,
            listenersCount: this.listeners.size,
            isConnected: this.isConnected(),
            lastHeartbeat: this.lastHeartbeat || null
        };
    }
}

/**
 * Specialized WebSocket for agent updates
 */
class AgentWebSocket extends WebSocketManager {
    constructor(options = {}) {
        super(null, {
            heartbeatInterval: 15000, // More frequent for agent monitoring
            ...options
        });
        
        this.setupAgentListeners();
    }

    setupAgentListeners() {
        // Agent status updates
        this.on('agent_status', (data) => {
            this.updateAgentStatus(data);
        });

        // Blog automation updates
        this.on('blog_generation', (data) => {
            this.handleBlogGenerationUpdate(data);
        });

        this.on('blog_published', (data) => {
            this.handleBlogPublishedUpdate(data);
        });

        // Analytics updates
        this.on('analytics_update', (data) => {
            this.handleAnalyticsUpdate(data);
        });

        // System updates
        this.on('system_status', (data) => {
            this.handleSystemStatusUpdate(data);
        });

        // Error notifications
        this.on('error_notification', (data) => {
            this.handleErrorNotification(data);
        });

        // Success notifications
        this.on('success_notification', (data) => {
            this.handleSuccessNotification(data);
        });
    }

    updateAgentStatus(data) {
        // Update agent status in UI
        const uptimeElement = document.getElementById('agentUptime');
        const modulesElement = document.getElementById('modulesLoaded');
        
        if (uptimeElement && data.uptime) {
            uptimeElement.textContent = Utils.formatUptime(data.uptime);
        }
        
        if (modulesElement && data.modules) {
            modulesElement.textContent = Object.keys(data.modules).length;
        }

        // Update status indicator
        this.updateConnectionState(data.is_running ? 'connected' : 'disconnected');
    }

    handleBlogGenerationUpdate(data) {
        // Show progress for blog generation
        toastManager.info(`Generating blog: ${data.title}`, {
            duration: 0 // Don't auto-hide
        });

        if (data.status === 'completed') {
            toastManager.success(`Blog generated successfully: ${data.title}`);
            
            // Refresh blog list if on blog automation page
            if (window.blogAutomation && typeof window.blogAutomation.loadBlogPosts === 'function') {
                setTimeout(() => window.blogAutomation.loadBlogPosts(), 2000);
            }
        } else if (data.status === 'failed') {
            toastManager.error(`Blog generation failed: ${data.error}`);
        }
    }

    handleBlogPublishedUpdate(data) {
        toastManager.success(`Blog published: ${data.title}`);
        
        // Refresh analytics
        if (window.analytics && typeof window.analytics.loadAnalyticsData === 'function') {
            setTimeout(() => window.analytics.loadAnalyticsData(), 1000);
        }
    }

    handleAnalyticsUpdate(data) {
        // Update analytics in real-time
        if (window.dashboard) {
            window.dashboard.updateAnalytics(data);
        }
    }

    handleSystemStatusUpdate(data) {
        // Update system status indicators
        const elements = {
            'databaseStatus': data.database_status,
            'aiStatus': data.ai_status
        };

        Object.entries(elements).forEach(([elementId, status]) => {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = status;
                element.className = `status-${status.toLowerCase()}`;
            }
        });
    }

    handleErrorNotification(data) {
        toastManager.error(data.message);
        
        // Log error for debugging
        console.error('Agent Error:', data);
    }

    handleSuccessNotification(data) {
        toastManager.success(data.message);
    }

    /**
     * Subscribe to specific updates
     */
    subscribe(updates) {
        this.send('subscribe', { updates });
    }

    /**
     * Unsubscribe from updates
     */
    unsubscribe(updates) {
        this.send('unsubscribe', { updates });
    }

    /**
     * Request current status
     */
    requestStatus() {
        this.send('request_status', { timestamp: Date.now() });
    }
}

/**
 * Initialize global WebSocket instances
 */
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main WebSocket for general updates
    window.websocket = new WebSocketManager();
    
    // Initialize agent-specific WebSocket
    window.agentWebSocket = new AgentWebSocket();
    
    // Auto-connect when page loads
    window.websocket.connect().catch((error) => {
        console.warn('Failed to connect to main WebSocket:', error);
    });
    
    window.agentWebSocket.connect().catch((error) => {
        console.warn('Failed to connect to agent WebSocket:', error);
    });
    
    // Handle visibility change to manage connections
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            // Pause heartbeats when page is hidden
            if (window.websocket.isConnected()) {
                window.websocket.clearHeartbeat();
            }
        } else {
            // Resume heartbeats when page becomes visible
            if (window.websocket.isConnected()) {
                window.websocket.startHeartbeat();
            }
            // Request fresh status
            window.agentWebSocket.requestStatus();
        }
    });
    
    // Connection state indicator
    if (window.websocket) {
        window.websocket.on('stateChange', (data) => {
            console.log('Connection state changed:', data.state);
        });
    }
    
    // Cleanup on page unload
    window.addEventListener('beforeunload', () => {
        window.websocket.disconnect();
        window.agentWebSocket.disconnect();
    });
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { WebSocketManager, AgentWebSocket };
}