# AI Automation Agent - Setup Guide

## 🏁 Quick Start (5 Minutes)

### 1. Prerequisites Check
```bash
# Check Python version (3.8+ required)
python --version

# Check MongoDB
mongosh --version

# Check OpenAI API key
echo $OPENAI_API_KEY
```

### 2. Repository Setup
```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/ai-automation-agent.git
cd ai-automation-agent

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env.celorisdesigns
nano .env.celorisdesigns
```

### 3. Configuration
Edit `.env.celorisdesigns` with your settings:

```bash
# Essential configurations
OPENAI_API_KEY=your_actual_openai_api_key
NEXTJS_BLOG_API=https://your-domain.com/api/admin/blog
NEXTJS_ADMIN_SESSION='{"id":"your-admin-id","email":"admin@yourdomain.com","role":"admin"}'
CHATBOT_PORT=8000
```

### 4. Start Service
```bash
# Test MongoDB connection
python tests/test_mongodb_connection.py

# Start the agent
python service_manager.py start

# Access dashboard
# Open browser to: http://localhost:8000
```

## 📝 Configuration Details

### Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for content generation | `sk-...` |
| `DATABASE_TYPE` | Yes | Database type (`mongodb` recommended) | `mongodb` |
| `MONGODB_URI` | Yes | MongoDB connection string | `mongodb://localhost:27017/ai_automation` |
| `NEXTJS_BLOG_API` | Optional | Next.js admin blog API endpoint | `https://your-domain.com/api/admin/blog` |
| `NEXTJS_ADMIN_SESSION` | Optional | Admin session JSON for Next.js auth | `{"id":"123","email":"admin@domain.com","role":"admin"}` |
| `CHATBOT_PORT` | Yes | Web interface port | `8000` |
| `SESSION_SECRET` | Yes | Session encryption secret | `your-random-secret-key` |

### MongoDB Setup

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

**CentOS/RHEL:**
```bash
sudo yum install mongodb
sudo systemctl start mongod
sudo systemctl enable mongod
```

**Docker (Alternative):**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### Next.js Integration Setup

1. **Create Admin User** in your Next.js database
2. **Get Admin Session** from your Next.js admin panel
3. **Configure Environment:**
   ```bash
   NEXTJS_ADMIN_SESSION='{"id":"your-user-id","email":"admin@domain.com","role":"admin"}'
   ```

## 🛠️ Troubleshooting

### Common Issues

**MongoDB Connection Failed**
```bash
# Check MongoDB status
sudo systemctl status mongodb

# Restart MongoDB
sudo systemctl restart mongodb

# Check MongoDB logs
sudo journalctl -u mongodb -f
```

**Permission Denied**
```bash
# Fix script permissions
chmod +x service_manager.py
chmod +x start_background_service.py

# Fix file ownership (if needed)
sudo chown -R $USER:$USER ~/ai-automation-agent
```

**Import Errors**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**Service Won't Start**
```bash
# Check service status
python service_manager.py status

# View detailed logs
python service_manager.py logs

# Kill any existing processes
pkill -f "python.*service_manager"
```

### Debug Mode

Enable verbose logging:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
export DETAILED_API_LOGGING=true
python service_manager.py start
```

## 🔄 Service Management

### Commands Reference

```bash
# Service operations
python service_manager.py start     # Start in background
python service_manager.py stop      # Stop service
python service_manager.py restart   # Restart service
python service_manager.py status    # Check service status
python service_manager.py logs      # View live logs

# Manual start (for debugging)
python start_background_service.py

# Direct web interface start
python web_interface/app.py
```

### Background Service Features

- **Auto-restart** on crashes
- **PID file management** for process tracking
- **Graceful shutdown** on system signals
- **Comprehensive logging** with rotation
- **Health monitoring** and status reporting

## 📊 Testing & Validation

### Connection Tests
```bash
# Test MongoDB connection
python tests/test_mongodb_connection.py

# Test Next.js integration
python tests/test_nextjs_integration.py

# Test web interface
curl http://localhost:8000/api/health
```

### Performance Tests
```bash
# Generate test blog post
python -c "
from modules.blog_automation.blog_generator import BlogGenerator
generator = BlogGenerator()
blog = generator.generate_blog('AI Technology', max_words=500)
print('✅ Blog generation working!')
"
```

## 🚀 Production Deployment

### VPS Deployment
1. **Upload to VPS:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-automation-agent.git
   cd ai-automation-agent
   ```

2. **Setup Environment:**
   ```bash
   pip install -r requirements.txt
   cp .env.example .env.celorisdesigns
   nano .env.celorisdesigns  # Add your actual API keys
   ```

3. **Configure Firewall:**
   ```bash
   sudo ufw allow 8000
   sudo ufw allow 22
   sudo ufw enable
   ```

4. **Start Service:**
   ```bash
   python service_manager.py start
   ```

5. **Access Dashboard:**
   ```
   http://YOUR_VPS_IP:8000
   ```

### Systemd Service (Optional)

Create `/etc/systemd/system/ai-automation-agent.service`:
```ini
[Unit]
Description=AI Automation Agent
After=network.target mongodb.service

[Service]
Type=forking
User=root
WorkingDirectory=/path/to/ai-automation-agent
ExecStart=/usr/bin/python service_manager.py start
ExecStop=/usr/bin/python service_manager.py stop
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-automation-agent
sudo systemctl start ai-automation-agent
```

## 📚 API Documentation

### Web Interface Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/health` | GET | Health check |
| `/api/generate-blog` | POST | Generate blog post |
| `/api/schedule-blog` | POST | Schedule blog generation |
| `/api/performance` | GET | Get performance metrics |
| `/api/logs` | GET | Get service logs |

### Usage Examples

**Generate Blog via API:**
```bash
curl -X POST http://localhost:8000/api/generate-blog \
  -H "Content-Type: application/json" \
  -d '{"topic":"AI in healthcare","max_words":800}'
```

**Get Performance Metrics:**
```bash
curl http://localhost:8000/api/performance
```

## 🔒 Security Best Practices

1. **Environment Variables:**
   - Never commit `.env.celorisdesigns` to git
   - Use strong, unique secrets
   - Rotate API keys regularly

2. **Network Security:**
   - Use HTTPS in production
   - Configure firewall rules
   - Limit database access

3. **Access Control:**
   - Restrict admin dashboard access
   - Use session-based authentication
   - Monitor API usage

4. **Monitoring:**
   - Enable comprehensive logging
   - Set up alerts for failures
   - Regular security updates

## 🎯 Next Steps

After successful setup:

1. **Customize Blog Topics:** Edit `BLOG_TOPICS` in `.env.celorisdesigns`
2. **Schedule Content:** Use the dashboard to schedule blog generation
3. **Monitor Performance:** Check dashboard metrics regularly
4. **Set up Backups:** Configure MongoDB backups
5. **Scale if Needed:** Consider additional instances for high traffic

For advanced usage, see [API_REFERENCE.md](API_REFERENCE.md) and [TROUBLESHOOTING.md](TROUBLESHOOTING.md).