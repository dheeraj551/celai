# 🚀 VPS DEPLOYMENT COMMANDS - Blog Publishing Features

## Immediate Deployment Commands

Execute these commands on your VPS (217.217.248.191) to deploy the blog publishing features:

### 1. Pull Latest Changes
```bash
ssh root@217.217.248.191
cd ~/ai-automation-agent/AI_Automation_Agent
git pull origin master
```

### 2. Quick Deployment (Recommended)
```bash
# Make script executable
chmod +x quick_blog_deployment.sh

# Run deployment
bash quick_blog_deployment.sh
```

### 3. Full Featured Deployment (Alternative)
```bash
# Make script executable  
chmod +x deploy_with_blog_features.sh

# Run full deployment with all features
bash deploy_with_blog_features.sh
```

### 4. Manual Steps (If Scripts Don't Work)
```bash
# Kill existing processes
pkill -f "working_agent.py" 2>/dev/null || true

# Ensure dependencies
pip3 install fastapi uvicorn openai requests beautifulsoup4 python-dotenv

# Start application
nohup python3 working_agent.py > logs/deployment.log 2>&1 &
echo $! > logs/app.pid

# Check status
sleep 3
ps aux | grep working_agent.py
```

## ✅ Verification Commands

After deployment, verify everything is working:

```bash
# Check if application is running
ps aux | grep working_agent.py

# Test main endpoint
curl -s http://localhost:8000/ | head -5

# Test blog settings endpoint
curl -s http://localhost:8000/api/blog/settings

# View logs if needed
tail -f logs/deployment.log
```

## 🌐 Access URLs

Once deployed successfully:
- **Dashboard**: http://217.217.248.191:8000
- **Blog Automation**: http://217.217.248.191:8000/blog-automation
- **Analytics**: http://217.217.248.191:8000/analytics

## 📝 Blog Publishing Features Now Available

✅ **AI Blog Generation**: Generate single blog posts with OpenAI
✅ **Blog Series Creation**: Create multiple related posts automatically  
✅ **Automated Scheduling**: Schedule daily/weekly blog generation
✅ **Multi-Platform Publishing**: WordPress, Medium, Dev.to, LinkedIn
✅ **Content Management**: Edit, manage, and organize all blog posts
✅ **Analytics Dashboard**: Track blog performance and engagement

## 🔧 Configuration Required

### OpenAI API Key
Ensure your OpenAI API key is set:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

### Platform Credentials (Optional)
Configure publishing platforms in the web interface settings.

## 🚨 If Deployment Fails

1. **Check logs**: `tail -50 logs/deployment.log`
2. **Test dependencies**: `python3 -c "import fastapi, uvicorn, openai; print('OK')"`
3. **Check port**: `netstat -tulpn | grep :8000`
4. **Restart**: `bash quick_blog_deployment.sh`

## 🎯 Quick Test

Generate your first blog post:
1. Go to http://217.217.248.191:8000/blog-automation
2. Click "Generate Blog"
3. Enter topic (e.g., "AI Automation")
4. Select style and length
5. Click Generate

Your blog publishing system is ready to use! 🚀