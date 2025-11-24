# AI Automation Agent

🚀 **Intelligent Blog Automation & Content Generation System**

A powerful AI-powered automation agent for generating, scheduling, and publishing blog content with advanced scheduling capabilities, multi-platform publishing, and session-based authentication.

## ✨ Features

- 🤖 **AI-Powered Blog Generation** - Generate high-quality blog posts using OpenAI
- ⏰ **Advanced Scheduling** - Daily, weekly, and custom scheduling options
- 🌐 **Multi-Platform Publishing** - Next.js, WordPress, Medium integration
- 🔐 **Session-Based Authentication** - Secure admin session authentication
- 📊 **Real-Time Dashboard** - Monitor performance and manage content
- 🔄 **Background Service** - Runs continuously with auto-restart
- 📈 **Performance Metrics** - Track generation and publishing success rates
- 🎯 **SEO Optimization** - Built-in SEO optimization for blog posts

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB
- OpenAI API Key
- VPS/Server with root access

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-automation-agent.git
   cd ai-automation-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env.celorisdesigns
   nano .env.celorisdesigns
   ```

4. **Setup MongoDB**
   ```bash
   sudo apt update && sudo apt install mongodb
   sudo systemctl start mongodb && sudo systemctl enable mongodb
   ```

5. **Start the agent**
   ```bash
   python service_manager.py start
   ```

6. **Access dashboard**
   ```
   http://YOUR_SERVER_IP:8000
   ```

## 📁 Project Structure

```
ai-automation-agent/
├── AI_Automation_Agent/          # Main application
│   ├── config/                   # Configuration files
│   │   ├── database.py          # Database management
│   │   └── settings.py          # Application settings
│   ├── modules/                 # Core modules
│   │   ├── blog_automation/     # Blog generation & scheduling
│   │   └── content_publisher/   # Multi-platform publishing
│   ├── web_interface/           # FastAPI web interface
│   │   ├── app.py              # Main web application
│   │   ├── templates/          # HTML templates
│   │   └── static/             # CSS, JS, assets
│   ├── .env.celorisdesigns       # Environment configuration
│   └── requirements.txt         # Python dependencies
├── docs/                        # Documentation
│   ├── SETUP_GUIDE.md          # Detailed setup instructions
│   ├── API_REFERENCE.md        # API documentation
│   └── TROUBLESHOOTING.md      # Common issues & solutions
├── scripts/                     # Utility scripts
│   ├── service_manager.py      # Background service management
│   ├── start_background_service.py # Service runner
│   └── quick_fix_mysql_error.sh # MongoDB setup fix
├── tests/                       # Test files
│   ├── test_mongodb_connection.py
│   └── test_nextjs_integration.py
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
└── README.md                   # This file
```

## ⚙️ Configuration

### Environment Variables

Key configuration options in `.env.celorisdesigns`:

```bash
# Database
DATABASE_TYPE=mongodb
MONGODB_URI=mongodb://localhost:27017/ai_automation

# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-3.5-turbo

# Next.js Integration (for celorisdesigns.com)
NEXTJS_BLOG_API=https://celorisdesigns.com/api/admin/blog
NEXTJS_ADMIN_SESSION='{"id":"admin-user-id","email":"admin@celorisdesigns.com","role":"admin"}'

# Web Interface
CHATBOT_PORT=8000
SESSION_SECRET=your-session-secret
```

### Blog Settings

Configure blog generation preferences:

```bash
BLOG_MAX_LENGTH=1500
BLOG_TOPICS=design,development,technology,web-development,ui-ux,react,nextjs
BLOG_DEFAULT_STATUS=draft
ENABLE_SCHEDULER=true
```

## 🔧 Service Management

### Background Service Commands

```bash
# Start the service
python service_manager.py start

# Check service status
python service_manager.py status

# Stop the service
python service_manager.py stop

# Restart the service
python service_manager.py restart

# View service logs
python service_manager.py logs
```

### Testing

```bash
# Test MongoDB connection
python test_mongodb_connection.py

# Test Next.js integration
python test_nextjs_integration.py
```

## 🎯 Usage Examples

### Generate a Single Blog Post

```python
from modules.blog_automation.blog_generator import BlogGenerator

generator = BlogGenerator()
blog = generator.generate_blog(
    topic="AI in healthcare",
    max_words=800,
    target_audience="healthcare professionals",
    style="informative"
)
```

### Schedule Daily Blog Generation

```python
from modules.blog_automation.blog_scheduler import BlogScheduler

scheduler = BlogScheduler()
scheduler.schedule_daily_blog_generation(
    topics=["AI", "Technology", "Innovation"],
    max_words=1000,
    publish_immediately=True,
    time_str="09:00"
)
scheduler.start()
```

### Publish to Multiple Platforms

```python
from modules.blog_automation.content_publisher import PublisherManager

publisher = PublisherManager()
publisher.add_nextjs_publisher(
    name="celorisdesigns",
    api_url="https://celorisdesigns.com/api/admin/blog",
    session_data=session_data
)

results = publisher.publish_to_all(
    title="Blog Title",
    content="Blog content...",
    tags=["AI", "Technology"],
    platforms=["celorisdesigns"]
)
```

## 🔒 Security Features

- **Session-Based Authentication** - No API keys in URLs
- **Environment Variable Protection** - Sensitive data in .env files
- **PID File Management** - Secure process management
- **Error Handling** - Graceful degradation and logging
- **Rate Limiting** - Built-in API rate limiting

## 📊 Dashboard Features

- **Real-time Status** - Agent and service status monitoring
- **Blog Automation** - Generate and schedule blog posts
- **Performance Metrics** - Success rates and generation stats
- **Service Logs** - Live log viewing and filtering
- **Configuration Management** - Update settings without restart

## 🛠️ Development

### Local Development Setup

```bash
# Clone and setup
git clone https://github.com/YOUR_USERNAME/ai-automation-agent.git
cd ai-automation-agent

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Enable debug mode
export DEBUG=true
export LOG_LEVEL=DEBUG

# Run with hot reload
uvicorn web_interface.app:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_mongodb_connection.py -v

# Test with coverage
pytest tests/ --cov=AI_Automation_Agent --cov-report=html
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📋 Troubleshooting

### Common Issues

**MongoDB Connection Failed**
```bash
sudo systemctl start mongodb
sudo systemctl status mongodb
```

**Permission Denied (Service Manager)**
```bash
chmod +x service_manager.py
chmod +x start_background_service.py
```

**Web Interface Not Loading**
```bash
python service_manager.py status
python service_manager.py logs
```

**Session Authentication Error**
- Verify `NEXTJS_ADMIN_SESSION` in `.env.celorisdesigns`
- Check admin user exists in your Next.js database
- Ensure session data format matches: `{"id":"user-id","email":"email","role":"admin"}`

### Debug Mode

Enable detailed logging:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
export DETAILED_API_LOGGING=true
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** - For the powerful GPT models
- **FastAPI** - For the excellent web framework
- **MongoDB** - For the flexible database solution
- **Loguru** - For the improved logging system

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/ai-automation-agent/issues)
- **Documentation**: [Full Documentation](docs/)
- **Email**: support@yourdomain.com

---

**Made with ❤️ for automating content creation and distribution**