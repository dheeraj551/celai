# AI Automation Agent - VPS Deployment Guide

🤖 **Quick deployment guide for your AI automation agent with celorisdesigns.com integration**

## 📋 What You Need

- VPS at: `217.217.248.191`
- Root access
- Git repository with the latest optimized code
- This deployment guide

## 🚀 Deployment Steps

### Step 1: Pull Latest Code from GitHub

```bash
# Connect to your VPS
ssh root@217.217.248.191

# Navigate to your project directory
cd /root/ai-automation-agent/AI_Automation_Agent

# Pull the latest changes
git pull origin main  # or your branch name

# Verify you have the latest files
ls -la
# You should see: complete_blog_automation_app.py, ai-automation-agent.service, requirements.txt, deploy_to_vps.sh
```

### Step 2: Run Automated Deployment

```bash
# Make the deployment script executable
chmod +x deploy_to_vps.sh

# Run the automated deployment
sudo ./deploy_to_vps.sh
```

The script will:
1. ✅ Install Python dependencies
2. ✅ Create necessary directories
3. ✅ Install systemd service
4. ✅ Start the AI automation agent
5. ✅ Verify deployment
6. ✅ Show you the dashboard URL

### Step 3: Access Your Dashboard

Once deployment completes successfully, open your browser:

```
http://217.217.248.191:8000
```

## 🎯 Testing CelorisDesigns.com Integration

### Test Blog Generation

1. **Open the dashboard** at http://217.217.248.191:8000
2. **Scroll to "AI Blog Generator" section**
3. **Enter a test topic**, e.g., "React Development" or "AI Technology"
4. **Click "Generate Blog"**
5. **Watch the real-time progress**
6. **Check the result message**

### Expected Success Message

```
✅ "Blog generated and published to celorisdesigns.com!"
```

### Verify on CelorisDesigns.com

1. **Open** https://celorisdesigns.com/api/admin/blog
2. **Look for your new blog post** with:
   - Title: "AI-Generated: [Topic] - Complete Guide 2025"
   - Author: "@MiniMax Agent"
   - Category: Auto-detected (AI, Web Development, Technology, etc.)
   - Status: "published"
   - Read time: Calculated automatically

### Test Different Categories

Try these topics to test category detection:

| Topic | Expected Category |
|-------|------------------|
| "React Development" | Web Development |
| "AI Technology" | AI |
| "UI Design Tips" | Design |
| "Productivity Automation" | Productivity |
| "Technology Trends" | Technology |

## 🔧 Management Commands

### Check Service Status
```bash
sudo systemctl status ai-automation-agent
```

### View Real-time Logs
```bash
sudo journalctl -u ai-automation-agent -f
```

### Restart Service
```bash
sudo systemctl restart ai-automation-agent
```

### Stop Service
```bash
sudo systemctl stop ai-automation-agent
```

### Start Service
```bash
sudo systemctl start ai-automation-agent
```

## 📊 API Endpoints to Test

### Basic Health Check
```bash
curl http://217.217.248.191:8000/api/system/resources
```

### List Blog Posts
```bash
curl http://217.217.248.191:8000/api/blog/posts
```

### Generate Blog via API
```bash
curl -X POST http://217.217.248.191:8000/api/blog/generate \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Topic", "length": "medium"}'
```

### View System Logs
```bash
curl http://217.217.248.191:8000/api/system/logs
```

## 🔍 Troubleshooting

### Issue: Service Won't Start
```bash
# Check what's wrong
sudo systemctl status ai-automation-agent
sudo journalctl -u ai-automation-agent --no-pager -n 20

# Try restarting
sudo systemctl restart ai-automation-agent
```

### Issue: Port 8000 Not Listening
```bash
# Check if something is using port 8000
sudo netstat -tlnp | grep :8000

# Check firewall
sudo ufw status
```

### Issue: CelorisDesigns.com Publishing Fails
```bash
# Test API connectivity
curl -X POST https://celorisdesigns.com/api/admin/blog \
  -H "Content-Type: application/json" \
  -H "x-admin-session: {\"id\":\"550e8400-e29b-41d4-a716-446655440000\",\"email\":\"support@celorisdesigns.com\",\"role\":\"admin\"}" \
  -d '{"title":"Test","content":"Test content"}'
```

### Issue: Dashboard Not Loading
```bash
# Test locally first
curl http://localhost:8000

# Check if service is running
ps aux | grep uvicorn
```

## 📱 Mobile Testing

The dashboard is fully responsive. Test on:
- 📱 Mobile browser
- 📱 Tablet
- 💻 Desktop

## 🎉 Success Indicators

When everything is working correctly, you should see:

1. ✅ **Dashboard loads** at http://217.217.248.191:8000
2. ✅ **VPS monitoring shows real-time metrics** (CPU, RAM, disk)
3. ✅ **Blog generation works** and shows success message
4. ✅ **Blogs appear in celorisdesigns.com admin interface**
5. ✅ **Category detection works** (auto-categorizes correctly)
6. ✅ **WebSocket shows green connection status**

## 🔐 Security Notes

- Service runs as root (adjust permissions for production)
- All ports open for demonstration
- Use environment variables for credentials in production

## 📞 Support

If you encounter issues:

1. Check the logs: `sudo journalctl -u ai-automation-agent -f`
2. Verify service status: `sudo systemctl status ai-automation-agent`
3. Test API endpoints manually with curl
4. Check celorisdesigns.com API accessibility

## 🎊 You're Ready!

Once deployed and tested:

- **Dashboard**: http://217.217.248.191:8000
- **API**: http://217.217.248.191:8000/api
- **Management**: `sudo systemctl` commands
- **Monitoring**: Real-time in dashboard
- **Auto-publishing**: Works automatically to celorisdesigns.com

Happy automating! 🤖✨

---

*Generated by MiniMax Agent - Optimized for celorisdesigns.com Integration*