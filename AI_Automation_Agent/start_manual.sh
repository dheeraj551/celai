#!/bin/bash
# =============================================================================
# MANUAL STARTUP SCRIPT - AI AUTOMATION AGENT
# Simplified script to start the application in background
# =============================================================================

set -e

echo "===================================================="
echo "AI AUTOMATION AGENT - MANUAL STARTUP"
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

# Function to check if config file exists with correct name
check_config_file() {
    if [[ ! -f ".env.celorisdesigns" ]]; then
        echo -e "${YELLOW}[WARNING]${NC} Configuration file .env.celorisdesigns not found"
        
        if [[ -f "env.celorisdesigns" ]]; then
            echo -e "${YELLOW}[INFO]${NC} Found env.celorisdesigns (missing dot), renaming..."
            mv "env.celorisdesigns" ".env.celorisdesigns"
            echo -e "${GREEN}[SUCCESS]${NC} Config file renamed to .env.celorisdesigns"
        else
            echo -e "${YELLOW}[INFO]${NC} Creating config file from example..."
            if [[ -f ".env.example" ]]; then
                cp ".env.example" ".env.celorisdesigns"
                echo -e "${GREEN}[INFO]${NC} Created .env.celorisdesigns from example"
                echo -e "${YELLOW}[WARNING]${NC} Please edit .env.celorisdesigns with your actual credentials"
            else
                echo -e "${RED}[ERROR]${NC} No config template found"
                return 1
            fi
        fi
    else
        echo -e "${GREEN}[SUCCESS]${NC} Config file .env.celorisdesigns found"
    fi
}

# Function to stop existing processes
stop_existing() {
    echo -e "${BLUE}[INFO]${NC} Checking for existing processes..."
    
    # Stop processes on port 8000
    PIDS=$(lsof -t -i:8000 2>/dev/null || true)
    if [[ -n "$PIDS" ]]; then
        echo -e "${YELLOW}[INFO]${NC} Stopping existing processes on port 8000: $PIDS"
        kill $PIDS 2>/dev/null || true
        sleep 2
    fi
    
    # Stop working_app.py processes
    PIDS=$(pgrep -f "working_app.py" 2>/dev/null || true)
    if [[ -n "$PIDS" ]]; then
        echo -e "${YELLOW}[INFO]${NC} Stopping existing working_app.py processes: $PIDS"
        kill $PIDS 2>/dev/null || true
        sleep 1
    fi
    
    # Remove old PID file if exists
    [[ -f "agent.pid" ]] && rm -f agent.pid
    
    echo -e "${GREEN}[SUCCESS]${NC} Existing processes stopped"
}

# Function to start application
start_application() {
    echo -e "${BLUE}[INFO]${NC} Starting AI Automation Agent..."
    
    # Get current working directory
    CURRENT_DIR=$(pwd)
    echo -e "${BLUE}[INFO]${NC} Current working directory: $CURRENT_DIR"
    
    # Check if web_interface exists in current directory
    if [[ ! -d "web_interface" ]]; then
        echo -e "${RED}[ERROR]${NC} web_interface directory not found in: $CURRENT_DIR"
        echo -e "${BLUE}[INFO]${NC} Contents of current directory:"
        ls -la
        echo -e ""
        echo -e "${YELLOW}[INFO]${NC} You need to run this script from the AI_Automation_Agent directory"
        echo -e "${BLUE}   cd ~/ai-automation-agent/AI_Automation_Agent${NC}"
        echo -e "${BLUE}   ./start_manual.sh${NC}"
        return 1
    fi
    
    echo -e "${GREEN}[SUCCESS]${NC} web_interface directory found"
    
    # Activate virtual environment
    if [[ -d "venv" ]]; then
        source venv/bin/activate
        echo -e "${GREEN}[SUCCESS]${NC} Virtual environment activated"
        echo -e "${BLUE}[INFO]${NC} Python: $(python --version)"
    else
        echo -e "${YELLOW}[WARNING]${NC} No virtual environment found, using system Python"
        echo -e "${YELLOW}[INFO]${NC} Please ensure all dependencies are installed"
    fi
    
    # Create logs directory
    mkdir -p logs
    
    # Start application in background
    cd web_interface
    echo -e "${BLUE}[INFO]${NC} Starting web interface on port 8000..."
    echo -e "${BLUE}[INFO]${NC} Current directory: $(pwd)"
    
    # Start with venv if available
    if [[ -n "$VIRTUAL_ENV" ]]; then
        echo -e "${GREEN}[SUCCESS]${NC} Running with virtual environment: $VIRTUAL_ENV"
        nohup python working_app.py > ../logs/agent.log 2>&1 &
    else
        echo -e "${YELLOW}[WARNING]${NC} Running without virtual environment"
        nohup python3 working_app.py > ../logs/agent.log 2>&1 &
    fi
    PID=$!
    cd ..
    
    # Save PID
    echo $PID > agent.pid
    
    # Wait a moment and check if process is running
    sleep 3
    
    if kill -0 $PID 2>/dev/null; then
        echo -e "${GREEN}[SUCCESS]${NC} Application started successfully!"
        echo -e "${GREEN}[SUCCESS]${NC} Process ID: $PID"
        echo -e "${BLUE}[INFO]${NC} Dashboard URL: http://$(hostname -I | awk '{print $1}'):8000/"
        echo -e "${BLUE}[INFO]${NC} Log file: logs/agent.log"
        echo -e "${BLUE}[INFO]${NC} PID file: agent.pid"
        
        # Test the interface
        sleep 2
        if curl -s -f http://localhost:8000/ > /dev/null; then
            echo -e "${GREEN}[SUCCESS]${NC} Web interface is responding!"
        else
            echo -e "${YELLOW}[WARNING]${NC} Web interface may not be fully ready yet"
        fi
        
        return 0
    else
        echo -e "${RED}[ERROR]${NC} Failed to start application"
        echo -e "${YELLOW}[INFO]${NC} Check logs: tail -f logs/agent.log"
        return 1
    fi
}

# Function to show usage instructions
show_instructions() {
    echo -e ""
    echo -e "${GREEN}=== USAGE INSTRUCTIONS ===${NC}"
    echo -e ""
    echo -e "${BLUE}Monitor Application:${NC}"
    echo -e "  View logs:     tail -f logs/agent.log"
    echo -e "  Check status:  cat agent.pid"
    echo -e "  Test endpoint: curl http://localhost:8000/api/status"
    echo -e ""
    echo -e "${BLUE}Control Application:${NC}"
    echo -e "  Stop:          kill \$(cat agent.pid)"
    echo -e "  Restart:       $0"
    echo -e ""
    echo -e "${BLUE}Configuration:${NC}"
    echo -e "  Edit config:   nano .env.celorisdesigns"
    echo -e ""
    echo -e "${BLUE}Dashboard:${NC}"
    echo -e "  URL:           http://$(hostname -I | awk '{print $1}'):8000/"
    echo -e ""
}

# Main execution
main() {
    echo -e "${BLUE}[INFO]${NC} Starting AI Automation Agent in manual mode..."
    
    check_config_file
    stop_existing
    start_application
    
    show_instructions
    
    echo -e "${GREEN}[INFO]${NC} Manual startup completed!"
}

# Show help if requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    echo "AI Automation Agent - Manual Startup Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo ""
    echo "This script:"
    echo "  1. Checks and fixes config file naming"
    echo "  2. Stops any existing processes"
    echo "  3. Starts the web interface in background"
    echo "  4. Verifies the application is running"
    echo ""
    exit 0
fi

# Run main function
main "$@"