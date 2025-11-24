#!/bin/bash

# AI Automation Agent - Deployment Organization Script
# This script organizes all deployment files into the correct structure

echo "🚀 Organizing AI Automation Agent deployment files..."

# Create necessary directories
mkdir -p AI_Automation_Agent/logs
mkdir -p AI_Automation_Agent/config

# Check if we need to copy files from workspace root
if [ -f "complete_blog_automation_app.py" ]; then
    echo "📁 Copying main application file..."
    cp complete_blog_automation_app.py AI_Automation_Agent/
fi

if [ -f "requirements.txt" ]; then
    echo "📋 Copying requirements file..."
    cp requirements.txt AI_Automation_Agent/
fi

if [ -f "deploy_to_vps.sh" ]; then
    echo "🔧 Copying deployment script..."
    cp deploy_to_vps.sh AI_Automation_Agent/
fi

if [ -f "health_check.sh" ]; then
    echo "🔍 Copying health check script..."
    cp health_check.sh AI_Automation_Agent/
fi

if [ -f "VPS_DEPLOYMENT_GUIDE.md" ]; then
    echo "📚 Copying deployment guide..."
    cp VPS_DEPLOYMENT_GUIDE.md AI_Automation_Agent/
fi

# Set execute permissions
chmod +x AI_Automation_Agent/deploy_to_vps.sh
chmod +x AI_Automation_Agent/health_check.sh

echo "✅ File organization complete!"
echo ""
echo "📊 Directory structure:"
echo "ai-automation-agent/"
echo "├── AI_Automation_Agent/"
echo "│   ├── complete_blog_automation_app.py"
echo "│   ├── ai-automation-agent.service"
echo "│   ├── requirements.txt"
echo "│   ├── deploy_to_vps.sh"
echo "│   ├── health_check.sh"
echo "│   ├── VPS_DEPLOYMENT_GUIDE.md"
echo "│   └── logs/"
echo ""
echo "🎯 Ready for git deployment!"