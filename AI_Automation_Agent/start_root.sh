#!/bin/bash
# =============================================================================
# SIMPLE ROOT DIRECTORY STARTUP
# AI Automation Agent - Start from root directory (like start_web_interface.py)
# =============================================================================

set -e

echo "===================================================="
echo "AI AUTOMATION AGENT - ROOT STARTUP"
echo "===================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}[INFO]${NC} Working directory: $PROJECT_DIR"

# Kill existing processes
echo -e "${BLUE}[INFO]${NC} Stopping existing processes..."

pkill -f "start_web_interface.py" 2>/dev/null || true
pkill -f "working_app.py" 2>/dev/null || true
pkill -f "working_agent.py" 2>/dev/null || true
pkill -f "app.py" 2>/dev/null || true

# Activate virtual environment
if [[ -d "venv" ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} Activating virtual environment..."
    source venv/bin/activate
    echo -e "${BLUE}[INFO]${NC} Python: $(python --version)"
else
    echo -e "${YELLOW}[WARNING]${NC} No virtual environment found"
fi

# Create logs directory
mkdir -p logs

# Start application in background
echo -e "${BLUE}[INFO]${NC} Starting AI Automation Agent..."
echo -e "${BLUE}[INFO]${NC} Using working_agent.py (root directory version)"

nohup python working_agent.py > logs/agent.log 2>&1 &
PID=$!

# Save PID
echo $PID > agent.pid

# Wait and check if process is running
sleep 3

if kill -0 $PID 2>/dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} Application started successfully!"
    echo -e "${GREEN}[SUCCESS]${NC} Process ID: $PID"
    echo -e "${BLUE}[INFO]${NC} Dashboard URL: http://$(hostname -I | awk '{print $1}'):8000/"
    echo -e "${BLUE}[INFO]${NC} Log file: logs/agent.log"
    echo -e "${BLUE}[INFO]${NC} PID file: agent.pid"
    echo ""
    echo -e "${GREEN}=== APPLICATION RUNNING ===${NC}"
    echo -e "${BLUE}Monitor:${NC} tail -f logs/agent.log"
    echo -e "${BLUE}Stop:${NC} kill $PID"
    echo -e "${BLUE}Dashboard:${NC} http://$(hostname -I | awk '{print $1}'):8000/"
    
    # Test the interface
    sleep 2
    if curl -s -f http://localhost:8000/ > /dev/null; then
        echo -e "${GREEN}[SUCCESS]${NC} Web interface is responding!"
    else
        echo -e "${YELLOW}[WARNING]${NC} Web interface may not be fully ready yet"
    fi
else
    echo -e "${RED}[ERROR]${NC} Failed to start application"
    echo -e "${YELLOW}[INFO]${NC} Check logs: tail -f logs/agent.log"
    exit 1
fi