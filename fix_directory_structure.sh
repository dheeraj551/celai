#!/bin/bash
echo "🔧 Fixing directory structure..."

# Create the correct structure
mkdir -p ~/ai-automation-agent/AI_Automation_Agent/logs

# Move files to correct location
cd ~

# Check current location and move files
if [ -f "complete_blog_automation_app.py" ]; then
    mv complete_blog_automation_app.py ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved main app file"
fi

if [ -f "ai-automation-agent.service" ]; then
    mv ai-automation-agent.service ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved service file"
fi

if [ -f "requirements.txt" ]; then
    mv requirements.txt ai-automation-agent/AI_Automation_Agent/
    echo "✅ Moved requirements file"
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
chmod +x ai-automation-agent/AI_Automation_Agent/deploy_to_vps.sh
chmod +x ai-automation-agent/AI_Automation_Agent/health_check.sh

echo "🎯 Directory structure fixed!"
echo "📁 Files are now in: ~/ai-automation-agent/AI_Automation_Agent/"

# Run deployment
echo "🚀 Running deployment..."
cd ai-automation-agent/AI_Automation_Agent
./deploy_to_vps.sh
