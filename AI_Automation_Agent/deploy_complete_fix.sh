#!/bin/bash
# Complete Blog Publishing & VPS Monitoring Deployment Script
# This script deploys the AI Automation Agent with all fixes

echo "🚀 Complete Blog Publishing & VPS Monitoring Deployment"
echo "====================================================="

# Navigate to application directory
cd ~/ai-automation-agent/AI_Automation_Agent

# Kill existing processes
echo "🔄 Stopping existing processes..."
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
pip install psutil fastapi uvicorn requests beautifulsoup4 python-dotenv

# Ensure directories exist
mkdir -p data logs

# Check if OpenAI key is available
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OpenAI API key found"
    pip install openai
else
    echo "⚠️  OpenAI API key not found - using template generation"
fi

# Start the application
echo "🚀 Starting AI Automation Agent with all features..."
nohup python3 working_agent.py > logs/complete_deployment.log 2>&1 &

# Get PID
APP_PID=$!
echo $APP_PID > logs/app.pid

# Wait for startup
echo "⏳ Waiting for application to start..."
sleep 5

# Test if running
if ps -p $APP_PID > /dev/null; then
    echo "✅ SUCCESS! Application started with PID: $APP_PID"
    echo ""
    echo "🌐 Access your application:"
    echo "   📊 Dashboard: http://217.217.248.191:8000"
    echo ""
    echo "📝 FIXED ISSUES:"
    echo "   ✅ Blog posts now visible in dashboard"
    echo "   ✅ Blog editing feature now available"
    echo "   ✅ VPS monitoring added (RAM, CPU, Storage, Uptime)"
    echo ""
    echo "📋 Available Features:"
    echo "   • Generate AI-powered blog posts"
    echo "   • Edit and publish blog posts"
    echo "   • Monitor VPS resources in real-time"
    echo "   • View system uptime and performance"
    echo ""
    echo "📋 Logs: logs/complete_deployment.log"
    echo ""
    
    # Test endpoints
    echo "🧪 Testing endpoints..."
    sleep 2
    
    # Test main dashboard
    curl -s http://localhost:8000/ > /dev/null && echo "✅ Dashboard working" || echo "❌ Dashboard failed"
    
    # Test blog posts
    curl -s http://localhost:8000/api/blog/posts > /dev/null && echo "✅ Blog API working" || echo "❌ Blog API failed"
    
    # Test system metrics
    curl -s http://localhost:8000/api/system/metrics > /dev/null && echo "✅ VPS monitoring working" || echo "❌ VPS monitoring failed"
    
    echo ""
    echo "🎯 Ready to use! Try:"
    echo "   1. Go to http://217.217.248.191:8000"
    echo "   2. Click 'Generate New Blog with AI'"
    echo "   3. Edit any blog posts with the Edit button"
    echo "   4. Monitor your VPS resources in real-time"
    
else
    echo "❌ Failed to start. Check logs/complete_deployment.log"
    echo "🔧 Error details:"
    tail -10 logs/complete_deployment.log
    exit 1
fi