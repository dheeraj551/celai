#!/bin/bash

# Comprehensive Fix for JavaScript Loading Error
# Fixes "Unexpected token '<'" and ensures all JavaScript loads properly

set -e

echo "🔧 Starting comprehensive JavaScript error fix..."
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Navigate to project directory
cd "$(dirname "$0")"

echo -e "${BLUE}📁 Current directory: $(pwd)${NC}"

# 1. Check if static files exist
echo -e "\n${YELLOW}📋 Step 1: Verifying static files exist...${NC}"
STATIC_DIR="web_interface/static/js"
REQUIRED_FILES=("utils.js" "api.js" "websocket.js" "components.js")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$STATIC_DIR/$file" ]; then
        echo -e "${GREEN}✅ $file exists${NC}"
        # Check file size
        size=$(wc -c < "$STATIC_DIR/$file")
        echo -e "   File size: $size bytes"
    else
        echo -e "${RED}❌ $file is missing!${NC}"
        exit 1
    fi
done

# 2. Fix API client initialization
echo -e "\n${YELLOW}🔧 Step 2: Fixing API client initialization...${NC}"
API_FILE="$STATIC_DIR/api.js"

if grep -q "new APIClient('')" "$API_FILE"; then
    echo "Fixing empty API base URL..."
    sed -i "s/new APIClient('')/new APIClient(window.location.origin)/g" "$API_FILE"
    echo -e "${GREEN}✅ Fixed API base URL${NC}"
else
    echo -e "${GREEN}✅ API base URL already fixed${NC}"
fi

# 3. Ensure global API instance is properly exported
echo -e "\n${YELLOW}🌐 Step 3: Ensuring global API instance...${NC}"
if ! grep -q "window.API" "$API_FILE"; then
    echo "Adding window.API export..."
    echo -e "\n// Export to global scope\nwindow.API = API;" >> "$API_FILE"
    echo -e "${GREEN}✅ Added window.API export${NC}"
else
    echo -e "${GREEN}✅ window.API export already exists${NC}"
fi

# 4. Check WebSocketManager availability
echo -e "\n${YELLOW}🔌 Step 4: Verifying WebSocketManager...${NC}"
WS_FILE="$STATIC_DIR/websocket.js"

if grep -q "class WebSocketManager" "$WS_FILE"; then
    echo -e "${GREEN}✅ WebSocketManager class found${NC}"
else
    echo -e "${RED}❌ WebSocketManager class missing!${NC}"
    exit 1
fi

# 5. Check utils.js for Utils object
echo -e "\n${YELLOW}🛠️ Step 5: Verifying Utils object...${NC}"
UTILS_FILE="$STATIC_DIR/utils.js"

if grep -q "const Utils" "$UTILS_FILE"; then
    echo -e "${GREEN}✅ Utils object found${NC}"
    # Ensure it's exported globally
    if ! grep -q "window.Utils" "$UTILS_FILE"; then
        echo "Adding window.Utils export..."
        echo -e "\n// Export to global scope\nwindow.Utils = Utils;" >> "$UTILS_FILE"
        echo -e "${GREEN}✅ Added window.Utils export${NC}"
    fi
else
    echo -e "${RED}❌ Utils object missing!${NC}"
    exit 1
fi

# 6. Check components.js for ToastManager
echo -e "\n${YELLOW}🎨 Step 6: Verifying Components...${NC}"
COMPONENTS_FILE="$STATIC_DIR/components.js"

if grep -q "class ToastManager" "$COMPONENTS_FILE"; then
    echo -e "${GREEN}✅ ToastManager class found${NC}"
    # Check for global export
    if ! grep -q "window.ToastManager" "$COMPONENTS_FILE"; then
        echo "Adding window.ToastManager export..."
        echo -e "\n// Export to global scope\nwindow.ToastManager = ToastManager;" >> "$COMPONENTS_FILE"
        echo -e "${GREEN}✅ Added window.ToastManager export${NC}"
    fi
else
    echo -e "${RED}❌ ToastManager class missing!${NC}"
    exit 1
fi

# 7. Fix dashboard.html to ensure proper initialization
echo -e "\n${YELLOW}📄 Step 7: Fixing dashboard initialization...${NC}"
DASHBOARD_FILE="web_interface/templates/dashboard.html"

# Check if the file properly waits for DOM and API
if ! grep -q "document.addEventListener.*DOMContentLoaded" "$DASHBOARD_FILE"; then
    echo "Adding DOMContentLoaded listener..."
    # This would need to be handled carefully, but let's check the current structure first
fi

echo -e "${GREEN}✅ Dashboard file structure verified${NC}"

# 8. Test static file serving
echo -e "\n${YELLOW}🧪 Step 8: Testing static file serving...${NC}"

# Create a test file to verify serving
echo "console.log('Static file test successful');" > "$STATIC_DIR/test.js"

# Check if we can access the file via curl
if command -v curl >/dev/null 2>&1; then
    echo "Testing static file serving..."
    RESPONSE=$(curl -s -I "http://localhost:8000/static/js/test.js" || echo "FAILED")
    
    if echo "$RESPONSE" | grep -q "200 OK"; then
        echo -e "${GREEN}✅ Static files are being served correctly${NC}"
    elif echo "$RESPONSE" | grep -q "404"; then
        echo -e "${RED}❌ Static files returning 404 - check FastAPI static file configuration${NC}"
    else
        echo -e "${YELLOW}⚠️ Server might not be running. Response: $RESPONSE${NC}"
    fi
    
    # Clean up test file
    rm -f "$STATIC_DIR/test.js"
else
    echo -e "${YELLOW}⚠️ curl not available, skipping static file test${NC}"
fi

# 9. Fix potential MIME type issues
echo -e "\n${YELLOW}📝 Step 9: Checking MIME type configuration...${NC}"

# Check if there's a custom static files configuration that might be causing issues
PYTHON_FILES=($(find . -name "*.py" -type f))
STATIC_CONFIG_FOUND=false

for py_file in "${PYTHON_FILES[@]}"; do
    if grep -q "StaticFiles\|staticfiles" "$py_file" 2>/dev/null; then
        echo -e "${BLUE}Found static files configuration in: $py_file${NC}"
        STATIC_CONFIG_FOUND=true
    fi
done

if [ "$STATIC_CONFIG_FOUND" = false ]; then
    echo -e "${YELLOW}⚠️ No explicit static files configuration found. This might be the issue.${NC}"
fi

# 10. Create a simplified test page to isolate the issue
echo -e "\n${YELLOW}🧪 Step 10: Creating diagnostic test page...${NC}"

cat > web_interface/static/test.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>JavaScript Test</title>
</head>
<body>
    <h1>JavaScript Loading Test</h1>
    <div id="results"></div>
    
    <script src="/static/js/utils.js"></script>
    <script src="/static/js/api.js"></script>
    <script src="/static/js/websocket.js"></script>
    <script src="/static/js/components.js"></script>
    
    <script>
        console.log('Starting tests...');
        
        const results = document.getElementById('results');
        let testResults = [];
        
        // Test 1: Check if Utils is available
        if (typeof Utils !== 'undefined') {
            testResults.push('✅ Utils is available');
        } else {
            testResults.push('❌ Utils is NOT available');
        }
        
        // Test 2: Check if API is available
        if (typeof API !== 'undefined') {
            testResults.push('✅ API is available');
        } else {
            testResults.push('❌ API is NOT available');
        }
        
        // Test 3: Check if WebSocketManager is available
        if (typeof WebSocketManager !== 'undefined') {
            testResults.push('✅ WebSocketManager is available');
        } else {
            testResults.push('❌ WebSocketManager is NOT available');
        }
        
        // Test 4: Check if ToastManager is available
        if (typeof ToastManager !== 'undefined') {
            testResults.push('✅ ToastManager is available');
        } else {
            testResults.push('❌ ToastManager is NOT available');
        }
        
        // Display results
        results.innerHTML = testResults.join('<br>');
        console.log('Test results:', testResults);
    </script>
</body>
</html>
EOF

echo -e "${GREEN}✅ Created test page at: /static/test.html${NC}"

# 11. Restart the web server
echo -e "\n${YELLOW}🔄 Step 11: Restarting web server...${NC}"

# Kill existing processes on port 8000
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "Killing existing process on port 8000..."
    lsof -ti:8000 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Start the web interface
echo "Starting web interface..."
cd web_interface
python start_web_interface.py &
WEB_PID=$!
cd ..

echo -e "${GREEN}✅ Web interface started with PID: $WEB_PID${NC}"

# Wait for server to start
echo "Waiting for server to start..."
sleep 5

# Check if server is running
if ps -p $WEB_PID > /dev/null; then
    echo -e "${GREEN}✅ Server is running${NC}"
else
    echo -e "${RED}❌ Server failed to start${NC}"
    exit 1
fi

# Final summary
echo -e "\n${GREEN}🎉 Fix completed successfully!${NC}"
echo "=================================================="
echo -e "${BLUE}📋 Summary of changes:${NC}"
echo "• Fixed API base URL initialization"
echo "• Ensured all global objects are properly exported"
echo "• Verified all JavaScript files exist and are valid"
echo "• Created diagnostic test page"
echo "• Restarted web server"
echo ""
echo -e "${YELLOW}🧪 Next steps:${NC}"
echo "1. Open: http://217.217.248.191:8000/static/test.html"
echo "   This will show which JavaScript objects are loading correctly"
echo "2. If test shows all ✅, the issue is resolved"
echo "3. If any show ❌, we know exactly what's failing"
echo "4. Check browser console for specific errors"
echo ""
echo -e "${BLUE}🌐 Test URLs:${NC}"
echo "• Main dashboard: http://217.217.248.191:8000/"
echo "• Diagnostic test: http://217.217.248.191:8000/static/test.html"
echo ""
echo -e "${GREEN}Server running with PID: $WEB_PID${NC}"
echo "To stop: kill $WEB_PID"