# Quick Start Guide - AI Automation Agent

## 🚀 Get Started in 15 Minutes

This guide gets you up and running quickly with the AI Automation Agent.

## Prerequisites Check

Before starting, ensure you have:
- [ ] VPS with Ubuntu 20.04+ (2GB RAM, 2 cores minimum)
- [ ] OpenAI API Key (required for AI functionality)
- [ ] Domain name (optional, for web interface access)
- [ ] Basic knowledge of terminal/SSH

## Step 1: System Setup (5 minutes)

```bash
# Connect to your VPS and update system
ssh ubuntu@your-server-ip
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv git curl wget -y

# Create project directory
mkdir ~/ai-automation-agent
cd ~/ai-automation-agent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
```

## Step 2: Install Agent (3 minutes)

```bash
# Copy/extract your project files here
# For example:
# git clone <your-repo-url> .

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create required directories
mkdir -p logs courses jobs web_interface/static web_interface/templates
```

## Step 3: Database Setup (3 minutes)

### Option A: MongoDB (Recommended)
```bash
# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update
sudo apt install -y mongodb-org

# Start MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Create database and user
mongosh --eval '
use ai_automation
db.createUser({
  user: "ai_agent",
  pwd: "SecurePassword123!",
  roles: ["readWrite"]
})
'
```

### Option B: MySQL
```bash
# Install MySQL
sudo apt install mysql-server mysql-client -y
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p <<EOF
CREATE DATABASE ai_automation;
CREATE USER 'ai_agent'@'localhost' IDENTIFIED BY 'SecurePassword123!';
GRANT ALL PRIVILEGES ON ai_automation.* TO 'ai_agent'@'localhost';
FLUSH PRIVILEGES;
EOF
```

## Step 4: Configure Environment (3 minutes)

```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env
```

**Required settings in .env:**
```bash
# Database (choose one)
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb://ai_agent:SecurePassword123!@localhost:27017/ai_automation

# OR for MySQL
# DATABASE_TYPE=mysql
# MYSQL_HOST=localhost
# MYSQL_PORT=3306
# MYSQL_USER=ai_agent
# MYSQL_PASSWORD=SecurePassword123!
# MYSQL_DATABASE=ai_automation

# AI Configuration (REQUIRED)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Next.js Integration (RECOMMENDED)
NEXTJS_BLOG_API=https://your-nextjs-site.com/api/blogs
NEXTJS_API_KEY=your_secure_api_key_here

# Web Interface
WEB_INTERFACE_PORT=8080
WEB_INTERFACE_HOST=0.0.0.0
```

## Step 5: Test Installation (1 minute)

```bash
# Test database connection
python -c "
from config.database import init_database
if init_database():
    print('✅ Database: Connected')
else:
    print('❌ Database: Failed')
    exit(1)
"

# Test AI generation
python -c "
from modules.blog_automation.blog_generator import BlogGenerator
gen = BlogGenerator()
blog = gen.generate_blog('AI trends', max_words=200)
print('✅ AI Generation: Working')
print(f'   Generated: {blog[\"title\"]}')
"

echo "🎉 Installation test completed!"
```

## Step 6: Start the Agent

```bash
# Start web interface
python start_web_interface.py
```

**Access your agent:**
- **Local**: http://localhost:8080
- **Remote**: http://your-server-ip:8080

## Quick Verification Checklist

After starting, verify these are working:

- [ ] **Web Interface** opens successfully
- [ ] **Database Connection** shows as connected
- [ ] **AI Generation** produces content without errors
- [ ] **Blog Creation** works in the web interface
- [ ] **Logs** show no critical errors

## Next Steps

### 1. Configure Next.js Integration
If you have a Next.js site, set up the API endpoint:

```javascript
// pages/api/blogs.js in your Next.js app
export default async function handler(req, res) {
  if (req.method === 'POST') {
    const authHeader = req.headers.authorization;
    if (authHeader !== `Bearer ${process.env.BLOG_API_KEY}`) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    // Process blog post
    const blogPost = await processBlogPost(req.body);
    res.status(201).json({ success: true, blogId: blogPost.id });
  }
  res.status(405).json({ error: 'Method not allowed' });
}
```

### 2. Set Up Automatic Scheduling

```bash
# Create cron job for blog automation
crontab -e

# Add this line to run blog generation every day at 9 AM
0 9 * * * cd /home/ubuntu/ai-automation-agent && /home/ubuntu/ai-automation-agent/venv/bin/python modules/blog_automation/blog_scheduler.py
```

### 3. Production Deployment

```bash
# Create production service
sudo nano /etc/systemd/system/ai-automation-agent.service
```

Add this content:
```ini
[Unit]
Description=AI Automation Agent
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/ai-automation-agent
Environment=PATH=/home/ubuntu/ai-automation-agent/venv/bin
ExecStart=/home/ubuntu/ai-automation-agent/venv/bin/python start_web_interface.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ai-automation-agent
sudo systemctl start ai-automation-agent
```

## Troubleshooting

### Common Issues

**"Database connection failed"**
```bash
# Check database status
sudo systemctl status mongod  # MongoDB
sudo systemctl status mysql   # MySQL

# Restart database
sudo systemctl restart mongod
```

**"OpenAI API error"**
```bash
# Verify API key is set
echo $OPENAI_API_KEY

# Test API key
python -c "
import openai
import os
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
try:
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': 'test'}],
        max_tokens=5
    )
    print('✅ OpenAI API: Working')
except Exception as e:
    print(f'❌ OpenAI API Error: {e}')
"
```

**"Permission denied"**
```bash
# Fix permissions
chmod -R 755 ~/ai-automation-agent/
chown -R ubuntu:ubuntu ~/ai-automation-agent/
```

### Get Help

1. **Check logs**: `tail -f logs/agent.log`
2. **Test components**: Run diagnostic commands above
3. **Verify settings**: Double-check .env configuration
4. **Restart services**: Database and agent

## Ready for Module 2!

Once your blog automation is working:

- **Module 2**: Course Creation will be available
- **Module 3**: Job Aggregation next
- **Module 4**: User Data Management
- **Module 5**: AI Chatbot

Each module builds on the established foundation!

---

**🎯 Goal**: Have a working AI-powered blog automation system in 15 minutes!

**📞 Need help?** Check the full `SETUP_GUIDE_UPDATED.md` for detailed troubleshooting.