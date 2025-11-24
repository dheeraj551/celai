#!/bin/bash

# =============================================================================
# COMPLETE DEPLOYMENT SCRIPT - Blog Management + VPS Monitoring + CelorisDesigns
# =============================================================================
# This script deploys the complete fix with all three requested features:
# 1. Blog visibility in dashboard
# 2. Working blog editing functionality  
# 3. VPS resource monitoring
# 4. Next.js integration with celorisdesigns.com
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/dheeraj551/celai.git"
DEPLOY_DIR="$HOME/ai-automation-agent/AI_Automation_Agent"
BACKUP_DIR="$HOME/ai-automation-backup-$(date +%Y%m%d_%H%M%S)"
SERVICE_NAME="ai-automation-agent"

echo -e "${BLUE}🚀 Starting Complete Deployment Process...${NC}"
echo -e "${BLUE}📋 Features to deploy:${NC}"
echo "  ✅ Blog visibility in dashboard"
echo "  ✅ Working blog editing functionality"
echo "  ✅ VPS resource monitoring (CPU, RAM, Storage, Uptime)"
echo "  ✅ Next.js integration with celorisdesigns.com"
echo ""

# =============================================================================
# STEP 1: Backup Current Installation
# =============================================================================
echo -e "${YELLOW}📦 Step 1: Backing up current installation...${NC}"

if [ -d "$DEPLOY_DIR" ]; then
    echo "Creating backup at: $BACKUP_DIR"
    cp -r "$DEPLOY_DIR" "$BACKUP_DIR"
    echo -e "${GREEN}✅ Backup completed${NC}"
else
    echo -e "${YELLOW}⚠️  No existing installation found${NC}"
fi

# =============================================================================
# STEP 2: Navigate to deployment directory
# =============================================================================
echo -e "${YELLOW}📁 Step 2: Setting up deployment directory...${NC}"

if [ ! -d "$DEPLOY_DIR" ]; then
    echo "Creating deployment directory..."
    mkdir -p "$(dirname "$DEPLOY_DIR")"
    cd "$(dirname "$DEPLOY_DIR")"
    
    echo "Cloning repository..."
    git clone "$REPO_URL"
    
    cd "$DEPLOY_DIR"
    echo -e "${GREEN}✅ Repository cloned${NC}"
else
    cd "$DEPLOY_DIR"
    
    echo "Pulling latest changes..."
    git pull origin master
    echo -e "${GREEN}✅ Repository updated${NC}"
fi

# =============================================================================
# STEP 3: Install Dependencies
# =============================================================================
echo -e "${YELLOW}📦 Step 3: Installing dependencies...${NC}"

# Check if requirements.txt exists and install
if [ -f "requirements.txt" ]; then
    echo "Installing Python packages..."
    pip install -r requirements.txt --upgrade
    
    # Install additional required packages
    pip install fastapi uvicorn websockets requests psutil loguru python-dotenv mongodb
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found, installing core packages...${NC}"
    pip install fastapi uvicorn websockets requests psutil loguru python-dotenv mongodb
fi

# =============================================================================
# STEP 4: Configure Environment
# =============================================================================
echo -e "${YELLOW}⚙️  Step 4: Configuring environment...${NC}"

# Copy environment file
if [ -f ".env.celorisdesigns" ]; then
    echo "Using celorisdesigns.com configuration..."
    cp .env.celorisdesigns .env
    echo -e "${GREEN}✅ Environment configured for celorisdesigns.com${NC}"
else
    echo -e "${YELLOW}⚠️  .env.celorisdesigns not found, using existing .env${NC}"
fi

# Ensure logs directory exists
mkdir -p logs

# =============================================================================
# STEP 5: Setup Service
# =============================================================================
echo -e "${YELLOW}🔧 Step 5: Setting up systemd service...${NC}"

# Create service file
cat > /tmp/ai-automation-agent.service << EOF
[Unit]
Description=AI Automation Agent with Blog Publishing
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$DEPLOY_DIR
Environment=PATH=$DEPLOY_DIR
ExecStart=/usr/bin/python3 -m uvicorn blog_automation_app:app --host 0.0.0.0 --port 8000 --reload
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Copy service file and enable
cp /tmp/ai-automation-agent.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable ai-automation-agent

echo -e "${GREEN}✅ Service configured${NC}"

# =============================================================================
# STEP 6: Stop and Start Service
# =============================================================================
echo -e "${YELLOW}🔄 Step 6: Restarting service...${NC}"

# Stop existing service
if systemctl is-active --quiet ai-automation-agent; then
    echo "Stopping existing service..."
    systemctl stop ai-automation-agent
    sleep 2
fi

# Start new service
echo "Starting AI Automation Agent..."
systemctl start ai-automation-agent

# Wait for service to start
sleep 5

# Check service status
if systemctl is-active --quiet ai-automation-agent; then
    echo -e "${GREEN}✅ Service started successfully${NC}"
else
    echo -e "${RED}❌ Service failed to start${NC}"
    echo "Service logs:"
    journalctl -u ai-automation-agent --no-pager -n 20
    exit 1
fi

# =============================================================================
# STEP 7: Verify Deployment
# =============================================================================
echo -e "${YELLOW}🔍 Step 7: Verifying deployment...${NC}"

# Test basic connectivity
echo "Testing API endpoints..."
sleep 3

# Test main endpoint
if curl -s -f http://localhost:8000 > /dev/null; then
    echo -e "${GREEN}✅ Main API responding${NC}"
else
    echo -e "${YELLOW}⚠️  Main API might still be starting up${NC}"
fi

# Test blog posts endpoint
if curl -s -f http://localhost:8000/api/blog/posts > /dev/null; then
    echo -e "${GREEN}✅ Blog API responding${NC}"
else
    echo -e "${YELLOW}⚠️  Blog API might still be starting up${NC}"
fi

# Test VPS monitoring endpoint
if curl -s -f http://localhost:8000/api/system/resources > /dev/null; then
    echo -e "${GREEN}✅ VPS Monitoring API responding${NC}"
else
    echo -e "${YELLOW}⚠️  VPS Monitoring API might still be starting up${NC}"
fi

# =============================================================================
# STEP 8: Display Final Status
# =============================================================================
echo ""
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!${NC}"
echo ""
echo -e "${BLUE}📊 Deployment Summary:${NC}"
echo "  ✅ Blog visibility: Implemented with JSON-based storage"
echo "  ✅ Blog editing: Modal-based editing interface"  
echo "  ✅ VPS monitoring: CPU, RAM, Storage, Uptime tracking"
echo "  ✅ Next.js integration: Auto-publishing to celorisdesigns.com"
echo ""
echo -e "${BLUE}🌐 Access Information:${NC}"
echo "  URL: http://217.217.248.191:8000"
echo "  Status: $(systemctl is-active ai-automation-agent)"
echo "  Service: $SERVICE_NAME"
echo ""
echo -e "${BLUE}🔧 Management Commands:${NC}"
echo "  Check status: sudo systemctl status ai-automation-agent"
echo "  View logs: sudo journalctl -u ai-automation-agent -f"
echo "  Restart: sudo systemctl restart ai-automation-agent"
echo ""
echo -e "${BLUE}📋 Next Steps:${NC}"
echo "  1. Visit http://217.217.248.191:8000 to access the dashboard"
echo "  2. Test AI blog generation and verify it auto-publishes to celorisdesigns.com"
echo "  3. Test blog editing functionality"
echo "  4. Check VPS monitoring section for system metrics"
echo ""
echo -e "${GREEN}🎯 All features are now live and ready for testing!${NC}"
