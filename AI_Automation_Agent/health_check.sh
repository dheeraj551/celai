#!/bin/bash

# AI Automation Agent - Health Check Script
# Run this script to verify your deployment is working correctly

echo "🔍 AI Automation Agent - Health Check"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_passed() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
}

check_failed() {
    echo -e "${RED}❌ FAIL:${NC} $1"
}

check_warning() {
    echo -e "${YELLOW}⚠️  WARN:${NC} $1"
}

# Test 1: Check if service is running
echo "Test 1: Checking systemd service..."
if systemctl is-active --quiet ai-automation-agent; then
    check_passed "Service is running"
else
    check_failed "Service is not running"
    echo "   Try: sudo systemctl start ai-automation-agent"
fi
echo ""

# Test 2: Check if port 8000 is listening
echo "Test 2: Checking port 8000..."
if netstat -tuln | grep -q ":8000"; then
    check_passed "Port 8000 is listening"
else
    check_failed "Port 8000 is not listening"
    echo "   Service may not be started properly"
fi
echo ""

# Test 3: Check HTTP response
echo "Test 3: Testing HTTP endpoint..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000 | grep -q "200"; then
    check_passed "Dashboard is accessible (HTTP 200)"
else
    check_failed "Dashboard is not accessible"
    echo "   Try: curl http://localhost:8000"
fi
echo ""

# Test 4: Check API endpoints
echo "Test 4: Testing API endpoints..."

# Test system resources endpoint
if curl -s http://localhost:8000/api/system/resources > /dev/null; then
    check_passed "System resources API works"
else
    check_warning "System resources API may not be responding"
fi

# Test blog posts endpoint
if curl -s http://localhost:8000/api/blog/posts > /dev/null; then
    check_passed "Blog posts API works"
else
    check_warning "Blog posts API may not be responding"
fi
echo ""

# Test 5: Check logs for errors
echo "Test 5: Checking recent logs for errors..."
ERROR_COUNT=$(journalctl -u ai-automation-agent --since "5 minutes ago" | grep -i error | wc -l)
if [ "$ERROR_COUNT" -eq 0 ]; then
    check_passed "No errors in recent logs"
else
    check_warning "Found $ERROR_COUNT error(s) in recent logs"
    echo "   Check: sudo journalctl -u ai-automation-agent --since '5 minutes ago'"
fi
echo ""

# Test 6: Check disk space
echo "Test 6: Checking disk space..."
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    check_passed "Disk usage is healthy (${DISK_USAGE}%)"
else
    check_warning "Disk usage is high (${DISK_USAGE}%)"
fi
echo ""

# Test 7: Check memory usage
echo "Test 7: Checking memory usage..."
MEM_USAGE=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
if (( $(echo "$MEM_USAGE < 90" | bc -l) )); then
    check_passed "Memory usage is healthy (${MEM_USAGE}%)"
else
    check_warning "Memory usage is high (${MEM_USAGE}%)"
fi
echo ""

# Test 8: Test celorisdesigns.com connectivity (if possible)
echo "Test 8: Testing celorisdesigns.com API connectivity..."
if curl -s --max-time 5 https://celorisdesigns.com/api/admin/blog > /dev/null 2>&1; then
    check_passed "celorisdesigns.com API is reachable"
else
    check_warning "celorisdesigns.com API may not be reachable"
    echo "   This might affect blog publishing"
fi
echo ""

# Summary
echo "========================================="
echo "📊 Health Check Summary"
echo "========================================="
echo ""

# Service status
if systemctl is-active --quiet ai-automation-agent; then
    echo "🌐 Dashboard: http://217.217.248.191:8000"
else
    echo "❌ Service not running"
fi

echo ""
echo "🔧 Useful Commands:"
echo "  • Check status: sudo systemctl status ai-automation-agent"
echo "  • View logs: sudo journalctl -u ai-automation-agent -f"
echo "  • Restart: sudo systemctl restart ai-automation-agent"
echo "  • Test API: curl http://localhost:8000/api/system/resources"
echo ""

echo "🧪 Quick Test:"
echo "  1. Open http://217.217.248.191:8000 in your browser"
echo "  2. Enter a blog topic and click 'Generate Blog'"
echo "  3. Check if it publishes to celorisdesigns.com"
echo ""

# Performance metrics
echo "💻 VPS Performance:"
echo "  • CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')% usage"
echo "  • Memory: $MEM_USAGE% used"
echo "  • Disk: $DISK_USAGE% used"
echo ""

if systemctl is-active --quiet ai-automation-agent && netstat -tuln | grep -q ":8000"; then
    echo -e "${GREEN}🎉 Overall Status: HEALTHY${NC}"
    echo "Your AI Automation Agent is running correctly!"
else
    echo -e "${RED}⚠️  Overall Status: NEEDS ATTENTION${NC}"
    echo "Some issues detected. Check the warnings above."
fi

echo ""
echo "For detailed troubleshooting, see VPS_DEPLOYMENT_GUIDE.md"
