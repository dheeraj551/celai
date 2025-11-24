# AI Automation Agent - Troubleshooting Guide

## Issues and Solutions

### 1. Dashboard Loading Icon Issue

**Problem**: The dashboard shows only loading spinners and never loads data.

**Common Causes and Solutions**:

#### A. Database Connection Issues
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB if not running
sudo systemctl start mongod

# Test MongoDB connection
mongo --eval "db.adminCommand('ping')"
```

#### B. Missing Dependencies
```bash
# Install required Python packages
pip install fastapi uvicorn pymongo loguru python-dotenv jinja2 python-multipart

# Or install from requirements
pip install -r requirements.txt
```

#### C. Configuration Issues
```bash
# Check your environment configuration
cat .env.celorisdesigns

# Make sure CHATBOT_PORT is set to 8000 (not 8080)
# Ensure DEBUG=true for development
```

#### D. API Health Check
Visit: `http://localhost:8000/api/health` to check:
- Database connection status
- Agent initialization
- Configuration loading

### 2. Terminal Dependency Issue

**Problem**: Web interface stops when you close the terminal.

**Solutions**:

#### Solution A: Background Service (Recommended)
```bash
# Start service in background
python service_manager.py start

# Check status
python service_manager.py status

# Stop service
python service_manager.py stop

# View logs
python service_manager.py logs
```

#### Solution B: System Service (Linux)
```bash
# Create systemd service file
sudo nano /etc/systemd/system/ai-automation-agent.service

# Add the following content:
[Unit]
Description=AI Automation Agent Web Interface
After=network.target mongod.service

[Service]
Type=simple
User=root
WorkingDirectory=/root/ai-automation-agent
ExecStart=/usr/bin/python3 /root/ai-automation-agent/start_web_interface.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable ai-automation-agent
sudo systemctl start ai-automation-agent

# Check status
sudo systemctl status ai-automation-agent
```

#### Solution C: Screen/Tmux Session
```bash
# Install screen
sudo apt install screen

# Create new screen session
screen -S ai-agent

# Start the web interface
python start_web_interface.py

# Detach from session (Ctrl+A, then D)
# Reattach later with: screen -r ai-agent
```

### 3. Port Already in Use

**Problem**: "Address already in use" error on port 8000.

**Solutions**:
```bash
# Find process using port 8000
sudo netstat -tlnp | grep :8000

# Kill the process
sudo kill -9 <PID>

# Or use lsof
sudo lsof -i :8000
sudo kill -9 <PID>
```

### 4. Database Connection Errors

**Problem**: "MongoDB connection failed" or similar database errors.

**Solutions**:
```bash
# Install MongoDB
sudo apt update
sudo apt install mongodb

# Start MongoDB service
sudo systemctl start mongodb
sudo systemctl enable mongodb

# Check MongoDB status
sudo systemctl status mongodb

# Test connection
mongo --eval "db.adminCommand('ping')"
```

### 5. Environment Variables Not Loading

**Problem**: Settings showing as "None" or default values.

**Solutions**:
```bash
# Ensure .env file exists and is in the right location
ls -la .env*

# Check file permissions
chmod 644 .env.celorisdesigns

# Copy to .env if needed
cp .env.celorisdesigns .env

# Verify Python-dotenv is installed
pip install python-dotenv
```

### 6. WebSocket Connection Issues

**Problem**: Real-time updates not working.

**Solutions**:
- Check browser console for WebSocket errors
- Ensure firewall allows WebSocket connections
- Try refreshing the page
- Check network connectivity

### 7. API Endpoints Not Responding

**Problem**: 500 errors or connection timeouts.

**Solutions**:
```bash
# Check server logs
tail -f logs/web_interface.log

# Run in debug mode
DEBUG=true python start_web_interface.py

# Test individual endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/status
```

## Diagnostic Commands

### Quick System Check
```bash
# Check all services
python service_manager.py status

# View recent logs
python service_manager.py logs 20

# Test health endpoint
curl http://localhost:8000/api/health

# Check database connection
python -c "from config.database import db_manager; print('DB Connected' if db_manager.mongo_db else 'DB Disconnected')"
```

### Complete Restart
```bash
# Stop service
python service_manager.py stop

# Clear logs
rm -f logs/*.log*

# Restart
python service_manager.py start

# Monitor startup
python service_manager.py logs 50
```

## Performance Optimization

### For Production Use
1. **Enable Caching**: Configure Redis for session caching
2. **Database Optimization**: Add database indexes
3. **Static Files**: Serve static files separately
4. **Load Balancing**: Use nginx for reverse proxy
5. **Monitoring**: Set up log monitoring and alerts

### Memory Usage
```bash
# Monitor memory usage
ps aux | grep python

# Check for memory leaks
python -m memory_profiler start_web_interface.py
```

## Emergency Recovery

### If Nothing Works
```bash
# Complete reset
sudo systemctl stop ai-automation-agent
rm -rf logs/ web_interface.pid
pip install --upgrade -r requirements.txt
python service_manager.py start
```

### Create Fresh Installation
```bash
# Backup configuration
cp .env.celorisdesigns .env.backup

# Fresh start
pip install -r requirements.txt
python service_manager.py start
```

## Getting Help

### Log Analysis
- Check `logs/background_service.log` for service issues
- Check `logs/web_interface.log` for API issues
- Check browser console for frontend issues

### Information to Collect
1. Operating system and version
2. Python version (`python --version`)
3. Error messages from logs
4. Output of diagnostic commands
5. Screenshots of issues

### Support
For additional help, check:
- `logs/` directory for detailed error information
- Browser developer console for frontend errors
- System logs for system-level issues