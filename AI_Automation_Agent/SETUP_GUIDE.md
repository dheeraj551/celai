# AI Automation Agent - Complete Setup Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Initial Setup](#initial-setup)
3. [Database Configuration](#database-configuration)
4. [Environment Variables](#environment-variables)
5. [Blog Automation Module Setup](#blog-automation-module-setup)
6. [Testing Your Setup](#testing-your-setup)
7. [VPS Deployment](#vps-deployment)
8. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum VPS Requirements
- **OS**: Ubuntu 22.04 LTS
- **RAM**: 2GB minimum, 4GB recommended
- **CPU**: 2 cores minimum
- **Storage**: 20GB SSD
- **Network**: Stable internet connection

### Software Dependencies
- Python 3.8 or higher
- Git
- curl
- wget

## Initial Setup

### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Python and Development Tools
```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv python3-dev -y

# Install additional system dependencies
sudo apt install build-essential libssl-dev libffi-dev -y

# Note: Node.js is NOT required for Next.js integration
# This system uses API-based publishing instead of web automation
```

### 3. Create Project Directory
```bash
mkdir ~/ai-automation-agent
cd ~/ai-automation-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

## Database Configuration

### Option 1: MongoDB (Recommended for Beginners)

#### Install MongoDB
```bash
# Import MongoDB repository
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify installation
sudo systemctl status mongod
```

#### Configure MongoDB
```bash
# Create MongoDB user for the application
mongosh

# In MongoDB shell:
use ai_automation
db.createUser({
  user: "ai_agent",
  pwd: "your_secure_password",
  roles: ["readWrite"]
})

# Exit with exit or quit()
```

### Option 2: MySQL

#### Install MySQL
```bash
sudo apt install mysql-server mysql-client -y

# Secure MySQL installation
sudo mysql_secure_installation
```

#### Configure MySQL
```bash
# Login to MySQL
sudo mysql -u root -p

# Create database and user
CREATE DATABASE ai_automation;
CREATE USER 'ai_agent'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON ai_automation.* TO 'ai_agent'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Environment Variables

### 1. Create Environment File
```bash
cp .env.example .env
nano .env
```

### 2. Configure Database Settings

#### For MongoDB:
```bash
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb://ai_agent:your_secure_password@localhost:27017/ai_automation
```

#### For MySQL:
```bash
DATABASE_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=ai_agent
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=ai_automation
```

### 3. Configure AI Settings
```bash
# Required: Your OpenAI API key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Customize AI behavior
AI_MODEL=gpt-3.5-turbo
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### 4. Configure Blog Automation
```bash
BLOG_FREQUENCY=daily
BLOG_TOPICS=technology,ai,programming,web-development
BLOG_MAX_LENGTH=1000
BLOG_PUBLISH_TO=wordpress,medium
```

### 5. Configure Publishing Platforms

#### WordPress (if using):
```bash
WORDPRESS_URL=https://yourblog.com
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_application_password
```

**Important**: WordPress requires Application Passwords, not regular passwords:
1. Go to WordPress Admin → Users → Profile
2. Scroll to "Application Passwords"
3. Generate a new password for your application

#### Medium (if using):
```bash
MEDIUM_TOKEN=your_medium_integration_token
```

### 6. Configure Next.js Integration (Recommended)
```bash
# Next.js API endpoint for blog publishing
NEXTJS_BLOG_API=https://your-nextjs-site.com/api/blogs
# API authentication (API key or JWT token)
NEXTJS_API_KEY=your_secure_api_key_here
# API timeout settings
NEXTJS_API_TIMEOUT=30
# Default blog status (draft for testing)
BLOG_DEFAULT_STATUS=draft
```

## Blog Automation Module Setup

### 1. Test AI Generation
```bash
cd ~/ai-automation-agent
python -c "
from modules.blog_automation.blog_generator import BlogGenerator
gen = BlogGenerator()
blog = gen.generate_blog('AI in healthcare', max_words=500)
print('Title:', blog['title'])
print('Success!')
"
```

### 2. Test Database Connection
```bash
python -c "
from config.database import init_database
success = init_database()
print('Database connection:', 'SUCCESS' if success else 'FAILED')
"
```

### 3. Run Blog Automation Example
```bash
cd modules/blog_automation
python example_usage.py
```

## Testing Your Setup

### 1. Test Individual Components

#### Test Blog Generation
```bash
python -c "
from modules.blog_automation.blog_generator import BlogGenerator
from config.settings import settings

if not settings.OPENAI_API_KEY:
    print('ERROR: OPENAI_API_KEY not set')
    exit(1)

gen = BlogGenerator()
blog = gen.generate_blog('test topic', max_words=300)
print('Blog generation test: PASSED')
"
```

#### Test Database
```bash
python -c "
from config.database import init_database, get_collection
success = init_database()
if success:
    collection = get_collection('test_collection')
    result = collection.insert_one({'test': 'data'})
    print('Database test: PASSED')
else:
    print('Database test: FAILED')
"
```

#### Test Publishers (without actual publishing)
```bash
python -c "
from modules.blog_automation.content_publisher import PublisherManager
pm = PublisherManager()
print('Publisher manager test: PASSED')
print('Note: Add credentials to test actual publishing')
"
```

### 2. Full Integration Test
```bash
# Run the complete example
python modules/blog_automation/example_usage.py
```

## VPS Deployment

### 1. Create Deployment Script
```bash
nano ~/deploy_ai_agent.sh
```

Add the following content:
```bash
#!/bin/bash

echo "Deploying AI Automation Agent..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip python3-venv mongodb-org mysql-server -y

# Create application directory
sudo mkdir -p /opt/ai-automation-agent
sudo chown $USER:$USER /opt/ai-automation-agent

# Copy application files
cp -r ~/ai-automation-agent/* /opt/ai-automation-agent/
cd /opt/ai-automation-agent

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create log directory
mkdir -p logs

echo "Deployment completed!"
echo "Next steps:"
echo "1. Configure .env file"
echo "2. Set up database"
echo "3. Test the installation"
```

### 2. Make Script Executable and Run
```bash
chmod +x ~/deploy_ai_agent.sh
~/deploy_ai_agent.sh
```

### 3. Create Systemd Service (Optional)
```bash
sudo nano /etc/systemd/system/ai-automation-agent.service
```

Add service configuration:
```ini
[Unit]
Description=AI Automation Agent
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/opt/ai-automation-agent
Environment=PATH=/opt/ai-automation-agent/venv/bin
ExecStart=/opt/ai-automation-agent/venv/bin/python agent_core.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-automation-agent
sudo systemctl start ai-automation-agent
```

### 4. Setup Log Rotation
```bash
sudo nano /etc/logrotate.d/ai-automation-agent
```

Add log rotation config:
```
/opt/ai-automation-agent/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    copytruncate
}
```

## Running Your Agent

### 1. Manual Start
```bash
cd ~/ai-automation-agent
source venv/bin/activate
python modules/blog_automation/example_usage.py
```

### 2. Run Scheduler
```bash
python modules/blog_automation/blog_scheduler.py
```

### 3. Check Logs
```bash
tail -f logs/agent.log
```

## Troubleshooting

### Common Issues

#### 1. OpenAI API Errors
**Problem**: `openai.error.AuthenticationError`
**Solution**: 
```bash
# Check your API key
echo $OPENAI_API_KEY

# Verify in .env file
grep OPENAI_API_KEY .env
```

#### 2. Database Connection Failed
**Problem**: `pymongo.errors.ServerSelectionTimeoutError`
**Solution**:
```bash
# For MongoDB
sudo systemctl status mongod
sudo systemctl restart mongod

# For MySQL
sudo systemctl status mysql
sudo systemctl restart mysql
```

#### 3. Permission Errors
**Problem**: Permission denied when creating files
**Solution**:
```bash
# Fix permissions
chmod +x ~/ai-automation-agent/venv/bin/activate
chmod -R 755 ~/ai-automation-agent/
```

#### 4. Module Import Errors
**Problem**: `ModuleNotFoundError`
**Solution**:
```bash
# Ensure virtual environment is activated
source ~/ai-automation-agent/venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### 5. WordPress Publishing Failed
**Problem**: WordPress connection errors
**Solution**:
1. Verify Application Password is used (not regular password)
2. Check WordPress URL is correct
3. Ensure XML-RPC is enabled in WordPress

### Performance Issues

#### 1. High Memory Usage
**Solution**:
- Reduce `MAX_TOKENS` in settings
- Process blogs in smaller batches
- Monitor with `htop`

#### 2. Slow Blog Generation
**Solution**:
- Check internet connection
- Verify OpenAI API response times
- Reduce `max_words` parameter

#### 3. Database Performance
**Solution**:
- For MongoDB: Create indexes
- For MySQL: Optimize queries and add indexes
- Monitor database performance

### Getting Help

1. **Check Logs**: Always check `logs/agent.log` first
2. **Test Components**: Test each component individually
3. **Verify Configuration**: Double-check all environment variables
4. **Community Support**: Check the project documentation

## Security Best Practices

1. **API Keys**: Never commit API keys to version control
2. **Database**: Use strong passwords and restrict database access
3. **Updates**: Keep system and dependencies updated
4. **Monitoring**: Set up monitoring for your agent
5. **Backups**: Regularly backup your database and configuration

---

## Next Steps

After successful setup:
1. Customize topics and preferences in `.env`
2. Configure your publishing platforms
3. Set up automated scheduling
4. Monitor performance and logs
5. Extend with additional modules

Ready to proceed to **Module 2: Course Creation**!