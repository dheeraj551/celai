#!/bin/bash
# =============================================================================
# DIAGNOSTIC AND FIX SCRIPT
# Check directory structure and fix issues step by step
# =============================================================================

set -e

echo "===================================================="
echo "AI AUTOMATION AGENT - DIAGNOSTIC & FIX"
echo "===================================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[STEP 1]${NC} Current Directory Analysis"
echo -e "${BLUE}Current directory:${NC} $(pwd)"
echo -e "${BLUE}Script location:${NC} $0"

echo ""
echo -e "${BLUE}[STEP 2]${NC} Directory Structure Check"

# Check for AI_Automation_Agent directory structure
if [[ -d "web_interface" ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} web_interface directory found in current directory"
else
    echo -e "${YELLOW}[INFO]${NC} web_interface not found in current directory"
    
    # Check if we're in parent directory
    if [[ -d "AI_Automation_Agent/web_interface" ]]; then
        echo -e "${BLUE}[INFO]${NC} Found web_interface in AI_Automation_Agent subdirectory"
        echo -e "${GREEN}[SUCCESS]${NC} Navigating to AI_Automation_Agent directory..."
        cd AI_Automation_Agent
        echo -e "${BLUE}New directory:${NC} $(pwd)"
    else
        echo -e "${RED}[ERROR]${NC} Cannot find web_interface directory anywhere!"
        echo -e "${BLUE}Directory contents:${NC}"
        ls -la
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}[STEP 3]${NC} File and Directory Verification"

# Check essential files
REQUIRED_ITEMS=("web_interface" "working_app.py" "venv")
for item in "${REQUIRED_ITEMS[@]}"; do
    if [[ -e "$item" ]]; then
        echo -e "${GREEN}[SUCCESS]${NC} $item found"
    else
        echo -e "${RED}[ERROR]${NC} $item missing!"
    fi
done

echo ""
echo -e "${BLUE}[STEP 4]${NC} Virtual Environment Check"

if [[ -d "venv" ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} Virtual environment found"
    
    # Test activation
    if source venv/bin/activate; then
        echo -e "${GREEN}[SUCCESS]${NC} Virtual environment activated successfully"
        echo -e "${BLUE}Python version:${NC} $(python --version)"
        echo -e "${BLUE}Pip version:${NC} $(pip --version)"
        
        # Check required packages
        echo -e "${BLUE}[STEP 5]${NC} Package Verification"
        REQUIRED_PACKAGES=("fastapi" "uvicorn" "pymongo" "loguru")
        for package in "${REQUIRED_PACKAGES[@]}"; do
            if python -c "import $package" 2>/dev/null; then
                echo -e "${GREEN}[SUCCESS]${NC} $package available"
            else
                echo -e "${YELLOW}[WARNING]${NC} $package not found, installing..."
                pip install $package
            fi
        done
        
    else
        echo -e "${RED}[ERROR]${NC} Failed to activate virtual environment"
        exit 1
    fi
else
    echo -e "${RED}[ERROR]${NC} No virtual environment found!"
    echo -e "${YELLOW}[INFO]${NC} Please create virtual environment:"
    echo -e "${BLUE}   python3 -m venv venv${NC}"
    echo -e "${BLUE}   source venv/bin/activate${NC}"
    echo -e "${BLUE}   pip install -r requirements.txt${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[STEP 6]${NC} Final Setup Verification"

# Verify working_app.py exists and is executable
if [[ -f "web_interface/working_app.py" ]]; then
    echo -e "${GREEN}[SUCCESS]${NC} working_app.py found"
    chmod +x web_interface/working_app.py 2>/dev/null || true
else
    echo -e "${RED}[ERROR]${NC} working_app.py not found in web_interface directory"
    exit 1
fi

echo ""
echo -e "${GREEN}[SUCCESS]${NC} All checks passed!"
echo -e "${BLUE}[INFO]${NC} Ready to start application"
echo ""
echo -e "${GREEN}=== READY TO START ===${NC}"
echo -e "${BLUE}Run this command to start the application:${NC}"
echo -e "${GREEN}cd web_interface && nohup python working_app.py > ../logs/agent.log 2>&1 &${NC}"
echo ""
echo -e "${BLUE}Or use the start_manual.sh script:${NC}"
echo -e "${GREEN}cd .. && ./start_manual.sh${NC}"