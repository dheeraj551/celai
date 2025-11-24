#!/bin/bash

# AI Automation Agent - VPS Deployment Script
# This script deploys the application from GitHub

echo "🚀 Starting AI Automation Agent deployment..."

# Navigate to home directory
cd ~

# Pull latest code from GitHub (UPDATE THIS URL)
echo "📥 Pulling latest code from GitHub..."
git pull https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git main

# Create deployment structure
echo "📁 Creating deployment structure..."
mkdir -p ai-automation-agent/AI_Automation_Agent/logs

# Move files to correct location
echo "🔧 Organizing files..."
if [ -f "complete_blog_automation_app.py" ]; then
    mv complete_blog_automation_app.py ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved main application"
fi

if [ -f "ai-automation-agent.service" ]; then
    mv ai-automation-agent.service ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved service file"
fi

if [ -f "requirements.txt" ]; then
    mv requirements.txt ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved requirements"
fi

if [ -f "deploy_to_vps.sh" ]; then
    mv deploy_to_vps.sh ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved deployment script"
fi

if [ -f "health_check.sh" ]; then
    mv health_check.sh ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved health check script"
fi

if [ -f "VPS_DEPLOYMENT_GUIDE.md" ]; then
    mv VPS_DEPLOYMENT_GUIDE.md ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved deployment guide"
fi

# Set permissions
chmod +x ai-automation-agent/AI_Automation_Agent/*.sh

# Navigate to app directory
cd ai-automation-agent/AI_Automation_Agent

# Run deployment
echo "⚡ Running automated deployment..."
./deploy_to_vps.sh

echo "🎉 Deployment complete!"
echo "🔗 Access dashboard at: http://YOUR_VPS_IP:8000"