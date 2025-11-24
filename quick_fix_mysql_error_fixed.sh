#!/bin/bash
# Quick Fix Script for MySQL Import Error
# Run this from inside the AI_Automation_Agent directory

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
if [ ! -f ".env.celorisdesigns" ] || [ ! -f "service_manager.py" ]; then
    echo "❌ Error: Please run this script from inside the AI_Automation_Agent directory"
    echo "   Current directory: $(pwd)"
    echo "   This directory should contain:"
    echo "   - .env.celorisdesigns"
    echo "   - service_manager.py"
    echo "   - requirements.txt"
    exit 1
fi

echo "📍 Current directory: $(pwd)"
echo "✅ Found AI_Automation_Agent directory"
echo ""

echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "🧪 Testing MongoDB connection..."
if [ -f "../test_mongodb_connection.py" ]; then
    # If test script is in parent directory
    python ../test_mongodb_connection.py
else
    # Create and run a simple test inline
    python3 -c "
import sys
try:
    from config.settings import settings
    from config.database import init_database
    print('✅ Configuration loaded successfully')
    print(f'Database Type: {settings.DATABASE_TYPE}')
    print(f'MongoDB URI: {settings.MONGODB_URI}')
    
    print('Testing database connection...')
    success = init_database()
    if success:
        print('✅ MongoDB connected successfully!')
    else:
        print('❌ MongoDB connection failed!')
        sys.exit(1)
except ImportError as e:
    print(f'❌ Import error: {e}')
    print('Please ensure all dependencies are installed: pip install -r requirements.txt')
    sys.exit(1)
except Exception as e:
    print(f'❌ Connection error: {e}')
    sys.exit(1)
"
fi

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
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo "✅ Web interface is responding!"
        echo ""
        echo "🎉 SUCCESS! Your AI Automation Agent is running."
        echo ""
        echo "📝 Access Information:"
        echo "   Web Interface: http://$(hostname -I | awk '{print $1}'):8000"
        echo "   Service Status: python service_manager.py status"
        echo "   Stop Service: python service_manager.py stop"
        echo "   View Logs: python service_manager.py logs"
        echo ""
        echo "🔒 Test permanent operation:"
        echo "   1. Close this terminal"
        echo "   2. Wait 30 seconds"
        echo "   3. Open new terminal and run:"
        echo "      cd ~/ai-automation-agent/AI_Automation_Agent"
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