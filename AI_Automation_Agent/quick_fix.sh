#!/bin/bash

# AI Automation Agent - Quick Setup and Fix Script
# Addresses: Loading icon issue and terminal dependency

set -e

echo "=================================================="
echo "AI AUTOMATION AGENT - QUICK FIX & SETUP"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "start_web_interface.py" ]; then
    print_error "Please run this script from the AI_Automation_Agent directory"
    exit 1
fi

print_info "Starting AI Automation Agent setup and fix..."
echo ""

# Step 1: Check Python and dependencies
print_info "Step 1: Checking Python and dependencies..."

python_version=$(python3 --version 2>/dev/null || echo "not found")
if [[ $python_version == *"Python 3"* ]]; then
    print_status "Python 3 found: $python_version"
else
    print_error "Python 3 not found. Please install Python 3.7+"
    exit 1
fi

# Install/upgrade pip
print_info "Installing/upgrading pip..."
pip3 install --upgrade pip

# Install required packages
print_info "Installing required Python packages..."
pip3 install fastapi uvicorn pymongo loguru python-dotenv jinja2 python-multipart requests

print_status "Dependencies installed successfully"
echo ""

# Step 2: Setup environment
print_info "Step 2: Setting up environment..."

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.celorisdesigns" ]; then
        cp .env.celorisdesigns .env
        print_status "Copied .env.celorisdesigns to .env"
    else
        print_error "No environment file found. Please create .env or .env.celorisdesigns"
        exit 1
    fi
else
    print_status "Environment file exists"
fi

# Ensure correct port configuration
print_info "Configuring web interface port..."
sed -i 's/CHATBOT_PORT=8080/CHATBOT_PORT=8000/g' .env
sed -i 's/DEBUG=false/DEBUG=true/g' .env
print_status "Port set to 8000, Debug enabled"
echo ""

# Step 3: Setup MongoDB
print_info "Step 3: Checking MongoDB..."

# Check if MongoDB is installed
if command -v mongod &> /dev/null; then
    print_status "MongoDB is installed"
else
    print_warning "MongoDB not found. Installing..."
    sudo apt update
    sudo apt install -y mongodb
fi

# Start MongoDB
print_info "Starting MongoDB service..."
sudo systemctl start mongod 2>/dev/null || sudo systemctl start mongodb 2>/dev/null || true
sudo systemctl enable mongod 2>/dev/null || sudo systemctl enable mongodb 2>/dev/null || true

# Wait for MongoDB to start
sleep 3

# Test MongoDB connection
if timeout 5 mongo --eval "db.adminCommand('ping')" &>/dev/null; then
    print_status "MongoDB connection successful"
else
    print_warning "MongoDB connection failed, but continuing..."
fi
echo ""

# Step 4: Fix loading issues
print_info "Step 4: Testing database and API connectivity..."

# Create a simple test script
cat > test_connection.py << 'EOF'
import sys
import os
sys.path.append(os.getcwd())

try:
    from config.settings import settings
    from config.database import db_manager
    print("✓ Settings loaded successfully")
    print(f"✓ Database type: {settings.DATABASE_TYPE}")
    print(f"✓ Chatbot port: {settings.CHATBOT_PORT}")
    print(f"✓ OpenAI API key: {'Set' if settings.OPENAI_API_KEY else 'Not set'}")
    
    # Test database connection
    if db_manager.mongo_db is not None:
        db_manager.mongo_db.admin.command('ping')
        print("✓ MongoDB connection successful")
    else:
        print("⚠ MongoDB connection failed")
        
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
EOF

python3 test_connection.py
rm test_connection.py
echo ""

# Step 5: Setup background service
print_info "Step 5: Setting up background service..."

# Stop any existing services
python3 service_manager.py stop 2>/dev/null || true

print_status "Background service configured"
echo ""

# Step 6: Start the service
print_info "Step 6: Starting AI Automation Agent..."

# Start in background
python3 service_manager.py start

echo ""
echo "=================================================="
print_status "SETUP COMPLETE!"
echo "=================================================="
echo ""
print_info "Service Status:"
python3 service_manager.py status
echo ""

print_info "Access Points:"
echo "  🌐 Web Interface: http://localhost:8000"
echo "  📊 Status API: http://localhost:8000/api/status"
echo "  🔍 Health Check: http://localhost:8000/api/health"
echo ""

print_info "Management Commands:"
echo "  python3 service_manager.py status   # Check status"
echo "  python3 service_manager.py logs     # View logs"
echo "  python3 service_manager.py stop     # Stop service"
echo "  python3 service_manager.py restart  # Restart service"
echo ""

print_info "Troubleshooting:"
echo "  If loading issues persist:"
echo "  1. Visit http://localhost:8000/api/health"
echo "  2. Check logs: python3 service_manager.py logs"
echo "  3. Review TROUBLESHOOTING_GUIDE.md"
echo ""

print_warning "Important Notes:"
echo "  • Service runs in background and won't stop when terminal closes"
echo "  • Check /var/log/mongodb/ for MongoDB issues"
echo "  • Browser cache may need clearing if issues persist"
echo ""

print_info "Press Ctrl+C to exit, or visit http://localhost:8000 in your browser"
echo ""

# Keep the script running so user can see output
read -p "Press Enter to continue to background, or Ctrl+C to exit..."

print_status "Script completed. Service is running in background."
print_info "Use 'python3 service_manager.py status' to check status anytime."