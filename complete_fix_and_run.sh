#!/bin/bash

echo "🚀 Complete AI Automation Agent Fix & Setup"
echo "============================================="
echo "This script will fix all JavaScript, WebSocket, and service issues"
echo ""

# Check if we're in the right directory
if [ ! -d "AI_Automation_Agent" ]; then
    echo "❌ AI_Automation_Agent directory not found!"
    echo "Please run this script from the parent directory containing AI_Automation_Agent"
    exit 1
fi

cd AI_Automation_Agent

echo "📍 Current directory: $(pwd)"

# Step 1: Kill existing processes
echo ""
echo "🛑 Step 1: Stopping existing services..."
pkill -f "python.*start_web_interface.py" 2>/dev/null || true
pkill -f "python.*service_manager.py" 2>/dev/null || true
sleep 2
echo "✅ Existing services stopped"

# Step 2: Apply JavaScript fixes
echo ""
echo "🔧 Step 2: Applying JavaScript fixes..."

# Fix api.js - Remove duplicate WebSocketManager and fix base URL
echo "   📝 Fixing api.js..."
sed -i 's/const API = new APIClient('\''\'', {/const API = new APIClient(window.location.origin, {/g' web_interface/static/js/api.js

# Create a clean version of api.js without WebSocketManager duplication
cat > web_interface/static/js/api.js << 'EOF'
/**
 * AI Automation Agent - API Client
 * Handles all HTTP requests to the backend API
 */

class APIClient {
    constructor(baseURL = '', defaultHeaders = {}) {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            ...defaultHeaders
        };
        
        this.requestInterceptors = [];
        this.responseInterceptors = [];
    }

    /**
     * Add request interceptor
     */
    addRequestInterceptor(interceptor) {
        this.requestInterceptors.push(interceptor);
    }

    /**
     * Add response interceptor
     */
    addResponseInterceptor(interceptor) {
        this.responseInterceptors.push(interceptor);
    }

    /**
     * Build URL with base URL
     */
    buildURL(endpoint) {
        if (endpoint.startsWith('http')) {
            return endpoint;
        }
        return `${this.baseURL}${endpoint.startsWith('/') ? '' : '/'}${endpoint}`;
    }

    /**
     * Build request options
     */
    buildRequestOptions(options = {}) {
        const requestOptions = {
            ...options,
            headers: {
                ...this.defaultHeaders,
                ...options.headers
            }
        };

        // Apply request interceptors
        return this.requestInterceptors.reduce((options, interceptor) => {
            return interceptor(options) || options;
        }, requestOptions);
    }

    /**
     * Handle response
     */
    async handleResponse(response) {
        const responseData = await response.json().catch(() => ({}));
        
        // Apply response interceptors
        const processedResponse = this.responseInterceptors.reduce((data, interceptor) => {
            return interceptor(data, response) || data;
        }, responseData);

        if (!response.ok) {
            throw new APIError(
                processedResponse.message || `HTTP ${response.status}`,
                response.status,
                processedResponse
            );
        }

        return processedResponse;
    }

    /**
     * Make HTTP request
     */
    async request(endpoint, options = {}) {
        const url = this.buildURL(endpoint);
        const requestOptions = this.buildRequestOptions(options);

        try {
            const response = await fetch(url, requestOptions);
            return await this.handleResponse(response);
        } catch (error) {
            if (error instanceof APIError) {
                throw error;
            }
            
            // Network or other errors
            throw new APIError(
                error.message || 'Network error',
                0,
                { originalError: error }
            );
        }
    }

    /**
     * GET request
     */
    async get(endpoint, params = {}) {
        const url = new URL(this.buildURL(endpoint));
        
        Object.entries(params).forEach(([key, value]) => {
            if (value !== null && value !== undefined) {
                url.searchParams.set(key, value);
            }
        });

        return this.request(url.pathname + url.search, {
            method: 'GET'
        });
    }

    /**
     * POST request
     */
    async post(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }

    /**
     * PUT request
     */
    async put(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }

    /**
     * PATCH request
     */
    async patch(endpoint, data = {}) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });
    }
}

/**
 * API Error class
 */
class APIError extends Error {
    constructor(message, status = 0, data = {}) {
        super(message);
        this.name = 'APIError';
        this.status = status;
        this.data = data;
    }
}

/**
 * Create API client with default configuration
 */
const API = new APIClient(window.location.origin, {
    'Content-Type': 'application/json'
});

/**
 * Add global interceptors
 */

// Authentication interceptor (if token exists)
API.addRequestInterceptor((options) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
        options.headers['Authorization'] = `Bearer ${token}`;
    }
    return options;
});

// Error handling interceptor
API.addResponseInterceptor((data, response) => {
    // Log errors for debugging
    if (response.status >= 400) {
        console.error('API Error:', data);
    }
    return data;
});

/**
 * Create global instances
 */
window.API = API;
window.APIError = APIError;
EOF

# Fix dashboard.html - Change API to api
echo "   📝 Fixing dashboard.html..."
sed -i 's/{% block scripts %}/{% block scripts %}\n<script>\n\/\/ Initialize API client\nconst api = window.API;\n\n\/\/ Dashboard specific JavaScript\nclass Dashboard {/' web_interface/templates/dashboard.html
sed -i 's/await API\.get(/await api.get(/g' web_interface/templates/dashboard.html
sed -i 's/await API\.post(/await api.post(/g' web_interface/templates/dashboard.html

echo "✅ JavaScript fixes applied"

# Step 3: Create proper service management
echo ""
echo "🔧 Step 3: Setting up proper service management..."

# Create a robust startup script
cat > start_robust_service.py << 'EOF'
#!/usr/bin/env python3
"""
Robust startup script for AI Automation Agent
Handles startup, monitoring, and graceful shutdown
"""
import os
import sys
import signal
import subprocess
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ServiceManager:
    def __init__(self):
        self.process = None
        self.running = False
        
    def signal_handler(self, signum, frame):
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.shutdown()
        sys.exit(0)
        
    def start(self):
        """Start the AI Automation Agent service"""
        logger.info("🚀 Starting AI Automation Agent...")
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start the web interface
        try:
            self.process = subprocess.Popen(
                [sys.executable, "start_web_interface.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.running = True
            logger.info(f"✅ Service started with PID: {self.process.pid}")
            
            # Monitor the process
            self.monitor()
            
        except Exception as e:
            logger.error(f"❌ Failed to start service: {e}")
            return False
            
        return True
        
    def monitor(self):
        """Monitor the service and handle output"""
        try:
            while self.running and self.process.poll() is None:
                # Read output line by line
                line = self.process.stdout.readline()
                if line:
                    print(line.strip())
                    
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Error during monitoring: {e}")
        finally:
            self.shutdown()
            
    def shutdown(self):
        """Shutdown the service gracefully"""
        if self.running:
            logger.info("🛑 Shutting down service...")
            self.running = False
            
            if self.process:
                try:
                    # Try graceful shutdown first
                    self.process.terminate()
                    
                    # Wait for graceful shutdown
                    try:
                        self.process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        # Force kill if not responding
                        logger.warning("Force killing process...")
                        self.process.kill()
                        self.process.wait()
                        
                except Exception as e:
                    logger.error(f"Error during shutdown: {e}")
                    
                self.process = None
                
        logger.info("✅ Service shutdown complete")

def main():
    """Main entry point"""
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Add current directory to Python path
    sys.path.insert(0, str(script_dir))
    
    manager = ServiceManager()
    
    try:
        if manager.start():
            logger.info("🎉 AI Automation Agent is running!")
            logger.info("📋 To stop: Press Ctrl+C")
            logger.info("🌐 Access: http://localhost:8000")
        else:
            logger.error("❌ Failed to start service")
            return 1
            
    except KeyboardInterrupt:
        logger.info("👋 Goodbye!")
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
EOF

echo "✅ Service management setup complete"

# Step 4: Start the service
echo ""
echo "🚀 Step 4: Starting the service..."

# Start the robust service
python start_robust_service.py &
SERVICE_PID=$!

echo "✅ Service started with PID: $SERVICE_PID"

# Wait for startup
echo "⏳ Waiting for service to initialize..."
sleep 8

# Step 5: Verify everything is working
echo ""
echo "🔍 Step 5: Verification..."

# Check if service is running
if pgrep -f "start_web_interface.py" > /dev/null; then
    echo "✅ Web interface is running"
else
    echo "❌ Web interface is not running"
fi

# Test API endpoint
echo "🧪 Testing API endpoints..."
if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "✅ API is responding"
else
    echo "⚠️  API might still be starting up..."
fi

# Test WebSocket
echo "🧪 Testing WebSocket..."
python3 -c "
import socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex(('localhost', 8000))
    s.close()
    print('✅ WebSocket port is accessible' if result == 0 else '⚠️  WebSocket port not accessible')
except:
    print('⚠️  Could not test WebSocket port')
" 2>/dev/null

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "🌐 Access Points:"
IP=$(hostname -I | awk '{print $1}')
echo "   📱 Web Interface: http://$IP:8000"
echo "   📊 Health Check: http://$IP:8000/api/health"
echo "   🔌 WebSocket: ws://$IP:8000/ws"
echo ""
echo "📋 Management:"
echo "   🛑 Stop service: pkill -f start_web_interface.py"
echo "   📊 Check logs: tail -f web_interface.log"
echo "   🔄 Restart: pkill -f start_web_interface.py && sleep 2 && python start_robust_service.py &"
echo ""
echo "💡 Expected Results:"
echo "   ✅ Web interface should load completely"
echo "   ✅ No JavaScript errors in browser console"
echo "   ✅ Dashboard should show real data"
echo "   ✅ WebSocket should connect successfully"
echo "   ✅ Agent start/stop buttons should work"
echo ""
echo "🔧 If you still see issues:"
echo "   1. Check browser console for specific errors"
echo "   2. Verify MongoDB is running: sudo systemctl status mongod"
echo "   3. Check service logs: tail -f web_interface.log"
echo "   4. Ensure ports are not blocked by firewall"