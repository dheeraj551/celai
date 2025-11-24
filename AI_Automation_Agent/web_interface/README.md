# AI Automation Agent - Web Interface

A modern, responsive web interface for monitoring and configuring your AI Automation Agent. Built with FastAPI, modern JavaScript, and a clean dark theme design.

## Features

### 🖥️ **Dashboard**
- **Real-time Status**: Monitor agent uptime, modules, and database connectivity
- **Quick Actions**: Generate blogs, start/stop agent, manage automation
- **Activity Feed**: Track recent agent activities and blog posts
- **Performance Charts**: Visual analytics of blog performance and engagement
- **System Metrics**: Monitor resource usage and system health

### 📝 **Blog Automation**
- **Content Management**: View, edit, and manage all generated blog posts
- **Generation Interface**: Create single posts or entire blog series
- **Scheduling**: Configure automated daily/weekly blog generation
- **Publishing Controls**: Publish to WordPress, Medium, or custom platforms
- **Content Filtering**: Filter by status, topic, date, and other criteria

### 📊 **Analytics & Reports**
- **Performance Metrics**: Track views, engagement, SEO scores
- **Platform Analytics**: Compare performance across different platforms
- **Trending Topics**: Identify popular content themes
- **SEO Analysis**: Monitor readability, performance, and accessibility scores
- **Export Reports**: Generate and download comprehensive analytics reports

### ⚙️ **Settings & Configuration**
- **Agent Settings**: Configure name, timezone, language, logging
- **Database Configuration**: MongoDB and MySQL connection management
- **AI Configuration**: OpenAI API settings, model selection, parameters
- **Blog Automation**: Topics, frequency, writing style, publishing preferences
- **Security Settings**: Rate limiting, session timeout, API access control

### 🔄 **Real-time Updates**
- **WebSocket Connection**: Live status updates and notifications
- **Auto-refresh**: Automatic data updates every few seconds
- **Push Notifications**: Toast notifications for important events
- **Connection Status**: Visual indicators for system connectivity

## Technology Stack

### Backend
- **FastAPI**: Modern Python web framework with automatic API documentation
- **WebSocket Support**: Real-time communication for live updates
- **Jinja2 Templates**: Server-side template rendering
- **CORS Support**: Cross-origin resource sharing for frontend integration

### Frontend
- **Vanilla JavaScript**: Modern ES6+ with async/await
- **CSS Grid & Flexbox**: Responsive layout system
- **Chart.js**: Interactive charts and graphs
- **Font Awesome**: Comprehensive icon library
- **Custom Components**: Reusable UI components (modals, toasts, forms)

### Styling
- **CSS Variables**: Consistent theming and easy customization
- **Dark Theme**: Professional appearance with high contrast
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern Animations**: Smooth transitions and micro-interactions

## Installation & Setup

### Prerequisites
```bash
# Ensure Python 3.8+ is installed
python --version

# Install required Python packages
pip install -r requirements.txt
```

### Configuration
1. **Update Environment Variables**:
   ```bash
   # Edit .env file
   OPENAI_API_KEY=your_openai_api_key
   DATABASE_TYPE=mongodb  # or mysql
   CHATBOT_PORT=8000
   ```

2. **Configure Database**:
   - MongoDB: Update `MONGODB_URI`
   - MySQL: Update MySQL connection settings

3. **Optional: WordPress/Medium Integration**:
   ```bash
   WORDPRESS_URL=https://yourblog.com
   MEDIUM_TOKEN=your_medium_token
   ```

### Running the Web Interface

#### Method 1: Direct Python Script
```bash
python start_web_interface.py
```

#### Method 2: Import in Python Code
```python
from web_interface.app import main
main()
```

#### Method 3: Uvicorn (Production)
```bash
uvicorn web_interface.app:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing the Interface
Open your browser and navigate to:
- **Local**: http://localhost:8000
- **Network**: http://your_server_ip:8000

## API Endpoints

### Agent Management
- `GET /api/status` - Get agent status and statistics
- `POST /api/agent/start` - Start the automation agent
- `POST /api/agent/stop` - Stop the automation agent

### Blog Automation
- `GET /api/blog/posts` - Get list of blog posts
- `POST /api/blog/generate` - Generate new blog post
- `POST /api/blog/series` - Generate blog series
- `POST /api/blog/publish` - Publish blog post
- `PUT /api/blog/update` - Update blog post
- `DELETE /api/blog/delete` - Delete blog post

### Analytics
- `GET /api/analytics/summary` - Get analytics summary
- `GET /api/analytics/trending` - Get trending topics
- `GET /api/analytics/performance` - Get performance metrics
- `GET /api/analytics/seo` - Get SEO analysis
- `GET /api/analytics/engagement` - Get engagement metrics

### Settings
- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings
- `POST /api/settings/reset` - Reset to defaults
- `POST /api/settings/test` - Test configuration

### System
- `GET /api/system/health` - System health check
- `GET /api/system/logs` - Get system logs
- `GET /api/system/metrics` - Get system metrics

## WebSocket Events

### Real-time Updates
- `agent_status` - Agent status changes
- `blog_generation` - Blog generation progress
- `blog_published` - Blog post published
- `analytics_update` - Analytics data updates
- `system_status` - System status changes
- `error_notification` - Error notifications
- `success_notification` - Success notifications

### Client Events
- `subscribe` - Subscribe to updates
- `unsubscribe` - Unsubscribe from updates
- `request_status` - Request current status
- `ping/pong` - Heartbeat for connection keepalive

## Configuration Options

### Web Interface Settings
```python
# config/settings.py
CHATBOT_PORT = 8000              # Web interface port
NEXTJS_BLOG_API = your_api_url   # Next.js API endpoint
NEXTJS_API_KEY = your_api_key    # Next.js API authentication
LOG_LEVEL = "INFO"               # Logging level
```

### UI Customization
```css
/* static/css/main.css - CSS Variables */
:root {
    --primary-color: #3b82f6;
    --bg-primary: #0f172a;
    --text-primary: #f8fafc;
    /* Customize colors to match your brand */
}
```

## Development

### Adding New Pages
1. Create template in `templates/`
2. Add route in `app.py`
3. Include navigation in `base.html`
4. Add JavaScript logic in component files

### Custom Components
```javascript
// Use existing components
const modal = Modal.create({
    title: 'Custom Modal',
    content: '<p>Custom content</p>'
});
modal.open();

const loading = loadingManager.show('Loading...');
loadingManager.hide();
```

### API Integration
```javascript
// Use the API client
const response = await API.post('/api/blog/generate', {
    topic: 'AI in Healthcare',
    max_words: 800
});
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep :8000

# Kill the process
kill -9 <PID>
```

#### WebSocket Connection Failed
- Check firewall settings
- Verify WebSocket endpoint is accessible
- Check browser developer tools for errors

#### Database Connection Issues
- Verify database is running
- Check connection string in settings
- Test database connectivity

#### Missing Dependencies
```bash
# Reinstall requirements
pip install -r requirements.txt
```

### Debug Mode
Enable debug logging:
```bash
LOG_LEVEL=DEBUG python start_web_interface.py
```

### Browser Developer Tools
- Check Network tab for API calls
- Check Console for JavaScript errors
- Check WebSocket tab for real-time communication

## Performance Optimization

### Production Deployment
1. **Use a Production Server**:
   ```bash
   gunicorn web_interface.app:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Enable Caching**:
   ```python
   from fastapi.middleware.caching import CacheMiddleware
   ```

3. **Static File Optimization**:
   - Minify CSS/JS files
   - Enable gzip compression
   - Use CDN for external resources

### Database Optimization
- Add database indexes for frequently queried fields
- Implement query result caching
- Use connection pooling

## Security Considerations

### Authentication (Future Enhancement)
```python
# Add authentication middleware
from fastapi.security import HTTPBearer
security = HTTPBearer()
```

### Rate Limiting
- Implement rate limiting for API endpoints
- Add request validation and sanitization
- Use HTTPS in production

### Environment Variables
- Never commit sensitive data to version control
- Use environment-specific configuration files
- Rotate API keys regularly

## Contributing

### Code Style
- Follow PEP 8 for Python code
- Use Prettier for JavaScript formatting
- Maintain consistent naming conventions

### File Structure
```
web_interface/
├── app.py              # Main FastAPI application
├── static/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript modules
│   └── images/        # Static images
├── templates/         # HTML templates
└── README.md         # This file
```

## License

This web interface is part of the AI Automation Agent project and follows the same license terms.

---

**Happy automating! 🤖**