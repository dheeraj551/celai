#!/bin/bash
# Quick Fix Script for MySQL Import Error
# Run this on your VPS after uploading the corrected files

echo "=========================================="
echo "🔧 QUICK FIX FOR MYSQL IMPORT ERROR"
echo "=========================================="

echo ""
echo "📋 This script will:"
echo "   1. Install/verify all dependencies"
echo "   2. Test MongoDB connection"
echo "   3. Start the AI Automation Agent"
echo "   4. Verify the web interface is working"
echo ""

# Check if we're in the right directory
if [ ! -f "AI_Automation_Agent/.env.celorisdesigns" ]; then
    echo "❌ Error: Please run this script from the directory containing 'AI_Automation_Agent'"
    exit 1
fi

# Change to the agent directory
cd AI_Automation_Agent

echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "🧪 Testing MongoDB connection..."
python ../test_mongodb_connection.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🚀 Starting AI Automation Agent..."
    python service_manager.py start
    
    echo ""
    echo "⏳ Waiting for service to start..."
    sleep 5
    
    echo ""
    echo "📊 Checking service status..."
    python service_manager.py status
    
    echo ""
    echo "🌐 Testing web interface..."
    sleep 3
    
    # Test if the web interface is responding
    if curl -s http://localhost:8000 > /dev/null; then
        echo "✅ Web interface is responding!"
        echo ""
        echo "🎉 SUCCESS! Your AI Automation Agent is running."
        echo ""
        echo "📝 Access Information:"
        echo "   Web Interface: http://YOUR_VPS_IP:8000"
        echo "   Service Status: python service_manager.py status"
        echo "   Stop Service: python service_manager.py stop"
        echo "   View Logs: python service_manager.py logs"
        echo ""
        echo "🔒 Test permanent operation:"
        echo "   1. Close this terminal"
        echo "   2. Wait 30 seconds"
        echo "   3. Open new terminal and run:"
        echo "      python service_manager.py status"
        echo "   4. Access web interface to confirm it's still working"
    else
        echo "⚠️ Web interface may still be starting..."
        echo "   Please wait a moment and then check:"
        echo "   python service_manager.py status"
    fi
else
    echo ""
    echo "❌ MongoDB connection failed. Please:"
    echo "   1. Install MongoDB: sudo apt update && sudo apt install mongodb"
    echo "   2. Start MongoDB: sudo systemctl start mongodb"
    echo "   3. Enable MongoDB: sudo systemctl enable mongodb"
    echo "   4. Re-run this script"
fi

echo ""
echo "=========================================="