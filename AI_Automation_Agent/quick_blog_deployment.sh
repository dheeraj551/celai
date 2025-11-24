#!/bin/bash
# Quick Blog Deployment Script for VPS
# Run this script on your VPS to deploy blog publishing features

echo "🚀 Quick Blog Publishing Deployment"
echo "=================================="

# Navigate to application directory
cd ~/ai-automation-agent/AI_Automation_Agent

# Kill existing processes
pkill -f "working_agent.py" 2>/dev/null || true
pkill -f "blog_automation_app.py" 2>/dev/null || true

# Ensure virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install fastapi uvicorn openai requests beautifulsoup4 python-dotenv

# Create logs directory
mkdir -p logs

# Start the application
echo "🚀 Starting application..."
nohup python3 working_agent.py > logs/quick_deploy.log 2>&1 &

# Get PID
APP_PID=$!
echo $APP_PID > logs/app.pid

# Wait for startup
sleep 5

# Test if running
if ps -p $APP_PID > /dev/null; then
    echo "✅ SUCCESS! Application started with PID: $APP_PID"
    echo ""
    echo "🌐 Access your application:"
    echo "   📊 Dashboard: http://217.217.248.191:8000"
    echo "   ✍️  Blog Automation: http://217.217.248.191:8000/blog-automation"
    echo ""
    echo "📝 Blog Features Ready:"
    echo "   • Generate AI-powered blog posts"
    echo "   • Create blog series"
    echo "   • Schedule automated blogging"
    echo "   • Publish to multiple platforms"
    echo ""
    echo "📋 Logs: logs/quick_deploy.log"
    echo ""
    
    # Quick test
    echo "🧪 Testing endpoints..."
    sleep 2
    curl -s http://localhost:8000/api/blog/settings > /dev/null && echo "✅ Blog API working" || echo "❌ Blog API failed"
    
else
    echo "❌ Failed to start. Check logs/quick_deploy.log"
    exit 1
fi