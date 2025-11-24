#!/bin/bash
# =============================================================================
# VPS CONFIGURATION AND STARTUP FIX
# AI Automation Agent - Complete Fix for Database Connection and Permanent Startup
# =============================================================================

set -e

echo "===================================================="
echo "AI AUTOMATION AGENT - VPS CONFIG & STARTUP FIX"
echo "===================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$HOME/ai-automation-agent"
cd "$PROJECT_DIR" || { echo -e "${RED}Error: Cannot access $PROJECT_DIR${NC}"; exit 1; }

echo -e "${BLUE}[INFO]${NC} Working directory: $PROJECT_DIR"

# Function to check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        echo -e "${YELLOW}[WARNING]${NC} Running as root. Consider running as deploy user for security."
    fi
}

# Function to fix config file naming
fix_config_file() {
    echo -e "${BLUE}[STEP 1]${NC} Fixing configuration file naming..."
    
    if [[ -f "env.celorisdesigns" ]] && [[ ! -f ".env.celorisdesigns" ]]; then
        echo -e "${YELLOW}[INFO]${NC} Renaming env.celorisdesigns to .env.celorisdesigns"
        mv "env.celorisdesigns" ".env.celorisdesigns"
        echo -e "${GREEN}[SUCCESS]${NC} Config file renamed successfully"
    elif [[ -f ".env.celorisdesigns" ]]; then
        echo -e "${GREEN}[SUCCESS]${NC} Config file .env.celorisdesigns already exists"
    else
        echo -e "${YELLOW}[WARNING]${NC} No config file found. Creating from example..."
        if [[ -f ".env.example" ]]; then
            cp ".env.example" ".env.celorisdesigns"
            echo -e "${GREEN}[INFO]${NC} Created .env.celorisdesigns from example"
            echo -e "${YELLOW}[WARNING]${NC} Please edit .env.celorisdesigns with your actual database credentials"
        else
            echo -e "${RED}[ERROR]${NC} No config template found"
            return 1
        fi
    fi
}

# Function to verify Python environment
check_python_env() {
    echo -e "${BLUE}[STEP 2]${NC} Checking Python environment..."
    
    # Check if virtual environment exists
    if [[ ! -d "venv" ]]; then
        echo -e "${YELLOW}[INFO]${NC} Creating Python virtual environment..."
        python3 -m venv venv
        echo -e "${GREEN}[SUCCESS]${NC} Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install/upgrade required packages
    echo -e "${BLUE}[INFO]${NC} Installing/updating Python packages..."
    pip install --upgrade pip
    
    # Install required packages if requirements.txt exists
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
    else
        # Install essential packages
        pip install fastapi uvicorn jinja2 python-multipart loguru python-dotenv
    fi
    
    echo -e "${GREEN}[SUCCESS]${NC} Python environment ready"
}

# Function to stop existing processes
stop_existing_processes() {
    echo -e "${BLUE}[STEP 3]${NC} Stopping existing processes..."
    
    # Kill any running FastAPI processes on port 8000
    PORT=8000
    PIDS=$(lsof -t -i:$PORT 2>/dev/null || true)
    
    if [[ -n "$PIDS" ]]; then
        echo -e "${YELLOW}[INFO]${NC} Stopping processes on port $PORT: $PIDS"
        kill $PIDS 2>/dev/null || true
        sleep 2
        
        # Force kill if still running
        PIDS=$(lsof -t -i:$PORT 2>/dev/null || true)
        if [[ -n "$PIDS" ]]; then
            echo -e "${YELLOW}[INFO]${NC} Force stopping processes: $PIDS"
            kill -9 $PIDS 2>/dev/null || true
        fi
    fi
    
    # Also try to kill any working_app.py processes
    PIDS=$(pgrep -f "working_app.py" 2>/dev/null || true)
    if [[ -n "$PIDS" ]]; then
        echo -e "${YELLOW}[INFO]${NC} Stopping working_app.py processes: $PIDS"
        kill $PIDS 2>/dev/null || true
    fi
    
    echo -e "${GREEN}[SUCCESS]${NC} Existing processes stopped"
}

# Function to create systemd service
create_systemd_service() {
    echo -e "${BLUE}[STEP 4]${NC} Creating systemd service for permanent startup..."
    
    # Check if running as root for systemd service creation
    if [[ $EUID -ne 0 ]]; then
        echo -e "${YELLOW}[INFO]${NC} Not running as root. Skipping systemd service creation."
        echo -e "${BLUE}[INFO]${NC} To create systemd service, run: sudo $0"
        return 0
    fi
    
    SERVICE_FILE="/etc/systemd/system/ai-automation-agent.service"
    
    # Create systemd service file
    cat > "$SERVICE_FILE" << EOF
[Unit]
Description=AI Automation Agent Web Interface
After=network.target
Wants=network.target

[Service]
Type=simple
User=deploy
Group=deploy
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/python $PROJECT_DIR/web_interface/working_app.py
ExecReload=/bin/kill -HUP \$MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=5
PrivateTmp=true
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    echo -e "${GREEN}[SUCCESS]${NC} Systemd service file created at $SERVICE_FILE"
    
    # Reload systemd and enable service
    systemctl daemon-reload
    systemctl enable ai-automation-agent.service
    echo -e "${GREEN][SUCCESS]${NC} Service enabled to start on boot"
    
    # Start the service
    systemctl start ai-automation-agent.service
    sleep 3
    
    # Check service status
    if systemctl is-active --quiet ai-automation-agent.service; then
        echo -e "${GREEN}[SUCCESS]${NC} AI Automation Agent service is running"
        echo -e "${BLUE}[INFO]${NC} Dashboard URL: http://$(hostname -I | awk '{print $1}'):8000/"
    else
        echo -e "${RED}[ERROR]${NC} Service failed to start"
        systemctl status ai-automation-agent.service --no-pager
        return 1
    fi
}

# Function to start manually (fallback)
start_manually() {
    echo -e "${BLUE}[STEP 5]${NC} Starting application manually (background)..."
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Create logs directory
    mkdir -p logs
    
    # Start in background
    cd web_interface
    echo -e "${BLUE}[INFO]${NC} Starting AI Automation Agent with virtual environment..."
    nohup bash -c "source ../venv/bin/activate && python working_app.py" > ../logs/agent.log 2>&1 &
    cd ..
    
    # Get PID
    PID=$!
    echo $PID > agent.pid
    
    sleep 3
    
    # Check if process is running
    if kill -0 $PID 2>/dev/null; then
        echo -e "${GREEN}[SUCCESS]${NC} AI Automation Agent started successfully (PID: $PID)"
        echo -e "${BLUE}[INFO]${NC} Dashboard URL: http://$(hostname -I | awk '{print $1}'):8000/"
        echo -e "${BLUE}[INFO]${NC} Log file: logs/agent.log"
        echo -e "${BLUE}[INFO]${NC} PID file: agent.pid"
    else
        echo -e "${RED}[ERROR]${NC} Failed to start application"
        echo -e "${YELLOW}[INFO]${NC} Check logs: tail -f logs/agent.log"
        return 1
    fi
}

# Function to verify installation
verify_installation() {
    echo -e "${BLUE}[STEP 6]${NC} Verifying installation..."
    
    # Check if web interface is responding
    sleep 5
    
    if curl -s -f http://localhost:8000/ > /dev/null; then
        echo -e "${GREEN}[SUCCESS]${NC} Web interface is responding"
        
        # Check API endpoints
        if curl -s -f http://localhost:8000/api/status > /dev/null; then
            echo -e "${GREEN}[SUCCESS]${NC} API endpoints are working"
        else
            echo -e "${YELLOW}[WARNING]${NC} API endpoints may not be fully functional"
        fi
        
        echo -e "${GREEN}[SUCCESS]${NC} Installation verified successfully"
        echo -e ""
        echo -e "${GREEN}=== INSTALLATION COMPLETE ===${NC}"
        echo -e "${GREEN}Dashboard URL:${NC} http://$(hostname -I | awk '{print $1}'):8000/"
        echo -e "${GREEN}API Status:${NC} http://$(hostname -I | awk '{print $1}'):8000/api/status"
    else
        echo -e "${RED}[ERROR]${NC} Web interface is not responding"
        echo -e "${YELLOW}[INFO]${NC} Check logs for more details"
        return 1
    fi
}

# Function to show usage instructions
show_usage_instructions() {
    echo -e ""
    echo -e "${GREEN}=== USAGE INSTRUCTIONS ===${NC}"
    echo -e ""
    echo -e "${BLUE}Systemd Service Commands (recommended):${NC}"
    echo -e "  Start:   sudo systemctl start ai-automation-agent"
    echo -e "  Stop:    sudo systemctl stop ai-automation-agent"
    echo -e "  Status:  sudo systemctl status ai-automation-agent"
    echo -e "  Logs:    sudo journalctl -u ai-automation-agent -f"
    echo -e ""
    echo -e "${BLUE}Manual Process Commands:${NC}"
    echo -e "  Start:   cd $PROJECT_DIR && ./start_manual.sh"
    echo -e "  Stop:    kill \$(cat agent.pid)"
    echo -e "  Logs:    tail -f logs/agent.log"
    echo -e ""
    echo -e "${BLUE}Dashboard:${NC}"
    echo -e "  URL:     http://$(hostname -I | awk '{print $1}'):8000/"
    echo -e ""
    echo -e "${YELLOW}Configuration:${NC}"
    echo -e "  Edit:    nano $PROJECT_DIR/.env.celorisdesigns"
    echo -e ""
}

# Main execution
main() {
    echo -e "${BLUE}[INFO]${NC} Starting VPS configuration fix..."
    
    check_root
    fix_config_file
    check_python_env
    stop_existing_processes
    
    # Try systemd service first, fallback to manual
    if [[ $EUID -eq 0 ]]; then
        if ! create_systemd_service; then
            echo -e "${YELLOW}[WARNING]${NC} Systemd service failed, trying manual startup..."
            start_manually
        fi
    else
        start_manually
    fi
    
    verify_installation
    show_usage_instructions
    
    echo -e "${GREEN}[INFO]${NC} VPS configuration and startup fix completed!"
}

# Run main function
main "$@"