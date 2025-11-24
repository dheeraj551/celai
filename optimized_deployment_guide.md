# Complete Deployment Guide - AI Automation Agent with CelorisDesigns.com Integration

## Deployment Instructions for VPS (217.217.248.191)

### Prerequisites (Already Completed)
- ✅ Python dependencies installed: fastapi, uvicorn, websockets, requests, psutil, loguru, python-dotenv, aiofiles
- ✅ Git repository pulled and updated

### Step-by-Step Deployment

#### Step 1: Create Systemd Service File
```bash
sudo cp ai-automation-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable ai-automation-agent
```

#### Step 2: Install the Optimized Application
```bash
cd /root/ai-automation-agent/AI_Automation_Agent

# Backup existing file
cp complete_blog_automation_app.py complete_blog_automation_app.py.backup

# Create the new optimized file
cat > complete_blog_automation_app.py << 'EOF'
[INSERT COMPLETE APPLICATION CODE HERE - 1265 LINES]
EOF
```

#### Step 3: Start the Service
```bash
sudo systemctl start ai-automation-agent
sudo systemctl status ai-automation-agent
```

#### Step 4: Verify Service is Running
```bash
# Check if service is active
sudo systemctl is-active ai-automation-agent

# View logs to ensure no errors
sudo journalctl -u ai-automation-agent -f --since "5 minutes ago"

# Check if port 8000 is listening
netstat -tlnp | grep :8000
```

## Testing the Deployment

### Test 1: Dashboard Access
Open your browser and navigate to:
```
http://217.217.248.191:8000
```

### Test 2: API Endpoints
```bash
# Test VPS monitoring
curl http://217.217.248.191:8000/api/system/resources

# Test blog endpoints
curl http://217.217.248.191:8000/api/blog/posts
```

### Test 3: Blog Generation with CelorisDesigns.com Integration

#### Option A: Web Interface Test
1. Go to http://217.217.248.191:8000
2. Scroll to "AI Blog Generator" section
3. Enter a test topic like "React Development" or "AI Technology"
4. Click "Generate Blog"
5. Monitor the results

#### Option B: Direct API Test
```bash
curl -X POST http://217.217.248.191:8000/api/blog/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "React Development", "length": "medium"}'
```

#### Option C: WebSocket Test (Advanced)
1. Open browser developer tools (F12)
2. Go to Console tab
3. Enter the WebSocket testing code to connect and generate blogs

### Test 4: Verify CelorisDesigns.com Publishing

#### Expected Behavior:
1. **Blog Generation**: AI generates blog content with proper title, content, and metadata
2. **Category Detection**: Automatically detects category (AI, Web Development, Technology, etc.)
3. **Publishing**: Automatically publishes to https://celorisdesigns.com/api/admin/blog
4. **Format Matching**: Uses exact admin interface format:
   - Author: "@MiniMax Agent"
   - Read time: "X min" format
   - Date: "Nov 24, 2025, 1:00 PM" format
   - Status: "published" or "draft"

#### Success Indicators:
- ✅ Dashboard shows "Blog generated and published to celorisdesigns.com!"
- ✅ VPS system monitoring displays real-time metrics
- ✅ Blog appears in your dashboard with "celorisdesigns.com" status
- ✅ Check https://celorisdesigns.com/api/admin/blog to verify new posts

#### Failure Indicators:
- ❌ "Blog generated but failed to publish to celorisdesigns.com: [error]"
- ❌ Authentication errors (check admin session)
- ❌ Connection timeouts (check celorisdesigns.com API availability)

## Troubleshooting

### If Service Won't Start:
```bash
# Check service status and errors
sudo systemctl status ai-automation-agent
sudo journalctl -u ai-automation-agent --no-pager

# Restart service
sudo systemctl restart ai-automation-agent

# Check Python syntax
python3 -m py_compile complete_blog_automation_app.py
```

### If CelorisDesigns.com Publishing Fails:
```bash
# Test API connectivity
curl -X POST https://celorisdesigns.com/api/admin/blog \
  -H "Content-Type: application/json" \
  -H "x-admin-session: {\"id\":\"550e8400-e29b-41d4-a716-446655440000\",\"email\":\"support@celorisdesigns.com\",\"role\":\"admin\"}" \
  -d '{"title":"Test","content":"Test content"}'
```

### If Dashboard Not Loading:
```bash
# Check if uvicorn is running on port 8000
ps aux | grep uvicorn
sudo netstat -tlnp | grep :8000

# Check firewall
sudo ufw status
sudo iptables -L | grep :8000
```

## Next Steps After Successful Deployment

1. **Monitor Service**: Use `sudo systemctl status ai-automation-agent` regularly
2. **View Logs**: `sudo journalctl -u ai-automation-agent -f` for real-time monitoring
3. **Generate Test Blogs**: Test with different topics to verify category detection
4. **Check CelorisDesigns.com**: Confirm blogs appear in the admin interface
5. **Monitor VPS Resources**: Use the dashboard to track system performance

## Environment Variables
Ensure these are set in your environment:
```bash
export NEXTJS_ADMIN_SESSION='{"id":"550e8400-e29b-41d4-a716-446655440000","email":"support@celorisdesigns.com","role":"admin"}'
export NEXTJS_BLOG_API='https://celorisdesigns.com/api/admin/blog'
export NEXTJS_AUTH_HEADER='x-admin-session'
```

## Service Management Commands
```bash
# Start service
sudo systemctl start ai-automation-agent

# Stop service
sudo systemctl stop ai-automation-agent

# Restart service
sudo systemctl restart ai-automation-agent

# View logs
sudo journalctl -u ai-automation-agent -f

# Check service status
sudo systemctl status ai-automation-agent
```