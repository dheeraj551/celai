#!/bin/bash

# VPS Post-Upload Setup Commands
# Run these commands on your VPS after uploading the files

echo "Setting up AI Automation Agent on VPS..."

# 1. Navigate to project directory
cd /root/ai-automation-agent

# 2. Make scripts executable
chmod +x service_manager.py start_background_service.py complete_setup.sh

# 3. Install/update dependencies
pip install fastapi uvicorn pymongo loguru python-dotenv jinja2 python-multipart requests --upgrade

# 4. Check MongoDB is running
sudo systemctl status mongod
sudo systemctl start mongod

# 5. Start background service
python service_manager.py start

# 6. Verify it's working
python service_manager.py status

# 7. Test the web interface
echo "Testing web interface..."
sleep 3
curl -s http://localhost:8000/api/health | head -5

echo ""
echo "✅ Setup complete!"
echo "🌐 Access your web interface at: http://YOUR_VPS_IP:8000"
echo "📊 Status check: http://YOUR_VPS_IP:8000/api/status"
echo "🔍 Health check: http://YOUR_VPS_IP:8000/api/health"
echo ""
echo "Management commands:"
echo "  python service_manager.py status   # Check status"
echo "  python service_manager.py stop     # Stop service"
echo "  python service_manager.py restart  # Restart service"
echo "  python service_manager.py logs     # View logs"