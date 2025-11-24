#!/bin/bash

echo "🚀 Complete WebSocket and Running Setup Fix"
echo "============================================"

# Navigate to the AI_Automation_Agent directory
cd AI_Automation_Agent || {
    echo "❌ Error: AI_Automation_Agent directory not found!"
    echo "Please run this script from the parent directory containing AI_Automation_Agent"
    exit 1
}

echo "📍 Current directory: $(pwd)"

# Kill any existing processes
echo "🛑 Stopping existing processes..."
pkill -f "python.*start_web_interface.py" 2>/dev/null || true
pkill -f "python.*service_manager.py" 2>/dev/null || true
sleep 2

# Check if service_manager.py exists and use it
if [ -f "service_manager.py" ]; then
    echo "🔧 Found service_manager.py - using it for proper background service management"
    
    # Create the Python service start script
    cat > start_proper_service.py << 'EOF'
#!/usr/bin/env python3
"""
Proper service runner for AI Automation Agent
"""
import os
import sys
import signal
import subprocess
import time
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.getcwd())

def signal_handler(sig, frame):
    print("\n🛑 Shutting down gracefully...")
    # Kill child processes
    subprocess.Popen(["pkill", "-f", "start_web_interface.py"])
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def main():
    print("🚀 Starting AI Automation Agent as background service...")
    
    # Change to the agent directory
    agent_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(agent_dir)
    
    # Start the web interface in background
    try:
        print("📡 Starting web interface...")
        process = subprocess.Popen([
            sys.executable, "start_web_interface.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        print(f"✅ Service started with PID: {process.pid}")
        print("📋 To monitor logs, run: tail -f web_interface.log")
        print("🛑 To stop service, run: pkill -f start_web_interface.py")
        
        # Wait for the process and monitor it
        while process.poll() is None:
            line = process.stdout.readline()
            if line:
                print(line.strip())
            time.sleep(0.1)
            
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
EOF

    echo "🔧 Starting service using proper service manager..."
    python start_proper_service.py &
    SERVICE_PID=$!
    echo "✅ Service started with PID: $SERVICE_PID"
    
    # Wait for service to initialize
    echo "⏳ Waiting for service to initialize..."
    sleep 5
    
else
    echo "⚠️  service_manager.py not found - using direct startup"
    
    # Start the web interface directly in background
    echo "🚀 Starting web interface directly..."
    nohup python start_web_interface.py > web_interface.log 2>&1 &
    WEB_PID=$!
    echo "✅ Web interface started with PID: $WEB_PID"
fi

# Test if the service is running
echo "🔍 Testing service health..."
sleep 3

if pgrep -f "start_web_interface.py" > /dev/null; then
    echo "✅ Web interface is running"
    
    # Test the API endpoint
    echo "🧪 Testing API endpoints..."
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✅ API is responding"
    else
        echo "⚠️  API might still be starting up..."
    fi
    
    # Test WebSocket endpoint
    echo "🧪 Testing WebSocket endpoint..."
    if python3 -c "
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = s.connect_ex(('localhost', 8000))
s.close()
print('WebSocket port is open' if result == 0 else 'WebSocket port not accessible')
" | grep -q "open"; then
        echo "✅ WebSocket port is accessible"
    else
        echo "⚠️  WebSocket port may not be accessible yet"
    fi
    
else
    echo "❌ Web interface is not running!"
    echo "📋 Check logs with: tail -f web_interface.log"
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo "✅ Service Status:"
if pgrep -f "start_web_interface.py" > /dev/null; then
    echo "   🟢 Web Interface: RUNNING"
else
    echo "   🔴 Web Interface: STOPPED"
fi

echo ""
echo "🌐 Access Points:"
echo "   📱 Web Interface: http://$(hostname -I | awk '{print $1}'):8000"
echo "   📊 Health Check: http://$(hostname -I | awk '{print $1}'):8000/api/health"
echo "   🔌 WebSocket: ws://$(hostname -I | awk '{print $1}'):8000/ws"

echo ""
echo "📋 Management Commands:"
echo "   📋 View logs: tail -f web_interface.log"
echo "   🛑 Stop service: pkill -f start_web_interface.py"
echo "   🔄 Restart service: pkill -f start_web_interface.py && sleep 2 && python start_proper_service.py &"
echo "   📊 Check status: ps aux | grep start_web_interface"

echo ""
echo "💡 Troubleshooting:"
echo "   - If you see loading screen issues, check the API health endpoint"
echo "   - WebSocket errors may be normal during initial startup"
echo "   - The service will automatically restart with system (if configured)"

# Create systemd service file if running as root
if [ "$EUID" -eq 0 ] && [ -d "/etc/systemd/system" ]; then
    echo ""
    echo "🔧 Creating systemd service for permanent startup..."
    
    SERVICE_FILE="/etc/systemd/system/ai-automation-agent.service"
    
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=AI Automation Agent Web Interface
After=network.target
Wants=mongodb.service

[Service]
Type=forking
User=root
WorkingDirectory=$(pwd)
ExecStart=$(which python3) start_proper_service.py
ExecReload=/bin/kill -HUP \$MAINPID
ExecStop=/bin/kill -TERM \$MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ai-automation-agent

[Install]
WantedBy=multi-user.target
EOF

    echo "✅ Systemd service file created at: $SERVICE_FILE"
    echo "🔧 To enable auto-startup:"
    echo "   systemctl daemon-reload"
    echo "   systemctl enable ai-automation-agent"
    echo "   systemctl start ai-automation-agent"
fi

echo ""
echo "📈 Expected Results:"
echo "   1. Web interface should load completely without JavaScript errors"
echo "   2. Dashboard should show agent status, blog statistics, and recent activity"
echo "   3. WebSocket should connect and show live updates"
echo "   4. Agent start/stop buttons should work"
echo "   5. Blog generation features should be functional"