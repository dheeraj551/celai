# API Reference - AI Automation Agent

## 🏁 Overview

The AI Automation Agent provides a RESTful API for blog generation, scheduling, and management. All endpoints return JSON responses and support standard HTTP status codes.

## 🔐 Authentication

Currently uses session-based authentication. Future versions will support API key authentication.

## 📋 Base URL

```
http://localhost:8000/api
```

## 🏥 Health Check

### GET `/health`

Check system health and database connectivity.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-11-23T01:33:04Z",
    "database": {
        "connected": true,
        "type": "mongodb"
    },
    "service": {
        "running": true,
        "uptime": 3600,
        "version": "1.0.0"
    }
}
```

**Status Codes:**
- `200` - Service is healthy
- `503` - Service is unhealthy

## 📝 Blog Generation

### POST `/generate-blog`

Generate a new blog post using AI.

**Request Body:**
```json
{
    "topic": "AI in healthcare",
    "max_words": 800,
    "target_audience": "healthcare professionals",
    "style": "informative",
    "tags": ["AI", "healthcare", "technology"],
    "publish_immediately": false,
    "platforms": ["nextjs"]
}
```

**Response:**
```json
{
    "success": true,
    "blog": {
        "id": "blog_123",
        "title": "The Future of AI in Healthcare: Transforming Patient Care",
        "content": "Artificial intelligence is revolutionizing healthcare...",
        "word_count": 798,
        "tags": ["AI", "healthcare", "technology"],
        "created_at": "2025-11-23T01:33:04Z",
        "status": "draft"
    },
    "metadata": {
        "generation_time": 3.2,
        "model_used": "gpt-3.5-turbo",
        "tokens_used": 1250
    }
}
```

**Parameters:**
- `topic` (string, required) - Blog post topic
- `max_words` (integer, optional) - Maximum word count (default: 800)
- `target_audience` (string, optional) - Target audience (default: "general")
- `style` (string, optional) - Writing style (default: "informative")
- `tags` (array, optional) - Blog tags
- `publish_immediately` (boolean, optional) - Whether to publish immediately
- `platforms` (array, optional) - Platforms to publish to

### POST `/generate-blog-series`

Generate a series of related blog posts.

**Request Body:**
```json
{
    "main_topic": "React Development",
    "num_posts": 5,
    "max_words_per_post": 600,
    "style": "tutorial",
    "publish_immediately": false
}
```

**Response:**
```json
{
    "success": true,
    "series": {
        "main_topic": "React Development",
        "total_posts": 5,
        "posts": [
            {
                "id": "blog_124",
                "title": "Getting Started with React: A Beginner's Guide",
                "word_count": 598
            },
            {
                "id": "blog_125", 
                "title": "React Components: Building Blocks of Modern Apps",
                "word_count": 612
            }
            // ... more posts
        ]
    }
}
```

## ⏰ Scheduling

### POST `/schedule-blog`

Schedule automatic blog generation.

**Request Body:**
```json
{
    "topics": ["AI", "Technology", "Innovation"],
    "max_words": 1000,
    "time_str": "09:00",
    "days": ["mon", "wed", "fri"],
    "publish_immediately": true,
    "platforms": ["nextjs"]
}
```

**Response:**
```json
{
    "success": true,
    "schedule": {
        "id": "schedule_123",
        "cron_expression": "0 9 * * mon,wed,fri",
        "topics": ["AI", "Technology", "Innovation"],
        "next_run": "2025-11-25T09:00:00Z",
        "status": "active"
    }
}
```

### GET `/schedules`

Get all active schedules.

**Response:**
```json
{
    "schedules": [
        {
            "id": "schedule_123",
            "type": "daily_blog_generation",
            "cron_expression": "0 9 * * mon,wed,fri",
            "next_run": "2025-11-25T09:00:00Z",
            "status": "active",
            "config": {
                "topics": ["AI", "Technology"],
                "max_words": 1000
            }
        }
    ]
}
```

### DELETE `/schedule/{schedule_id}`

Delete a scheduled job.

**Parameters:**
- `schedule_id` (string, path) - Schedule ID to delete

**Response:**
```json
{
    "success": true,
    "message": "Schedule deleted successfully"
}
```

## 📊 Performance Metrics

### GET `/performance`

Get system performance metrics.

**Response:**
```json
{
    "metrics": {
        "blogs_generated": 150,
        "blogs_published": 142,
        "success_rate": 94.7,
        "avg_generation_time": 3.2,
        "api_calls_today": 25,
        "last_generation": "2025-11-23T01:30:00Z"
    },
    "database": {
        "total_blogs": 150,
        "recent_blogs": 5,
        "collections": {
            "blog_posts": 150,
            "blog_statistics": 1
        }
    },
    "service": {
        "uptime": 86400,
        "memory_usage": "45.2MB",
        "cpu_usage": "12.5%",
        "status": "running"
    }
}
```

### GET `/logs`

Get recent service logs.

**Query Parameters:**
- `lines` (integer, query) - Number of log lines to return (default: 100)
- `level` (string, query) - Log level filter (DEBUG, INFO, WARNING, ERROR)

**Response:**
```json
{
    "logs": [
        {
            "timestamp": "2025-11-23T01:33:04Z",
            "level": "INFO",
            "message": "Blog generation completed successfully",
            "module": "blog_generator"
        },
        {
            "timestamp": "2025-11-23T01:32:45Z",
            "level": "DEBUG",
            "message": "Starting blog generation for topic: AI in healthcare",
            "module": "blog_generator"
        }
    ],
    "total_lines": 150,
    "filtered": false
}
```

## 🎯 Manual Triggers

### POST `/manual-blog`

Manually trigger blog generation (bypasses scheduler).

**Request Body:**
```json
{
    "topic": "Machine Learning Trends 2025",
    "max_words": 1200,
    "publish_immediately": false
}
```

**Response:**
```json
{
    "success": true,
    "blog": {
        "id": "blog_126",
        "title": "Machine Learning Trends 2025: What's Next?",
        "status": "generated"
    },
    "triggered_at": "2025-11-23T01:33:04Z"
}
```

### POST `/manual-series`

Manually trigger blog series generation.

**Request Body:**
```json
{
    "main_topic": "Web Development 2025",
    "num_posts": 3,
    "max_words": 800
}
```

**Response:**
```json
{
    "success": true,
    "series": {
        "main_topic": "Web Development 2025",
        "total_posts": 3,
        "posts_generated": 3
    },
    "triggered_at": "2025-11-23T01:33:04Z"
}
```

## 📈 Statistics

### GET `/statistics`

Get detailed usage statistics.

**Response:**
```json
{
    "statistics": {
        "daily": {
            "blogs_generated": 5,
            "blogs_published": 4,
            "api_calls": 25,
            "avg_generation_time": 3.1
        },
        "weekly": {
            "blogs_generated": 35,
            "blogs_published": 32,
            "api_calls": 180,
            "avg_generation_time": 3.3
        },
        "monthly": {
            "blogs_generated": 150,
            "blogs_published": 142,
            "api_calls": 750,
            "avg_generation_time": 3.2
        }
    },
    "platforms": {
        "nextjs": {
            "published": 142,
            "success_rate": 94.7
        },
        "wordpress": {
            "published": 0,
            "success_rate": 0
        }
    }
}
```

## 🔧 Configuration

### GET `/config`

Get current configuration (non-sensitive values only).

**Response:**
```json
{
    "config": {
        "database_type": "mongodb",
        "ai_model": "gpt-3.5-turbo",
        "max_tokens": 2000,
        "temperature": 0.7,
        "blog_max_length": 1500,
        "scheduler_enabled": true,
        "web_interface_enabled": true,
        "port": 8000
    }
}
```

## 📜 Error Handling

All endpoints return standard HTTP status codes:

- `200` - Success
- `400` - Bad Request (missing/invalid parameters)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found (resource doesn't exist)
- `429` - Too Many Requests (rate limit exceeded)
- `500` - Internal Server Error
- `503` - Service Unavailable

### Error Response Format

```json
{
    "error": {
        "code": "INVALID_TOPIC",
        "message": "Topic cannot be empty",
        "details": {
            "field": "topic",
            "constraint": "required"
        }
    },
    "timestamp": "2025-11-23T01:33:04Z"
}
```

### Common Error Codes

- `INVALID_TOPIC` - Topic parameter is missing or invalid
- `RATE_LIMIT_EXCEEDED` - Too many requests
- `DATABASE_CONNECTION_FAILED` - MongoDB connection error
- `AI_SERVICE_UNAVAILABLE` - OpenAI API unavailable
- `PUBLISHING_FAILED` - Failed to publish to platform
- `SCHEDULE_CONFLICT` - Schedule already exists

## 🔄 Rate Limiting

Currently no rate limiting implemented. Future versions will include:

- 100 requests per hour for blog generation
- 10 requests per minute for scheduling
- 1000 requests per hour for metrics

## 📝 Example Usage

### JavaScript/Fetch

```javascript
// Generate blog post
const response = await fetch('/api/generate-blog', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        topic: "AI in Healthcare",
        max_words: 800,
        publish_immediately: false
    })
});

const result = await response.json();
console.log(result.blog.title);
```

### Python Requests

```python
import requests

# Generate blog post
response = requests.post('http://localhost:8000/api/generate-blog', json={
    'topic': 'AI in Healthcare',
    'max_words': 800,
    'publish_immediately': False
})

if response.status_code == 200:
    blog = response.json()['blog']
    print(f"Generated: {blog['title']}")
else:
    print(f"Error: {response.json()['error']['message']}")
```

### cURL

```bash
# Generate blog post
curl -X POST http://localhost:8000/api/generate-blog \
  -H "Content-Type: application/json" \
  -d '{"topic":"AI in Healthcare","max_words":800}'

# Get performance metrics
curl http://localhost:8000/api/performance

# Schedule blog generation
curl -X POST http://localhost:8000/api/schedule-blog \
  -H "Content-Type: application/json" \
  -d '{"topics":["AI"],"time_str":"09:00","days":["mon","wed","fri"]}'
```

## 🔗 Related Documentation

- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation and configuration
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common issues and solutions
- [README.md](../README.md) - Project overview