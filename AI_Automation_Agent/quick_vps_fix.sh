#!/bin/bash
# =============================================================================
# QUICK VPS FIX - Directory Structure and Virtual Environment
# Fixes immediate issues with paths and venv activation
# =============================================================================

set -e

echo "===================================================="
echo "QUICK VPS FIX - AI AUTOMATION AGENT"
echo "===================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[STEP 1]${NC} Checking current directory structure..."

# Get current working directory
CURRENT_DIR=$(pwd)
echo -e "${BLUE}[INFO]${NC} Current directory: $CURRENT_DIR"

# Navigate to project root if in subdirectory
if [[ "$CURRENT_DIR" == *"/AI_Automation_Agent" ]]; then
    echo -e "${BLUE}[INFO]${NC} Already in AI_Automation_Agent directory"
    PROJECT_ROOT="$CURRENT_DIR"
else
    echo -e "${YELLOW}[WARNING]${NC} Not in expected directory structure"
    if [[ -d "AI_Automation_Agent" ]]; then
        cd AI_Automation_Agent
        PROJECT_ROOT=$(pwd)
        echo -e "${GREEN}[SUCCESS]${NC} Navigated to: $PROJECT_ROOT"
    else
        echo -e "${RED}[ERROR]${NC} Cannot find AI_Automation_Agent directory"
        exit 1
    fi
fi

echo -e "${BLUE}[STEP 2]${NC} Checking for virtual environment..."

# Check for venv in current directory
if [[ -d "venv" ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} Virtual environment found in current directory"
    VENV_PATH="venv"
elif [[ -d "../venv" ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} Virtual environment found in parent directory"
    VENV_PATH="../venv"
else
    echo -e "${RED}[ERROR]${NC} No virtual environment found!"
    echo -e "${YELLOW}[INFO]${NC} Please create virtual environment first:"
    echo -e "${BLUE}   python3 -m venv venv${NC}"
    echo -e "${BLUE}   source venv/bin/activate${NC}"
    echo -e "${BLUE}   pip install -r requirements.txt${NC}"
    exit 1
fi

echo -e "${BLUE}[STEP 3]${NC} Checking for web_interface directory..."

if [[ ! -d "web_interface" ]]; then
    echo -e "${RED}[ERROR]${NC} web_interface directory not found!"
    echo -e "${BLUE}[INFO]${NC} Current directory contents:"
    ls -la
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} web_interface directory found"

echo -e "${BLUE}[STEP 4]${NC} Testing virtual environment..."

# Test venv activation
source $VENV_PATH/bin/activate
echo -e "${GREEN}[SUCCESS]${NC} Virtual environment activated"
echo -e "${BLUE}[INFO]${NC} Python version: $(python --version)"
echo -e "${BLUE}[INFO]${NC} Pip version: $(pip --version)"

echo -e "${BLUE}[STEP 5]${NC} Testing working_app.py..."

cd web_interface

if [[ ! -f "working_app.py" ]]; then
    echo -e "${RED}[ERROR]${NC} working_app.py not found in web_interface directory"
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} working_app.py found"

# Test imports
echo -e "${BLUE}[INFO]${NC} Testing required imports..."
python -c "import fastapi, uvicorn; print('✅ FastAPI and Uvicorn available')" || {
    echo -e "${RED}[ERROR]${NC} Required packages not installed"
    echo -e "${YELLOW}[INFO]${NC} Installing requirements..."
    pip install -r ../requirements.txt
}

echo -e "${BLUE}[STEP 6]${NC} Starting application..."

echo -e "${GREEN}[SUCCESS]${NC} All checks passed!"
echo -e "${BLUE}[INFO]${NC} Starting application in background..."
echo -e "${BLUE}[INFO]${NC} Dashboard will be available at: http://$(hostname -I | awk '{print $1}'):8000/"

# Create logs directory
mkdir -p ../logs

# Start in background
nohup python working_app.py > ../logs/agent.log 2>&1 &
PID=$!

# Save PID
echo $PID > ../agent.pid

# Wait and check
sleep 3

if kill -0 $PID 2>/dev/null; then
    echo -e "${GREEN}[SUCCESS]${NC} Application started successfully!"
    echo -e "${GREEN}[SUCCESS]${NC} Process ID: $PID"
    echo -e "${BLUE}[INFO]${NC} Dashboard URL: http://$(hostname -I | awk '{print $1}'):8000/"
    echo -e "${BLUE}[INFO]${NC} Logs: tail -f ../logs/agent.log"
    echo -e "${BLUE}[INFO]${NC} PID file: ../agent.pid"
    
    # Test endpoint
    sleep 2
    if curl -s -f http://localhost:8000/ > /dev/null; then
        echo -e "${GREEN}[SUCCESS]${NC} Web interface is responding!"
    else
        echo -e "${YELLOW}[WARNING]${NC} Web interface may not be fully ready yet"
    fi
else
    echo -e "${RED}[ERROR]${NC} Failed to start application"
    echo -e "${YELLOW}[INFO]${NC} Check logs: tail -f ../logs/agent.log"
    exit 1
fi

echo -e "${GREEN}[SUCCESS]${NC} Quick fix completed!"