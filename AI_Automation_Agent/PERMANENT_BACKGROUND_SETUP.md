# Keep AI Automation Agent Running Permanently

## Problem Solved: No More Terminal Dependency!

Your agent stops when you close the terminal because it's running in **foreground mode**. Here's how to run it permanently in the background:

## 🔧 Solution 1: Background Service (Recommended)

### Start the Service
```bash
# Navigate to your AI Automation Agent directory
cd AI_Automation_Agent

# Start service in background (runs permanently)
python service_manager.py start
```

### Verify It's Running
```bash
# Check service status
python service_manager.py status

# Expected output:
# ✅ ai-automation-agent is RUNNING
#    PID: 12345
#    Web Interface: http://localhost:8000
#    Status API: http://localhost:8000/api/status
```

### Test Permanent Operation
1. **Start the service**: `python service_manager.py start`
2. **Close your terminal window completely**
3. **Open a new browser**: Go to `http://localhost:8000`
4. **Result**: ✅ Web interface still works!

## 🛠️ Solution 2: System Service (Linux Production)

For maximum reliability on Linux servers:

### Create System Service
```bash
# Create service file
sudo nano /etc/systemd/system/ai-automation-agent.service
```

### Service Configuration
```ini
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
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

### Enable and Start
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service (starts automatically on boot)
sudo systemctl enable ai-automation-agent

# Start service
sudo systemctl start ai-automation-agent

# Check status
sudo systemctl status ai-automation-agent
```

### Service Management Commands
```bash
sudo systemctl start ai-automation-agent    # Start
sudo systemctl stop ai-automation-agent     # Stop
sudo systemctl restart ai-automation-agent  # Restart
sudo systemctl status ai-automation-agent   # Check status
sudo journalctl -u ai-automation-agent -f   # View logs
```

## 🖥️ Solution 3: Screen/Tmux Session

For development environments:

### Using Screen
```bash
# Install screen
sudo apt install screen

# Create new session
screen -S ai-agent

# Start the web interface
python start_web_interface.py

# Detach from session (don't close terminal yet)
# Press: Ctrl+A, then D

# Later, reattach with:
screen -r ai-agent
```

### Using Tmux
```bash
# Install tmux
sudo apt install tmux

# Create new session
tmux new -s ai-agent

# Start the web interface
python start_web_interface.py

# Detach from session
# Press: Ctrl+B, then D

# Later, reattach with:
tmux attach -t ai-agent
```

## 📋 Complete Management Commands

### Background Service Manager
```bash
# Start service (runs in background)
python service_manager.py start

# Check if running
python service_manager.py status

# Stop service
python service_manager.py stop

# Restart service
python service_manager.py restart

# View recent logs
python service_manager.py logs

# View live logs
tail -f logs/background_service.log
```

## 🔍 Troubleshooting

### Check if Service is Running
```bash
# Method 1: Using service manager
python service_manager.py status

# Method 2: Check port
sudo netstat -tlnp | grep :8000

# Method 3: Check process
ps aux | grep python | grep start_web_interface
```

### If Service Stops Unexpectedly
```bash
# Check logs for errors
python service_manager.py logs

# Restart service
python service_manager.py restart

# If MongoDB issues, restart it:
sudo systemctl restart mongod
```

### If Port is Already in Use
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use a different port in .env file:
CHATBOT_PORT=8001
```

## 🌐 Access Points (When Running)

Once your service is running permanently:

- **Main Dashboard**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health
- **Agent Status**: http://localhost:8000/api/status
- **Blog Posts**: http://localhost:8000/api/blog/posts
- **Analytics**: http://localhost:8000/api/analytics/summary

## ⚡ Quick Setup Commands

### One-Time Setup
```bash
# 1. Navigate to project
cd AI_Automation_Agent

# 2. Start as background service
python service_manager.py start

# 3. Verify it's working
python service_manager.py status

# 4. Test in browser
# Visit: http://localhost:8000
```

### Daily Usage
```bash
# Check status anytime
python service_manager.py status

# View logs if needed
python service_manager.py logs

# Restart if issues
python service_manager.py restart
```

## 🎯 Best Practices

1. **Always use background service** (`service_manager.py`) for production
2. **Monitor logs regularly** to catch issues early
3. **Set up system service** on Linux servers for maximum reliability
4. **Use health endpoint** (`/api/health`) to verify system status
5. **Keep MongoDB running** as a system service

## 🔒 Security Notes

- Change `SESSION_SECRET` in production
- Use HTTPS in production environments
- Restrict access to port 8000 via firewall
- Regular security updates for MongoDB

## 📞 Emergency Recovery

If everything fails:
```bash
# Complete restart
python service_manager.py stop
rm -f web_interface.pid logs/*.log*
python service_manager.py start

# Check if MongoDB is running
sudo systemctl status mongod

# View detailed logs
python service_manager.py logs 100
```

This solution ensures your AI Automation Agent runs permanently, regardless of terminal sessions!