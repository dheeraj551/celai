#!/bin/bash
# Complete Blog Automation Startup Script
# This script starts the AI Automation Agent with full blog publishing capabilities

echo "🚀 Starting AI Automation Agent with Blog Publishing..."

# Navigate to the application directory
cd ~/ai-automation-agent/AI_Automation_Agent

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Kill any existing instances
pkill -f "blog_automation_app.py" 2>/dev/null || true
pkill -f "working_app.py" 2>/dev/null || true
pkill -f "start_web_interface.py" 2>/dev/null || true

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the complete blog automation application
echo "📝 Starting comprehensive blog automation application..."
nohup python blog_automation_app.py > logs/complete_blog_app.log 2>&1 &

# Get the process ID
APP_PID=$!
echo "✅ Application started with PID: $APP_PID"

# Wait a moment for the application to start
sleep 3

# Check if the application is running
if ps -p $APP_PID > /dev/null; then
    echo "🎉 SUCCESS! Your AI Automation Agent with Blog Publishing is now running!"
    echo ""
    echo "🌐 Access your application:"
    echo "   📊 Dashboard: http://217.217.248.191:8000"
    echo "   ✍️  Blog Automation: http://217.217.248.191:8000/blog-automation"
    echo "   📈 Analytics: http://217.217.248.191:8000/analytics"
    echo "   ⚙️  Settings: http://217.217.248.191:8000/settings"
    echo ""
    echo "📝 Blog Publishing Features Available:"
    echo "   • Generate single blog posts with AI"
    echo "   • Create blog series automatically"
    echo "   • Schedule daily blog generation"
    echo "   • Publish to multiple platforms"
    echo "   • View detailed analytics"
    echo "   • Manage all blog posts in one place"
    echo ""
    echo "📋 Log file: logs/complete_blog_app.log"
    echo "🔄 Process ID: $APP_PID"
    
    # Save PID for later management
    echo $APP_PID > logs/app.pid
else
    echo "❌ Failed to start application. Check logs/complete_blog_app.log for details."
    exit 1
fi