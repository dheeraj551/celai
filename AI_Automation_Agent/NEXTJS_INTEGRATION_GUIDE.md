# Next.js Integration Guide

## Overview

The AI Automation Agent has been optimized for direct integration with Next.js applications using API-based publishing instead of web automation. This provides a more stable, efficient, and maintainable solution for content management.

## Key Benefits

✅ **Direct Integration**: Publish directly to your Next.js API endpoints  
✅ **No Web Automation**: Eliminates browser dependencies and complexity  
✅ **Better Performance**: Faster publishing with direct API calls  
✅ **Improved Reliability**: No flaky browser automation or DOM parsing  
✅ **Production Ready**: Robust error handling and logging  
✅ **Flexible Authentication**: Support for API keys and JWT tokens  

## What's Changed

### Before (Web Automation)
- Required Node.js installation
- Browser automation with Selenium/Playwright
- DOM parsing and element interaction
- Unreliable selectors and timing issues
- Complex debugging of browser crashes

### After (API Integration)
- Direct HTTP requests to Next.js API
- Simple authentication with headers
- JSON payload communication
- Predictable responses and status codes
- Clear error messages and logging

## Architecture

```
AI Agent → Next.js API → Your Database
    ↓           ↓            ↓
OpenAI      HTTP POST    Content
GPT API     JSON Auth    Storage
```

## Quick Setup

### 1. Configure Environment Variables

Update your `.env` file with Next.js settings:

```bash
# Primary: Next.js Integration
NEXTJS_BLOG_API=https://your-site.com/api/blogs
NEXTJS_API_KEY=your_api_key_or_jwt_token
NEXTJS_AUTH_HEADER=Authorization
NEXTJS_API_TIMEOUT=30

# Optional: Keep for legacy platforms
WORDPRESS_URL=https://yourblog.com
MEDIUM_ACCESS_TOKEN=your_medium_token
```

### 2. Next.js API Requirements

Your Next.js API should handle these endpoints:

#### Create Blog Post
```typescript
// POST /api/blogs
{
  "title": "AI-Generated Blog Post",
  "content": "Markdown or HTML content",
  "status": "draft", // or "published"
  "tags": ["ai", "automation"],
  "category": "technology",
  "ai_generated": true,
  "seo_title": "SEO Optimized Title",
  "seo_description": "Meta description",
  "metadata": {
    "source": "ai_automation_agent",
    "version": "1.0"
  }
}
```

#### Success Response
```typescript
{
  "success": true,
  "id": "blog_post_id",
  "url": "/blog/slug-url",
  "status": "draft"
}
```

#### Update Blog Post
```typescript
// PUT /api/blogs/{id}
{
  "status": "published"
}
```

### 3. Authentication Options

#### API Key Authentication
```typescript
// Environment
NEXTJS_AUTH_HEADER=X-API-Key
NEXTJS_API_KEY=your_api_key

// Request Headers
{
  "X-API-Key": "your_api_key",
  "Content-Type": "application/json"
}
```

#### JWT Token Authentication
```typescript
// Environment (Default)
NEXTJS_AUTH_HEADER=Authorization
NEXTJS_API_KEY=your_jwt_token

// Request Headers
{
  "Authorization": "Bearer your_jwt_token",
  "Content-Type": "application/json"
}
```

## Usage Examples

### Basic Blog Generation and Publishing

```python
from modules.blog_automation.content_publisher import NextJSAPIPublisher

# Initialize publisher
publisher = NextJSAPIPublisher(
    api_url="https://your-site.com/api/blogs",
    api_key="your_api_key"
)

# Generate and publish blog
blog_data = {
    "title": "The Future of AI in Content Creation",
    "content": "# AI Content Creation\n\n...",
    "tags": ["ai", "content", "technology"],
    "seo_title": "AI Content Creation: Complete Guide 2025",
    "seo_description": "Discover how AI is revolutionizing content creation..."
}

# Create as draft first (recommended)
result = publisher.create_draft(**blog_data)
if result['success']:
    print(f"✅ Draft created: {result['post_id']}")
    
    # Later, publish it
    update_result = publisher.update_post(
        post_id=result['post_id'],
        status="published"
    )
```

### Using the PublisherManager

```python
from modules.blog_automation.content_publisher import PublisherManager

# Initialize manager
manager = PublisherManager()

# Add Next.js publisher
manager.add_nextjs_publisher(
    name="my_nextjs_site",
    api_url="https://your-site.com/api/blogs",
    api_key="your_api_key"
)

# Publish to all platforms
results = manager.publish_to_all(
    title="AI Automation Blog Post",
    content="Generated content here...",
    tags=["ai", "automation"],
    platforms=["my_nextjs_site"]  # Specify platform
)

for platform, result in results.items():
    if result['success']:
        print(f"✅ {platform}: Published successfully")
    else:
        print(f"❌ {platform}: {result['error']}")
```

## Web Interface Integration

The web interface has been updated to show Next.js integration status:

- **Dashboard**: Shows `nextjs_enabled` status instead of `browser_headless`
- **Settings**: Configuration for `NEXTJS_BLOG_API` and `NEXTJS_API_KEY`
- **Monitoring**: Real-time API publishing logs and status

## Error Handling

The system provides comprehensive error handling:

### HTTP Status Codes
- **200/201**: Success
- **400**: Validation Error (check your API schema)
- **401**: Authentication failed (check API key/token)
- **429**: Rate limit exceeded (auto-retry logic available)
- **500**: Server error (check your Next.js API)

### Logging
All API calls are logged with detailed information:

```python
# Success logging
✅ Successfully published to Next.js API (ID: abc123) in 0.25s

# Error logging
❌ Bad Request: Validation failed - missing required field 'title'
❌ Unauthorized: Invalid API key or authentication
⏰ Timeout publishing to Next.js API after 30 seconds
```

## Migration from WordPress/Medium

If you're migrating from WordPress or Medium:

### Step 1: Update Environment Variables
```bash
# Old setup
WORDPRESS_URL=https://yourblog.com
WORDPRESS_USERNAME=...
WORDPRESS_PASSWORD=...

# New setup
NEXTJS_BLOG_API=https://your-new-site.com/api/blogs
NEXTJS_API_KEY=your_new_api_key
```

### Step 2: Update Code
```python
# Old approach
publisher = WordPressPublisher(...)

# New approach
publisher = NextJSAPIPublisher(
    api_url=settings.NEXTJS_BLOG_API,
    api_key=settings.NEXTJS_API_KEY
)
```

### Step 3: Test and Validate
```python
# Test with draft mode first
result = publisher.create_draft("Test Post", "Test content")
if result['success']:
    print("✅ Migration successful")
else:
    print(f"❌ Migration failed: {result['error']}")
```

## Best Practices

### 1. Start with Draft Mode
```python
# Always create drafts first for testing
draft = publisher.create_draft(title, content)
if draft['success']:
    # Review the content
    # Then publish
    publisher.update_post(draft['post_id'], status="published")
```

### 2. Use Proper Error Handling
```python
try:
    result = publisher.publish_post(...)
    if not result['success']:
        logger.error(f"Publishing failed: {result['error']}")
        # Handle the error appropriately
except Exception as e:
    logger.error(f"Unexpected error: {e}")
```

### 3. Monitor API Performance
```python
# Check response times
if 'api_response_time' in result:
    response_time = result['api_response_time']
    if response_time > 5.0:
        logger.warning(f"Slow API response: {response_time:.2f}s")
```

### 4. Implement Rate Limiting Awareness
```python
# The system automatically handles rate limits
# But you can also implement your own logic
if result['error'] == "Rate limit exceeded":
    # Wait and retry
    time.sleep(60)  # Wait 1 minute
    retry_result = publisher.publish_post(...)
```

## Troubleshooting

### Common Issues

#### 1. Authentication Failures
```
❌ Unauthorized: Invalid API key
```
**Solution**: Check your `NEXTJS_API_KEY` and `NEXTJS_AUTH_HEADER` configuration

#### 2. API Endpoint Not Found
```
Connection error to Next.js API
```
**Solution**: Verify your `NEXTJS_BLOG_API` URL is correct and accessible

#### 3. Validation Errors
```
❌ Bad Request: Validation failed
```
**Solution**: Check your Next.js API schema - ensure required fields are provided

#### 4. Timeout Issues
```
⏰ Timeout publishing after 30 seconds
```
**Solution**: Increase `NEXTJS_API_TIMEOUT` or check your API performance

### Debug Mode

Enable detailed logging for debugging:

```bash
# Environment
LOG_LEVEL=DEBUG
DETAILED_API_LOGGING=true

# Check logs
tail -f logs/agent.log
```

## Performance Optimization

### 1. Connection Pooling
The system automatically handles connection management for optimal performance.

### 2. Batch Operations
For multiple posts, consider implementing batch endpoints in your Next.js API:

```typescript
// POST /api/blogs/batch
{
  "posts": [
    {"title": "Post 1", "content": "..."},
    {"title": "Post 2", "content": "..."}
  ]
}
```

### 3. Caching
If your Next.js API supports caching headers, the agent will respect them:

```typescript
// API Response
{
  "success": true,
  "id": "post_id",
  "cache_control": "max-age=300"  // 5 minutes
}
```

## Security Considerations

### 1. API Key Security
- Store API keys in environment variables
- Use secure key rotation practices
- Consider using JWT tokens with expiration

### 2. Input Validation
Always validate input in your Next.js API:

```typescript
// Validate required fields
if (!title || !content) {
  return { error: "Missing required fields" };
}

// Sanitize content
const sanitizedContent = sanitizeHtml(content);
```

### 3. Rate Limiting
Implement rate limiting in your Next.js API:

```typescript
// Example with rate-limiter-flexible
const rateLimiter = new RateLimiterMemory({
  points: 10, // Number of requests
  duration: 60, // Per 60 seconds
});
```

## Conclusion

The Next.js integration provides a modern, reliable, and efficient solution for AI-powered content automation. By moving from web automation to API-based publishing, you gain:

- **Better Performance**: Direct API communication
- **Improved Reliability**: No browser automation issues
- **Enhanced Security**: Proper authentication and validation
- **Easier Maintenance**: Clear separation of concerns
- **Production Ready**: Comprehensive error handling and logging

For support or questions, check the logs or refer to the main documentation.

---

**Next Steps:**
1. Configure your Next.js API endpoints
2. Set up authentication
3. Test with draft mode
4. Monitor performance and logs
5. Scale up to production publishing