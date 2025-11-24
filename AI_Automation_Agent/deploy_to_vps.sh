#!/bin/bash

# AI Automation Agent Deployment Script for VPS
# This script automates the deployment of the AI Automation Agent to your VPS
# Run this script after pulling the latest code from GitHub

set -e

echo "🚀 AI Automation Agent - VPS Deployment Script"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Step 1: Check if running as root
print_info "Step 1: Checking permissions..."
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root (use sudo)"
   exit 1
fi
print_status "Running as root"
echo ""

# Step 2: Check current directory
print_info "Step 2: Checking deployment directory..."
CURRENT_DIR=$(pwd)
EXPECTED_DIR="/root/ai-automation-agent/AI_Automation_Agent"

if [[ "$CURRENT_DIR" != "$EXPECTED_DIR" ]]; then
    print_warning "Current directory: $CURRENT_DIR"
    print_warning "Expected directory: $EXPECTED_DIR"
    print_info "Changing to deployment directory..."
    cd "$EXPECTED_DIR"
fi
print_status "In deployment directory: $(pwd)"
echo ""

# Step 3: Install Python dependencies
print_info "Step 3: Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
    print_status "Dependencies installed successfully"
else
    print_error "pip3 not found. Installing..."
    apt update && apt install -y python3-pip
    pip3 install -r requirements.txt
    print_status "pip3 installed and dependencies added"
fi
echo ""

# Step 4: Create logs directory
print_info "Step 4: Creating logs directory..."
mkdir -p logs
print_status "Logs directory created"
echo ""

# Step 5: Backup existing application
print_info "Step 5: Backing up existing application..."
if [[ -f "complete_blog_automation_app.py" ]]; then
    BACKUP_FILE="complete_blog_automation_app.py.backup.$(date +%Y%m%d_%H%M%S)"
    cp complete_blog_automation_app.py "$BACKUP_FILE"
    print_status "Backed up to $BACKUP_FILE"
else
    print_info "No existing application file found"
fi
echo ""

# Step 6: Install systemd service
print_info "Step 6: Installing systemd service..."
if [[ -f "ai-automation-agent.service" ]]; then
    cp ai-automation-agent.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable ai-automation-agent
    print_status "Systemd service installed and enabled"
else
    print_error "Service file ai-automation-agent.service not found!"
    exit 1
fi
echo ""

# Step 7: Stop existing service if running
print_info "Step 7: Checking existing service..."
if systemctl is-active --quiet ai-automation-agent; then
    print_info "Stopping existing service..."
    systemctl stop ai-automation-agent
    print_status "Existing service stopped"
fi
echo ""

# Step 8: Start the service
print_info "Step 8: Starting AI Automation Agent..."
systemctl start ai-automation-agent
sleep 3

# Check if service started successfully
if systemctl is-active --quiet ai-automation-agent; then
    print_status "✅ AI Automation Agent started successfully!"
else
    print_error "Failed to start service. Checking logs..."
    systemctl status ai-automation-agent
    journalctl -u ai-automation-agent --no-pager -n 20
    exit 1
fi
echo ""

# Step 9: Verify deployment
print_info "Step 9: Verifying deployment..."

# Check if port 8000 is listening
if netstat -tuln | grep -q ":8000"; then
    print_status "Service is listening on port 8000"
else
    print_warning "Port 8000 not listening yet"
fi

# Check if service is healthy
sleep 2
if curl -s http://localhost:8000 > /dev/null; then
    print_status "✅ Dashboard is accessible at http://localhost:8000"
else
    print_warning "Dashboard not responding yet (might still be starting)"
fi
echo ""

# Step 10: Display service information
print_info "Step 10: Service Information"
echo "================================"
echo ""
echo "Service Status:"
systemctl status ai-automation-agent --no-pager -l
echo ""
echo "Recent Logs:"
journalctl -u ai-automation-agent --no-pager -n 10
echo ""

# Final instructions
echo ""
echo -e "${GREEN}🎉 Deployment Complete!${NC}"
echo "================================"
echo ""
echo "🌐 Your AI Automation Agent is now running on:"
echo "   Dashboard: http://217.217.248.191:8000"
echo "   API Base:  http://217.217.248.191:8000/api"
echo ""
echo "📝 Available endpoints:"
echo "   - GET  /                     → Dashboard (HTML)"
echo "   - GET  /api/blog/posts       → List all blogs"
echo "   - POST /api/blog/generate    → Generate new blog"
echo "   - GET  /api/system/resources → VPS monitoring"
echo "   - WS   /ws                   → WebSocket for real-time updates"
echo ""
echo "🛠️  Management Commands:"
echo "   systemctl status ai-automation-agent"
echo "   systemctl restart ai-automation-agent"
echo "   journalctl -u ai-automation-agent -f"
echo ""
echo "🔍 To test blog generation:"
echo "   1. Open http://217.217.248.191:8000 in your browser"
echo "   2. Enter a blog topic (e.g., 'AI Technology')"
echo "   3. Click 'Generate Blog'"
echo "   4. Check celorisdesigns.com admin interface"
echo ""
echo -e "${BLUE}Happy blogging! 🤖✨${NC}"
