# Troubleshooting Guide - AI Automation Agent

## 🏁 Quick Diagnostics

Before diving into specific issues, run these quick diagnostic commands:

```bash
# Check service status
python service_manager.py status

# Test MongoDB connection
python tests/test_mongodb_connection.py

# View recent logs
python service_manager.py logs | tail -20

# Test web interface
curl http://localhost:8000/api/health
```

## 🚨 Common Issues & Solutions

### 1. MongoDB Connection Failed

**Symptoms:**
- "MongoDB connection failed" error
- Service fails to start
- Database-related errors in logs

**Solutions:**

**Check MongoDB Status:**
```bash
# Check if MongoDB is running
sudo systemctl status mongodb

# Check MongoDB version
mongosh --version

# Test MongoDB connection manually
mongosh mongodb://localhost:27017
```

**Install MongoDB:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb

# CentOS/RHEL
sudo yum install mongodb
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Fix MongoDB Configuration:**
```bash
# Check MongoDB configuration
sudo nano /etc/mongodb.conf

# Ensure MongoDB is listening on correct interface
# Bind to 0.0.0.0 for remote access, 127.0.0.1 for local only

# Restart MongoDB
sudo systemctl restart mongodb
```

**Check Firewall:**
```bash
# Allow MongoDB through firewall
sudo ufw allow 27017
sudo firewall-cmd --permanent --add-port=27017/tcp
sudo firewall-cmd --reload
```

### 2. Import Errors (Module Not Found)

**Symptoms:**
- "ModuleNotFoundError: No module named 'xyz'"
- Import errors when starting service
- Missing dependency errors

**Solutions:**

**Reinstall Dependencies:**
```bash
# Force reinstall all dependencies
pip install --force-reinstall -r requirements.txt

# Install specific missing module
pip install pymongo
pip install fastapi
pip install loguru
```

**Check Python Path:**
```bash
# Verify Python can find modules
python -c "import sys; print('\n'.join(sys.path))"

# Add current directory to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Fix Path Issues:**
```bash
# Ensure you're in the correct directory
cd ai-automation-agent/AI_Automation_Agent

# Run service from correct location
python service_manager.py start
```

### 3. Service Won't Start / Process Issues

**Symptoms:**
- Service fails to start
- "Address already in use" error
- Process crashes immediately

**Solutions:**

**Check Port Conflicts:**
```bash
# Check what's using port 8000
sudo netstat -tulpn | grep :8000
sudo lsof -i :8000

# Kill process using the port
sudo kill -9 $(sudo lsof -t -i:8000)
```

**Check PID File Issues:**
```bash
# Remove stale PID file
rm -f ai_automation_agent.pid

# Check for zombie processes
ps aux | grep python
pkill -f "ai_automation_agent"
```

**Debug Service Start:**
```bash
# Start in foreground for debugging
python start_background_service.py

# Check for permission issues
ls -la service_manager.py
chmod +x service_manager.py
```

### 4. Web Interface Not Loading

**Symptoms:**
- Dashboard shows loading spinner
- Web interface returns 500 errors
- Connection refused errors

**Solutions:**

**Check Service Status:**
```bash
python service_manager.py status
python service_manager.py logs
```

**Test Web Interface Directly:**
```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test main page
curl http://localhost:8000
```

**Check Dependencies:**
```bash
# Verify all web interface dependencies
pip list | grep -E "(fastapi|uvicorn|jinja2)"

# Reinstall if needed
pip install fastapi uvicorn jinja2 python-multipart
```

**Check Configuration:**
```bash
# Verify environment variables
cat .env.celorisdesigns | grep -E "(PORT|DEBUG|SESSION_SECRET)"

# Ensure port is not in use
sudo netstat -tulpn | grep :8000
```

### 5. Blog Generation Failures

**Symptoms:**
- "OpenAI API key not configured"
- "AI service unavailable" errors
- Generated content is empty or malformed

**Solutions:**

**Check OpenAI Configuration:**
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test OpenAI API manually
python -c "
import openai
import os
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
response = client.chat.completions.create(
    model='gpt-3.5-turbo',
    messages=[{'role': 'user', 'content': 'Hello'}],
    max_tokens=10
)
print('✅ OpenAI API working')
"
```

**Fix API Key Issues:**
```bash
# Add to environment
export OPENAI_API_KEY="your_actual_api_key_here"

# Or add to .env.celorisdesigns
echo "OPENAI_API_KEY=your_actual_api_key_here" >> .env.celorisdesigns
```

**Check API Limits:**
```bash
# Monitor API usage in OpenAI dashboard
# Check for rate limiting
# Verify billing account status
```

### 6. Next.js Integration Issues

**Symptoms:**
- "Session authentication failed"
- Publishing to Next.js fails
- 401/403 errors from Next.js API

**Solutions:**

**Verify Session Configuration:**
```bash
# Check session data format
echo $NEXTJS_ADMIN_SESSION

# Validate JSON format
python -c "
import json
session = json.loads('$NEXTJS_ADMIN_SESSION')
print('Session data:', session)
"
```

**Test Next.js API:**
```bash
# Test API endpoint manually
curl -X POST https://your-domain.com/api/admin/blog \
  -H "Content-Type: application/json" \
  -H "x-admin-session: $NEXTJS_ADMIN_SESSION" \
  -d '{"title":"Test","content":"Test content","status":"draft"}'
```

**Fix Session Data:**
```json
{
    "id": "your_actual_admin_user_id",
    "email": "admin@yourdomain.com",
    "role": "admin"
}
```

**Check API Endpoint:**
```bash
# Verify Next.js blog API endpoint
curl -I https://your-domain.com/api/admin/blog
```

### 7. Permission Denied Errors

**Symptoms:**
- "Permission denied" when running scripts
- Cannot create PID files
- Cannot write to logs directory

**Solutions:**

**Fix Script Permissions:**
```bash
chmod +x service_manager.py
chmod +x start_background_service.py
chmod +x quick_fix_mysql_error.sh
```

**Fix File Ownership:**
```bash
# Change ownership to current user
sudo chown -R $USER:$USER ~/ai-automation-agent

# Or fix specific files
sudo chown $USER:$USER ai_automation_agent.pid
sudo chown $USER:$USER logs/
```

**Create Required Directories:**
```bash
# Create logs directory
mkdir -p logs

# Create other required directories
mkdir -p data
mkdir -p uploads
```

### 8. High Memory/CPU Usage

**Symptoms:**
- Server becomes slow
- High memory usage
- Service crashes with out-of-memory

**Solutions:**

**Monitor Resource Usage:**
```bash
# Check process resource usage
ps aux | grep python
top -p $(pgrep -f ai_automation_agent)

# Check memory usage
free -h
df -h
```

**Optimize Configuration:**
```bash
# Reduce concurrent requests
export MAX_CONCURRENT_REQUESTS=2

# Lower token limits
export MAX_TOKENS=1000

# Enable garbage collection
export PYTHONHASHSEED=0
```

**Scale Resources:**
```bash
# Add swap space
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 🔧 Advanced Debugging

### Enable Debug Mode

```bash
# Enable comprehensive debugging
export DEBUG=true
export LOG_LEVEL=DEBUG
export DETAILED_API_LOGGING=true

# Start service with debug output
python service_manager.py start
```

### Log Analysis

```bash
# View logs with timestamps
python service_manager.py logs | grep -E "[0-9]{4}-[0-9]{2}-[0-9]{2}"

# Filter for specific error types
python service_manager.py logs | grep -i error

# Monitor logs in real-time
tail -f logs/agent.log
```

### Performance Monitoring

```bash
# Monitor service performance
python -c "
from config.settings import settings
from config.database import db_manager
print(f'Database: {settings.DATABASE_TYPE}')
print(f'Port: {settings.CHATBOT_PORT}')
print(f'MongoDB URI: {settings.MONGODB_URI}')
"

# Test API performance
time curl http://localhost:8000/api/health
```

### Network Diagnostics

```bash
# Check if port is accessible
telnet localhost 8000
nc -zv localhost 8000

# Check network connectivity
ping google.com
curl -I http://google.com
```

## 🛠️ System Information Commands

### System Health Check

```bash
# Check system resources
free -h
df -h
uptime

# Check Python version
python --version
pip --version

# Check installed packages
pip list | grep -E "(fastapi|uvicorn|pymongo|loguru|openai)"
```

### Service Information

```bash
# Check running processes
ps aux | grep python
pgrep -f ai_automation_agent

# Check open ports
sudo netstat -tulpn | grep python
sudo lsof -i :8000
```

## 📞 Getting Help

### Collect Diagnostic Information

Before seeking help, gather this information:

```bash
# System information
uname -a
python --version
pip --version

# Service status
python service_manager.py status

# Recent logs
python service_manager.py logs | tail -50

# Configuration (remove sensitive data)
grep -v -E "(API_KEY|SECRET|PASSWORD)" .env.celorisdesigns

# Error messages from startup
python service_manager.py start 2>&1 | tee startup.log
```

### Common Support Channels

1. **GitHub Issues** - For bugs and feature requests
2. **Documentation** - Check API_REFERENCE.md and SETUP_GUIDE.md
3. **Community Forums** - For general questions
4. **Professional Support** - For critical production issues

### Issue Template

When reporting issues, include:

```
**Environment:**
- OS: [e.g., Ubuntu 20.04]
- Python: [e.g., 3.9.7]
- MongoDB: [e.g., 5.0.3]

**Issue Description:**
[Clear description of the problem]

**Steps to Reproduce:**
1. Step one
2. Step two
3. See error

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Error Messages:**
```
[Paste relevant error messages]
```

**Configuration:**
[Relevant config settings, remove sensitive data]

**Logs:**
[Relevant log entries]
```

## 🔄 Recovery Procedures

### Complete Service Reset

If all else fails, perform a complete reset:

```bash
# Stop service
python service_manager.py stop

# Remove PID file
rm -f ai_automation_agent.pid

# Clear logs
rm -f logs/agent.log

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Restart service
python service_manager.py start
```

### Database Reset

**⚠️ Warning: This will delete all data**

```bash
# Backup existing data
mongodump --db ai_automation --out backup_$(date +%Y%m%d_%H%M%S)

# Reset database
mongo ai_automation --eval "db.dropDatabase()"

# Restart service
python service_manager.py restart
```

### Clean Installation

For a completely fresh start:

```bash
# Remove existing installation
rm -rf ~/ai-automation-agent

# Fresh git clone
git clone https://github.com/YOUR_USERNAME/ai-automation-agent.git
cd ai-automation-agent

# Follow setup guide
./setup_github_repo.sh
# Follow SETUP_GUIDE.md instructions
```

## 📋 Maintenance Checklist

### Daily
- [ ] Check service status: `python service_manager.py status`
- [ ] Verify web interface: http://localhost:8000
- [ ] Monitor logs for errors: `python service_manager.py logs | tail -20`

### Weekly
- [ ] Check disk space: `df -h`
- [ ] Monitor MongoDB: `mongo --eval "db.stats()"`
- [ ] Review API usage and limits
- [ ] Update dependencies: `pip install --upgrade -r requirements.txt`

### Monthly
- [ ] Backup database: `mongodump`
- [ ] Review and rotate API keys
- [ ] Update system packages: `sudo apt update && sudo apt upgrade`
- [ ] Performance analysis and optimization

### Security
- [ ] Check for security updates
- [ ] Review access logs
- [ ] Update configuration if needed
- [ ] Monitor for suspicious activity

Remember: Prevention is better than cure. Regular monitoring and maintenance can prevent most issues from occurring in the first place.