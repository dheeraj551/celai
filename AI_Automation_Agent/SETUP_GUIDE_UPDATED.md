# AI Automation Agent - Complete Setup Guide (Updated)

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [System Requirements](#system-requirements)
3. [Quick Start Guide](#quick-start-guide)
4. [Database Configuration](#database-configuration)
5. [Environment Variables Configuration](#environment-variables-configuration)
6. [Next.js Integration Setup](#nextjs-integration-setup)
7. [Module Setup & Testing](#module-setup--testing)
8. [Web Interface](#web-interface)
9. [VPS Deployment](#vps-deployment)
10. [Troubleshooting](#troubleshooting)
11. [Migration from Previous Versions](#migration-from-previous-versions)

## System Architecture Overview

### Current Architecture (2025)
```
┌─────────────────────────────────────────────────────────┐
│                 AI Automation Agent                     │
│  ┌─────────────────┐    ┌─────────────────┐            │
│  │   Core Engine   │    │   Web Interface │            │
│  │                 │    │                 │            │
│  │ • Blog Creation │    │ • Status Panel  │            │
│  │ • Course Gen.   │◄──►│ • Controls      │            │
│  │ • Job Matching  │    │ • Analytics     │            │
│  │ • Data Mgmt     │    │ • Settings      │            │
│  └─────────────────┘    └─────────────────┘            │
└─────────────────────────────────────────────────────────┘
           │                       │                       │
           ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Next.js APIs   │    │  Database       │    │  AI Services    │
│                 │    │                 │    │                 │
│ • Blog Posts    │    │ • MongoDB/MySQL │    │ • OpenAI GPT    │
│ • Course Data   │    │ • User Profiles │    │ • Content Gen   │
│ • Job Data      │    │ • Analytics     │    │ • Analysis      │
│ • File Storage  │    └─────────────────┘    └─────────────────┘
└─────────────────┘
```

### Key Improvements (2025 Update)
- ✅ **API-First Design**: Direct HTTP communication instead of web automation
- ✅ **Simplified Setup**: No Node.js or browser automation required
- ✅ **Enhanced Error Handling**: Comprehensive logging and retry logic
- ✅ **Draft Mode**: Safe testing before publishing
- ✅ **Modular Architecture**: Each module independently testable
- ✅ **Web Interface**: Full control panel with real-time status

## System Requirements

### Minimum VPS Requirements
- **OS**: Ubuntu 20.04 LTS or newer
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: 2 cores minimum, 4 cores recommended
- **Storage**: 20GB SSD minimum
- **Network**: Stable internet connection (10 Mbps minimum)

### Software Dependencies
- **Python**: 3.8 or higher
- **Git**: Latest version
- **Database**: MongoDB 5.0+ or MySQL 8.0+
- **Optional**: Docker for containerized deployment

### NOT Required (Removed in 2025)
- ❌ Node.js (No longer needed for Next.js integration)
- ❌ Chrome/Firefox browsers
- ❌ Selenium/Playwright
- ❌ Web automation dependencies

## Quick Start Guide

### 1. System Preparation
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install core dependencies
sudo apt install python3 python3-pip python3-venv git curl wget -y

# Install Python development tools
sudo apt install build-essential libssl-dev libffi-dev -y

# Create project directory
mkdir ~/ai-automation-agent
cd ~/ai-automation-agent

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 2. Project Setup
```bash
# Clone or extract project files
# If you have the source code:
# git clone <repository-url> .

# Install dependencies
pip install -r requirements.txt

# Create required directories
mkdir -p logs config modules web_interface/static web_interface/templates
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit environment file
nano .env
```

## Database Configuration

### Option 1: MongoDB (Recommended)

#### Installation
```bash
# Import MongoDB repository
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify installation
sudo systemctl status mongod
```

#### Configuration
```bash
# Connect to MongoDB
mongosh

# In MongoDB shell:
use ai_automation
db.createUser({
  user: "ai_agent",
  pwd: "secure_password_here",
  roles: ["readWrite"]
})

# Exit with exit or quit()
```

### Option 2: MySQL

#### Installation
```bash
# Install MySQL
sudo apt install mysql-server mysql-client -y

# Secure MySQL installation
sudo mysql_secure_installation
```

#### Configuration
```bash
# Login to MySQL
sudo mysql -u root -p

# Create database and user
CREATE DATABASE ai_automation;
CREATE USER 'ai_agent'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON ai_automation.* TO 'ai_agent'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Environment Variables Configuration

### Complete .env Configuration

```bash
# ===============================
# CORE CONFIGURATION
# ===============================

# Database Configuration (Choose ONE)
DATABASE_TYPE=mongodb
# MongoDB Configuration
MONGODB_URI=mongodb://ai_agent:your_password@localhost:27017/ai_automation

# OR MySQL Configuration
# DATABASE_TYPE=mysql
# MYSQL_HOST=localhost
# MYSQL_PORT=3306
# MYSQL_USER=ai_agent
# MYSQL_PASSWORD=your_password
# MYSQL_DATABASE=ai_automation

# ===============================
# AI SERVICES
# ===============================

# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=sk-your-openai-api-key-here

# AI Model Settings
AI_MODEL=gpt-3.5-turbo
MAX_TOKENS=2000
TEMPERATURE=0.7

# ===============================
# BLOG AUTOMATION
# ===============================

# Blog Generation Settings
BLOG_FREQUENCY=daily
BLOG_TOPICS=technology,ai,programming,web-development,startups
BLOG_MAX_LENGTH=1500
BLOG_PUBLISH_TO=nextjs
BLOG_DEFAULT_STATUS=draft

# Blog Scheduling
BLOG_ENABLED=true
BLOG_MIN_INTERVAL_HOURS=24
BLOG_CONTENT_TONE=professional

# ===============================
# NEXT.JS INTEGRATION
# ===============================

# Next.js API Configuration (REQUIRED for Next.js publishing)
NEXTJS_BLOG_API=https://your-nextjs-site.com/api/blogs
NEXTJS_API_KEY=your_secure_api_key_here
NEXTJS_AUTH_HEADER=Authorization
NEXTJS_API_TIMEOUT=30

# ===============================
# PUBLISHING PLATFORMS
# ===============================

# WordPress Configuration (Optional)
WORDPRESS_URL=https://yourblog.com
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_application_password

# Medium Configuration (Optional)
MEDIUM_TOKEN=your_medium_integration_token

# ===============================
# WEB INTERFACE
# ===============================

# Web Interface Configuration
WEB_INTERFACE_HOST=0.0.0.0
WEB_INTERFACE_PORT=8080
WEB_INTERFACE_DEBUG=false

# ===============================
# COURSE CREATION
# ===============================

# Course Generation Settings
COURSE_ENABLED=true
COURSE_TOPICS=python,web-development,data-science,ai,entrepreneurship
COURSE_MAX_MODULES=10
COURSE_CONTENT_LENGTH=5000
COURSE_LANGUAGE=en

# Course Structure
COURSE_LEVELS=beginner,intermediate,advanced
COURSE_TYPES=video,text,quiz,practical
COURSE_STORAGE_PATH=courses/

# ===============================
# JOB AGGREGATION
# ===============================

# Job Search Configuration
JOB_ENABLED=true
JOB_SEARCH_KEYWORDS=python,developer,data scientist,web developer
JOB_SEARCH_LOCATIONS=remote,new york,san francisco,london
JOB_UPDATE_FREQUENCY=hourly
JOB_STORAGE_PATH=jobs/

# Job Sources (API Keys if available)
LINKEDIN_API_KEY=your_linkedin_api_key
GITHUB_JOBS_API_KEY=your_github_jobs_api_key

# ===============================
# LOGGING AND MONITORING
# ===============================

# Log Configuration
LOG_LEVEL=INFO
LOG_FILE_PATH=logs/agent.log
LOG_MAX_SIZE_MB=100
LOG_BACKUP_COUNT=5

# Performance Monitoring
MONITORING_ENABLED=true
HEALTH_CHECK_INTERVAL=300
```

## Next.js Integration Setup

### 1. Basic Next.js API Endpoint Setup

Create a basic Next.js API endpoint to receive blog posts:

```javascript
// pages/api/blogs.js
export default async function handler(req, res) {
  // Handle different HTTP methods
  if (req.method === 'POST') {
    try {
      const { title, content, tags, status, author } = req.body;
      
      // Validate API key
      const authHeader = req.headers.authorization;
      if (!authHeader || authHeader !== `Bearer ${process.env.BLOG_API_KEY}`) {
        return res.status(401).json({ error: 'Unauthorized' });
      }
      
      // Process blog post
      const blogPost = {
        id: Date.now().toString(),
        title,
        content,
        tags: tags || [],
        status: status || 'draft',
        author: author || 'AI Agent',
        createdAt: new Date().toISOString(),
        publishedAt: status === 'published' ? new Date().toISOString() : null
      };
      
      // Save to your database (MongoDB example)
      await mongoose.connect(process.env.MONGODB_URI);
      await mongoose.model('Blog').create(blogPost);
      
      res.status(201).json({ 
        success: true, 
        message: 'Blog post created successfully',
        blogId: blogPost.id
      });
      
    } catch (error) {
      console.error('Blog creation error:', error);
      res.status(500).json({ 
        error: 'Failed to create blog post',
        details: error.message 
      });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
```

### 2. Environment Configuration for Next.js

Add to your Next.js `.env.local`:
```bash
# Database connection
MONGODB_URI=mongodb://localhost:27017/your-nextjs-app

# Blog API key (must match the one in AI agent)
BLOG_API_KEY=your_secure_api_key_here
```

### 3. Test Next.js Integration

Run the integration test:
```bash
cd ~/ai-automation-agent
python test_nextjs_integration.py
```

## Module Setup & Testing

### 1. Blog Automation Module

#### Test Blog Generation
```bash
python -c "
from modules.blog_automation.blog_generator import BlogGenerator
from config.settings import settings

if not settings.OPENAI_API_KEY:
    print('ERROR: OpenAI API key not configured')
    exit(1)

gen = BlogGenerator()
blog = gen.generate_blog('AI in healthcare', max_words=500)
print('✅ Blog Generation: WORKING')
print(f'   Title: {blog[\"title\"]}')
print(f'   Content length: {len(blog[\"content\"])} characters')
"
```

#### Test Database Integration
```bash
python -c "
from config.database import init_database, get_collection
from modules.blog_automation.content_publisher import PublisherManager

# Test database
if init_database():
    print('✅ Database Connection: WORKING')
    collection = get_collection('test')
    result = collection.insert_one({'test': 'data'})
    print(f'   Test insert ID: {result.inserted_id}')
else:
    print('❌ Database Connection: FAILED')
"
```

#### Test Content Publisher
```bash
python -c "
from modules.blog_automation.content_publisher import PublisherManager
pm = PublisherManager()
print('✅ Content Publisher: WORKING')
print('   Available publishers:', list(pm.publishers.keys()))
"
```

### 2. Course Creation Module (Ready for Module 2)

#### Test Course Generator Structure
```bash
python -c "
import sys
import os
sys.path.append('.')

# Check if course creation module exists
if os.path.exists('modules/course_creation'):
    print('✅ Course Creation Module: READY')
    print('   Location: modules/course_creation/')
else:
    print('ℹ️  Course Creation Module: PREPARING')
    print('   Will be available in Module 2')
"
```

### 3. Job Aggregation Module (Ready for Module 3)

#### Test Job Search Structure
```bash
python -c "
import sys
import os
sys.path.append('.')

if os.path.exists('modules/job_aggregation'):
    print('✅ Job Aggregation Module: READY')
    print('   Location: modules/job_aggregation/')
else:
    print('ℹ️  Job Aggregation Module: PREPARING')
    print('   Will be available in Module 3')
"
```

### 4. Full Integration Test

```bash
# Run complete example
python modules/blog_automation/example_usage.py
```

## Web Interface

### Starting the Web Interface

```bash
# Start the web interface
python start_web_interface.py

# Or manually
cd web_interface
python app.py
```

### Web Interface Features

1. **Dashboard**: Real-time status of all modules
2. **Blog Management**: Create, edit, publish blog posts
3. **Course Management**: Generate and manage courses (Module 2)
4. **Job Board**: Monitor job aggregation (Module 3)
5. **User Management**: Handle user data (Module 4)
6. **AI Chatbot**: Interactive AI assistant (Module 5)
7. **Analytics**: Performance metrics and logs
8. **Settings**: Configuration management

### Accessing the Interface

Open your browser and navigate to:
- **Local**: http://localhost:8080
- **Remote**: http://your-server-ip:8080

## VPS Deployment

### 1. Production Setup Script

Create `deploy_production.sh`:
```bash
#!/bin/bash

echo "🚀 Deploying AI Automation Agent to Production..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install production dependencies
sudo apt install python3 python3-pip python3-venv git mongodb-org mysql-server nginx -y

# Create application directory
sudo mkdir -p /opt/ai-automation-agent
sudo chown $USER:$USER /opt/ai-automation-agent

# Copy application files
cp -r . /opt/ai-automation-agent/
cd /opt/ai-automation-agent

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Create required directories
mkdir -p logs courses jobs web_interface/static web_interface/templates

# Setup database
# For MongoDB:
sudo systemctl start mongod
sudo systemctl enable mongod

# For MySQL:
sudo systemctl start mysql
sudo systemctl enable mysql

# Setup log rotation
sudo tee /etc/logrotate.d/ai-automation-agent > /dev/null <<EOF
/opt/ai-automation-agent/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

echo "✅ Production deployment completed!"
echo ""
echo "Next steps:"
echo "1. Configure .env file with your API keys"
echo "2. Set up database credentials"
echo "3. Test the installation: python test_installation.py"
echo "4. Start the web interface: python start_web_interface.py"
```

### 2. Run Deployment
```bash
chmod +x deploy_production.sh
./deploy_production.sh
```

### 3. Systemd Service Configuration

Create service file:
```bash
sudo nano /etc/systemd/system/ai-automation-agent.service
```

Add content:
```ini
[Unit]
Description=AI Automation Agent
After=network.target mongodb.service mysql.service
Requires=mongodb.service mysql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/ai-automation-agent
Environment=PATH=/opt/ai-automation-agent/venv/bin
ExecStart=/opt/ai-automation-agent/venv/bin/python start_web_interface.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ai-automation-agent

# Security settings
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-automation-agent
sudo systemctl start ai-automation-agent

# Check status
sudo systemctl status ai-automation-agent
```

### 4. Nginx Reverse Proxy (Optional)

Install and configure Nginx:
```bash
sudo apt install nginx -y

sudo nano /etc/nginx/sites-available/ai-automation-agent
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/ai-automation-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Troubleshooting

### Common Issues and Solutions

#### 1. OpenAI API Errors
**Symptoms**: Authentication errors, rate limit errors
**Solutions**:
```bash
# Check API key
echo $OPENAI_API_KEY
python -c "
from openai import OpenAI
import os
try:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'test'}],
        max_tokens=5
    )
    print('✅ OpenAI API: WORKING')
except Exception as e:
    print(f'❌ OpenAI API Error: {e}')
"
```

#### 2. Database Connection Issues

**MongoDB Problems**:
```bash
# Check MongoDB status
sudo systemctl status mongod

# Restart MongoDB
sudo systemctl restart mongod

# Check logs
sudo journalctl -u mongod -f

# Test connection
mongosh --eval "db.runCommand({connectionStatus: 1})"
```

**MySQL Problems**:
```bash
# Check MySQL status
sudo systemctl status mysql

# Check logs
sudo tail -f /var/log/mysql/error.log

# Test connection
mysql -u ai_agent -p -e "SHOW DATABASES;"
```

#### 3. Next.js Integration Issues

**API Connection Failed**:
```bash
# Test API endpoint
curl -X POST https://your-nextjs-site.com/api/blogs \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_api_key" \
  -d '{"title":"Test","content":"Test content","status":"draft"}'

# Check Next.js logs
# Check server status
curl -I https://your-nextjs-site.com
```

#### 4. Permission Issues

**Fix common permission problems**:
```bash
# Fix file permissions
chmod -R 755 ~/ai-automation-agent/
chown -R $USER:$USER ~/ai-automation-agent/

# Fix virtual environment
chmod +x ~/ai-automation-agent/venv/bin/activate

# Fix log directory
mkdir -p logs
chmod 755 logs
```

#### 5. Module Import Errors

**Common Python path issues**:
```bash
# Ensure virtual environment is activated
source ~/ai-automation-agent/venv/bin/activate

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Test imports
python -c "
import sys
print('Python path:', sys.path)
try:
    from modules.blog_automation.blog_generator import BlogGenerator
    print('✅ Modules: IMPORTED SUCCESSFULLY')
except ImportError as e:
    print(f'❌ Import Error: {e}')
"
```

### Performance Optimization

#### 1. Memory Usage Optimization
```bash
# Monitor memory usage
htop

# Reduce token limits for AI generation
# Edit .env: MAX_TOKENS=1000

# Process smaller batches
# Edit .env: BLOG_MAX_LENGTH=800
```

#### 2. Database Performance
```bash
# For MongoDB - Create indexes
mongosh
use ai_automation
db.blogs.createIndex({"createdAt": -1})
db.blogs.createIndex({"status": 1})

# For MySQL - Optimize tables
mysql -u root -p
USE ai_automation;
OPTIMIZE TABLE blogs, courses, jobs;
```

#### 3. API Rate Limiting
```bash
# Check OpenAI rate limits
# Implement exponential backoff in code
# Use draft mode for testing
```

## Migration from Previous Versions

### Migrating from Web Automation (2024) to API Integration (2025)

#### Step 1: Backup Current Installation
```bash
# Create backup
cp -r ~/ai-automation-agent ~/ai-automation-agent-backup-$(date +%Y%m%d)

# Export database
mongodump --out ~/backup-$(date +%Y%m%d)  # MongoDB
# OR
mysqldump ai_automation > ~/backup-$(date +%Y%m%d).sql  # MySQL
```

#### Step 2: Update Environment Variables

**Remove obsolete variables**:
```bash
# Remove from .env file
BROWSER_HEADLESS=true
BROWSER_TIMEOUT=30
USER_AGENT=Mozilla/5.0...
```

**Add new variables**:
```bash
# Add to .env file
NEXTJS_BLOG_API=https://your-nextjs-site.com/api/blogs
NEXTJS_API_KEY=your_secure_api_key_here
NEXTJS_API_TIMEOUT=30
BLOG_DEFAULT_STATUS=draft
```

#### Step 3: Update Code Dependencies
```bash
# Remove old dependencies
pip uninstall selenium playwright

# Install new dependencies (already in requirements.txt)
pip install -r requirements.txt
```

#### Step 4: Test Migration
```bash
# Run migration test
python test_nextjs_integration.py

# Test old functionality still works
python modules/blog_automation/example_usage.py
```

#### Step 5: Deploy Updated Version
```bash
# Stop old service
sudo systemctl stop ai-automation-agent

# Deploy new version
cp -r updated_files/* /opt/ai-automation-agent/
cd /opt/ai-automation-agent

# Install dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart service
sudo systemctl start ai-automation-agent
sudo systemctl status ai-automation-agent
```

### Migration Checklist

- [ ] ✅ Backup current installation
- [ ] ✅ Export database
- [ ] ✅ Remove obsolete environment variables
- [ ] ✅ Add new Next.js configuration variables
- [ ] ✅ Update code dependencies
- [ ] ✅ Test Next.js integration
- [ ] ✅ Test all existing functionality
- [ ] ✅ Deploy updated version
- [ ] ✅ Monitor for errors
- [ ] ✅ Rollback plan ready (backup location: `~/ai-automation-agent-backup-YYYYMMDD`)

## Security Best Practices

### 1. API Key Management
```bash
# Never commit API keys to version control
echo ".env" >> .gitignore

# Use environment-specific keys
# Development: Test keys
# Production: Live keys

# Rotate keys regularly
# Monitor for unauthorized usage
```

### 2. Database Security
```bash
# Use strong passwords
# Restrict database access to localhost only
# Enable authentication
# Regular backups
# Monitor access logs
```

### 3. Server Security
```bash
# Keep system updated
sudo apt update && sudo apt upgrade

# Configure firewall
sudo ufw enable
sudo ufw allow 22    # SSH
sudo ufw allow 8080  # Web interface

# Limit file permissions
chmod 600 .env
chmod 700 logs/
```

### 4. Monitoring and Logging
```bash
# Enable comprehensive logging
# Monitor error rates
# Set up alerts for failures
# Regular log analysis
# Performance monitoring
```

## Next Steps

After successful installation:

1. **Complete Module Setup**:
   - ✅ Module 1: Blog Automation (Complete)
   - 🔄 Module 2: Course Creation (Ready to implement)
   - 🔄 Module 3: Job Aggregation (Ready to implement)
   - 🔄 Module 4: User Data Management (Ready to implement)
   - 🔄 Module 5: AI Chatbot (Ready to implement)

2. **Customize Configuration**:
   - Set your preferred topics and content styles
   - Configure publishing schedules
   - Set up monitoring and alerts

3. **Scale Your Setup**:
   - Add more VPS instances for load balancing
   - Implement Redis for caching
   - Set up CDN for static content
   - Configure backup strategies

4. **Extend Functionality**:
   - Add custom publishing platforms
   - Integrate additional AI services
   - Create custom analytics dashboards
   - Build mobile applications

---

## Getting Help

If you encounter issues:

1. **Check Logs First**: `tail -f logs/agent.log`
2. **Run Diagnostics**: `python test_installation.py`
3. **Verify Configuration**: Double-check all environment variables
4. **Test Components**: Test each module individually
5. **Community Support**: Check documentation and examples

**Ready to continue with Module 2: Course Creation!**