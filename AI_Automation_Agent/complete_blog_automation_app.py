"""
AI Automation Agent - Complete Blog Publishing Application
With blog visibility, editing functionality, and VPS monitoring
"""
import os
import json
import time
import psutil
import asyncio
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from loguru import logger

# =============================================================================
# CONFIGURATION AND SETUP
# =============================================================================

# Setup logging
logger.remove()
logger.add(
    "logs/ai_automation.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    rotation="1 day",
    retention="7 days"
)

# Add console logging
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}",
    level="INFO"
)

app = FastAPI(title="AI Automation Agent", version="2.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# DATABASE AND STORAGE SETUP
# =============================================================================

PROJECT_ROOT = Path(__file__).parent
BLOGS_FILE = PROJECT_ROOT / "blogs.json"
DATABASE_FILE = PROJECT_ROOT / "ai_automation.db"

def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create blogs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blogs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'draft',
            platforms TEXT DEFAULT '[]',
            ai_generated BOOLEAN DEFAULT TRUE,
            nextjs_posted BOOLEAN DEFAULT FALSE,
            nextjs_id TEXT,
            nextjs_url TEXT
        )
    ''')
    
    # Create system_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT,
            message TEXT,
            details TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def load_blogs():
    """Load blogs from JSON file with SQLite fallback"""
    try:
        # Try JSON file first
        if BLOGS_FILE.exists():
            return json.loads(BLOGS_FILE.read_text())
    except Exception as e:
        logger.error(f"Error loading JSON blogs: {e}")
    
    # Fallback to SQLite
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM blogs ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        
        blogs = []
        for row in rows:
            blog = {
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'created_at': row[3],
                'status': row[4],
                'platforms': json.loads(row[5] or '[]'),
                'ai_generated': bool(row[6]),
                'nextjs_posted': bool(row[7]),
                'nextjs_id': row[8],
                'nextjs_url': row[9]
            }
            blogs.append(blog)
        return blogs
    except Exception as e:
        logger.error(f"Error loading SQLite blogs: {e}")
        return []

def save_blogs(blogs):
    """Save blogs to JSON file and SQLite"""
    try:
        # Save to JSON file
        BLOGS_FILE.write_text(json.dumps(blogs, indent=2))
    except Exception as e:
        logger.error(f"Error saving JSON blogs: {e}")
    
    # Save to SQLite
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Clear existing blogs
        cursor.execute('DELETE FROM blogs')
        
        # Insert blogs
        for blog in blogs:
            cursor.execute('''
                INSERT INTO blogs (
                    title, content, created_at, status, platforms, 
                    ai_generated, nextjs_posted, nextjs_id, nextjs_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                blog.get('title', ''),
                blog.get('content', ''),
                blog.get('created_at', datetime.now().isoformat()),
                blog.get('status', 'draft'),
                json.dumps(blog.get('platforms', [])),
                blog.get('ai_generated', True),
                blog.get('nextjs_posted', False),
                blog.get('nextjs_id'),
                blog.get('nextjs_url')
            ))
        
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error saving SQLite blogs: {e}")

def log_event(event_type: str, message: str, details: str = ""):
    """Log system events to database"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO system_logs (event_type, message, details) VALUES (?, ?, ?)',
            (event_type, message, details)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error(f"Error logging event: {e}")

# Initialize database
init_database()

# =============================================================================
# NEXT.JS INTEGRATION FOR CELORISDESIGNS.COM
# =============================================================================

# Optimized Next.js Publisher for celorisdesigns.com
class NextJSPublisher:
    """Optimized publisher for celorisdesigns.com matching admin interface"""
    
    def __init__(self):
        self.api_url = "https://celorisdesigns.com/api/admin/blog"
        self.admin_session = '{"id":"550e8400-e29b-41d4-a716-446655440000","email":"support@celorisdesigns.com","role":"admin"}'
        self.auth_header = "x-admin-session"
        
        # Available categories from admin interface
        self.categories = [
            "Technology", "Productivity", "Platform", "Design", 
            "Development", "Web Development", "AI", "Innovation"
        ]
    
    def _create_slug(self, title: str) -> str:
        """Create URL-friendly slug from title"""
        import re
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def _extract_tags(self, content: str, category: str) -> list:
        """Extract relevant tags from content and category"""
        tags = [category.lower()]
        
        # Common tech keywords
        keywords = {
            'ai': ['artificial intelligence', 'machine learning', 'ai', 'neural'],
            'react': ['react', 'javascript', 'js', 'component'],
            'nextjs': ['next.js', 'nextjs', 'framework', 'ssr'],
            'web': ['web development', 'frontend', 'html', 'css'],
            'design': ['ui', 'ux', 'design', 'interface', 'user experience'],
            'productivity': ['automation', 'efficiency', 'workflow', 'productivity'],
            'technology': ['tech', 'innovation', 'digital', 'software']
        }
        
        content_lower = content.lower()
        for tag, related_words in keywords.items():
            if any(word in content_lower for word in related_words):
                tags.append(tag)
        
        return list(set(tags))  # Remove duplicates
    
    async def publish_blog(self, title: str, content: str, status: str = "draft", 
                          category: str = "Technology", is_featured: bool = False) -> Dict:
        """Publish blog to celorisdesigns.com with exact admin interface format"""
        try:
            import requests
            
            # Extract excerpt from content (first 150 chars)
            excerpt = content[:150].strip()
            if len(content) > 150:
                excerpt += "..."
            
            # Calculate read time (assuming 200 words per minute)
            word_count = len(content.split())
            read_time_minutes = max(1, round(word_count / 200))
            
            # Format date for celorisdesigns.com
            formatted_date = datetime.now().strftime("%b %d, %Y, %I:%M %p")
            
            # Validate category
            if category not in self.categories:
                category = "Technology"  # Default fallback
            
            # Create blog post data matching the admin interface
            blog_data = {
                # Core content fields
                "title": title,
                "content": content,
                "excerpt": excerpt,
                "category": category,
                
                # Status and publication fields
                "status": status,  # "published" or "draft"
                "is_featured": is_featured,  # Star icon in interface
                
                # Author and metadata
                "author": "@MiniMax Agent",  # Matches interface format
                "read_time": f"{read_time_minutes} min",  # Format: "4 min"
                "published_date": formatted_date,  # "Nov 23, 2025, 11:53 PM"
                
                # AI generation metadata
                "ai_generated": True,
                "generated_at": datetime.now().isoformat(),
                "source": "ai_automation_agent",
                "version": "2.0",
                
                # Statistics fields (initialize to 0)
                "views": 0,
                "engagement": 0,
                
                # SEO and metadata
                "slug": self._create_slug(title),
                "tags": self._extract_tags(content, category),
                "metadata": {
                    "source": "ai_automation_agent",
                    "version": "2.0",
                    "auth_type": "session",
                    "ai_generated": True,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
            headers = {
                self.auth_header: self.admin_session,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'AI-Automation-Agent/2.0'
            }
            
            logger.info(f"Creating blog post: {title} (Category: {category}, Status: {status})")
            logger.info(f"Excerpt: {excerpt}")
            logger.info(f"Read time: {read_time_minutes} min")
            
            # Make API request
            response = requests.post(
                self.api_url, 
                json=blog_data, 
                headers=headers, 
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"✅ Successfully created blog post on celorisdesigns.com")
                logger.info(f"   ID: {result.get('id', 'unknown')}")
                logger.info(f"   Status: {result.get('status', 'unknown')}")
                logger.info(f"   URL: {result.get('url', 'unknown')}")
                
                return {
                    'success': True,
                    'platform': 'celorisdesigns.com',
                    'blog_id': result.get('id'),
                    'url': result.get('url'),
                    'status': result.get('status', status),
                    'title': title,
                    'category': category,
                    'is_featured': is_featured,
                    'read_time': f"{read_time_minutes} min",
                    'views': 0,
                    'engagement': 0,
                    'message': f'Blog post "{title}" successfully created on celorisdesigns.com',
                    'details': {
                        'category': category,
                        'status': status,
                        'is_featured': is_featured,
                        'author': '@MiniMax Agent',
                        'read_time_minutes': read_time_minutes
                    }
                }
                
            elif response.status_code == 400:
                error_msg = f"Validation error: {response.text}"
                logger.error(f"❌ {error_msg}")
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': error_msg,
                    'title': title,
                    'category': category
                }
                
            elif response.status_code == 401:
                error_msg = "Authentication failed - check admin session"
                logger.error(f"❌ {error_msg}")
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': error_msg,
                    'auth_issue': True
                }
                
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ Failed to create blog post: {error_msg}")
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': error_msg,
                    'status_code': response.status_code,
                    'title': title
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Request timeout - API may be slow"
            logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': error_msg,
                'timeout': True
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': error_msg,
                'connection_error': True
            }
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': error_msg,
                'unexpected_error': True
            }

# =============================================================================
# MODELS
# =============================================================================

class BlogPost(BaseModel):
    title: str
    content: str
    status: str = "draft"
    platforms: List[str] = ["celorisdesigns"]

class BlogUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    platforms: Optional[List[str]] = None

# =============================================================================
# WEBSOCKET CONNECTION MANAGER
# =============================================================================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

# =============================================================================
# AI BLOG GENERATION
# =============================================================================

async def generate_blog_with_ai(topic: str, length: str = "medium") -> Dict:
    """Generate blog using AI simulation"""
    
    try:
        # Simulate AI generation delay
        await asyncio.sleep(2)
        
        # AI-generated content simulation
        blog_title = f"AI-Generated: {topic.title()} - Complete Guide 2025"
        
        blog_content = f"""# {blog_title}

## Introduction

The world of {topic.lower()} is evolving rapidly in 2025. As technology continues to advance, understanding these trends becomes crucial for businesses and individuals alike.

## Key Trends and Insights

### 1. Revolutionary Developments

Recent developments in {topic.lower()} have shown remarkable progress. Industry experts are witnessing unprecedented growth and innovation in this field.

### 2. Future Implications

The implications of these changes extend far beyond the current landscape. Organizations must adapt their strategies to remain competitive.

### 3. Best Practices

Here are some essential best practices for working with {topic.lower()}:

- Stay updated with the latest developments
- Implement proper security measures
- Focus on user experience
- Maintain scalability in your approach

### 4. Implementation Strategies

Successful implementation requires careful planning and execution. Consider these key factors:

1. **Planning**: Develop a comprehensive strategy
2. **Execution**: Implement with attention to detail
3. **Monitoring**: Track performance and metrics
4. **Optimization**: Continuously improve processes

## Conclusion

The future of {topic.lower()} looks promising. By staying informed and adapting to changes, businesses can leverage these developments for competitive advantage.

*This content was generated by AI on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} using the AI Automation Agent.*

---

**Keywords**: {topic.lower()}, technology, automation, AI, innovation, 2025
**Category**: Technology & Innovation
**Reading Time**: 5 minutes"""
        
        # Determine category based on topic
        category_mapping = {
            'ai': 'AI',
            'artificial intelligence': 'AI', 
            'machine learning': 'AI',
            'react': 'Web Development',
            'javascript': 'Web Development',
            'nextjs': 'Web Development',
            'next.js': 'Web Development',
            'web development': 'Web Development',
            'frontend': 'Web Development',
            'design': 'Design',
            'ui': 'Design',
            'ux': 'Design',
            'interface': 'Design',
            'productivity': 'Productivity',
            'automation': 'Productivity',
            'efficiency': 'Productivity',
            'technology': 'Technology',
            'tech': 'Technology',
            'development': 'Development',
            'platform': 'Platform',
            'innovation': 'Innovation'
        }
        
        # Determine best matching category
        topic_lower = topic.lower()
        category = "Technology"  # Default
        
        for keyword, cat in category_mapping.items():
            if keyword in topic_lower:
                category = cat
                break
        
        # Auto-publish to celorisdesigns.com
        publisher = NextJSPublisher()
        publish_result = await publisher.publish_blog(
            blog_title, 
            blog_content, 
            status="published",  # Published immediately
            category=category,
            is_featured=False  # Start as non-featured
        )
        
        # Create blog object
        blog = {
            'id': len(load_blogs()) + 1,
            'title': blog_title,
            'content': blog_content,
            'created_at': datetime.now().isoformat(),
            'status': 'published',
            'platforms': ['celorisdesigns'],
            'ai_generated': True,
            'nextjs_posted': publish_result.get('success', False),
            'nextjs_id': publish_result.get('blog_id'),
            'nextjs_url': publish_result.get('url')
        }
        
        # Save blog
        blogs = load_blogs()
        blogs.append(blog)
        save_blogs(blogs)
        
        # Log the generation
        log_event('blog_generated', f'AI generated blog: {blog_title}', json.dumps(blog))
        
        # Broadcast to connected clients
        await manager.broadcast({
            'type': 'blog_generated',
            'blog': blog,
            'publish_result': publish_result
        })
        
        return {
            'success': True,
            'blog': blog,
            'publish_result': publish_result,
            'category': category,
            'message': f'Blog generated and {"published" if publish_result.get("success") else "failed to publish"} to celorisdesigns.com in {category} category'
        }
        
    except Exception as e:
        logger.error(f"Error generating blog: {e}")
        return {
            'success': False,
            'error': str(e)
        }

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard with blog management and VPS monitoring"""
    return HTMLResponse(content=get_dashboard_html())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "generate_blog":
                result = await generate_blog_with_ai(
                    topic=data.get("topic", "technology"),
                    length=data.get("length", "medium")
                )
                await websocket.send_json(result)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.get("/api/blog/posts")
async def get_blogs():
    """Get all blog posts"""
    blogs = load_blogs()
    return {"blogs": blogs, "count": len(blogs)}

@app.post("/api/blog/generate")
async def generate_blog(request: dict):
    """Generate a new blog post"""
    topic = request.get("topic", "technology")
    length = request.get("length", "medium")
    
    result = await generate_blog_with_ai(topic, length)
    return result

@app.get("/api/blog/{blog_id}")
async def get_blog(blog_id: int):
    """Get specific blog post"""
    blogs = load_blogs()
    blog = next((b for b in blogs if b.get('id') == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@app.put("/api/blog/{blog_id}")
async def update_blog(blog_id: int, update: BlogUpdate):
    """Update blog post"""
    blogs = load_blogs()
    blog_index = next((i for i, b in enumerate(blogs) if b.get('id') == blog_id), None)
    
    if blog_index is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    # Update blog
    blog = blogs[blog_index]
    if update.title is not None:
        blog['title'] = update.title
    if update.content is not None:
        blog['content'] = update.content
    if update.status is not None:
        blog['status'] = update.status
    if update.platforms is not None:
        blog['platforms'] = update.platforms
    
    blog['updated_at'] = datetime.now().isoformat()
    blogs[blog_index] = blog
    save_blogs(blogs)
    
    # Log the update
    log_event('blog_updated', f'Blog updated: {blog["title"]}', json.dumps(blog))
    
    return {"success": True, "blog": blog}

@app.delete("/api/blog/{blog_id}")
async def delete_blog(blog_id: int):
    """Delete blog post"""
    blogs = load_blogs()
    blog_index = next((i for i, b in enumerate(blogs) if b.get('id') == blog_id), None)
    
    if blog_index is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    deleted_blog = blogs.pop(blog_index)
    save_blogs(blogs)
    
    # Log the deletion
    log_event('blog_deleted', f'Blog deleted: {deleted_blog["title"]}')
    
    return {"success": True, "message": "Blog deleted"}

@app.get("/api/system/resources")
async def system_resources():
    """Get VPS system resources"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory usage
        memory = psutil.virtual_memory()
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        # System uptime
        boot_time = psutil.boot_time()
        uptime = time.time() - boot_time
        
        # Process information
        process_count = len(psutil.pids())
        
        return {
            "cpu": {
                "percent": cpu_percent,
                "count": cpu_count,
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
            },
            "memory": {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used,
                "free": memory.free
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            },
            "uptime": {
                "seconds": uptime,
                "formatted": str(datetime.fromtimestamp(boot_time))
            },
            "processes": process_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting system resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system/logs")
async def get_system_logs(limit: int = 50):
    """Get recent system logs"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM system_logs ORDER BY timestamp DESC LIMIT ?',
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                'id': row[0],
                'timestamp': row[1],
                'event_type': row[2],
                'message': row[3],
                'details': row[4]
            })
        
        return {"logs": logs}
    except Exception as e:
        logger.error(f"Error getting system logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# DASHBOARD HTML TEMPLATE
# =============================================================================

def get_dashboard_html():
    """Generate the main dashboard HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Automation Agent Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .loading { animation: spin 1s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        .metric-card { transition: all 0.3s ease; }
        .metric-card:hover { transform: translateY(-2px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    </style>
</head>
<body class="bg-gray-50">
    <div class="min-h-screen" x-data="dashboard()">
        <!-- Header -->
        <header class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center h-16">
                    <div class="flex items-center">
                        <i class="fas fa-robot text-blue-600 text-2xl mr-3"></i>
                        <h1 class="text-xl font-semibold text-gray-900">AI Automation Agent</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-sm text-gray-500" x-text="`Last updated: ${new Date().toLocaleTimeString()}`"></span>
                        <div class="w-3 h-3 rounded-full" :class="connectionStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'"></div>
                    </div>
                </div>
            </div>
        </header>

        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- VPS Monitoring Section -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">
                    <i class="fas fa-server text-blue-600 mr-2"></i>VPS System Monitoring
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <!-- CPU Usage -->
                    <div class="metric-card bg-white p-6 rounded-lg shadow border-l-4 border-l-blue-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm font-medium text-gray-600">CPU Usage</p>
                                <p class="text-3xl font-bold text-gray-900" x-text="`${systemResources.cpu?.percent || 0}%`"></p>
                            </div>
                            <i class="fas fa-microchip text-blue-500 text-2xl"></i>
                        </div>
                        <div class="mt-4">
                            <div class="bg-gray-200 rounded-full h-2">
                                <div class="bg-blue-500 h-2 rounded-full transition-all duration-500" 
                                     :style="`width: ${systemResources.cpu?.percent || 0}%`"></div>
                            </div>
                            <p class="text-xs text-gray-500 mt-1" x-text="`${systemResources.cpu?.count || 0} cores`"></p>
                        </div>
                    </div>

                    <!-- Memory Usage -->
                    <div class="metric-card bg-white p-6 rounded-lg shadow border-l-4 border-l-green-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm font-medium text-gray-600">Memory Usage</p>
                                <p class="text-3xl font-bold text-gray-900" x-text="`${systemResources.memory?.percent || 0}%`"></p>
                            </div>
                            <i class="fas fa-memory text-green-500 text-2xl"></i>
                        </div>
                        <div class="mt-4">
                            <div class="bg-gray-200 rounded-full h-2">
                                <div class="bg-green-500 h-2 rounded-full transition-all duration-500" 
                                     :style="`width: ${systemResources.memory?.percent || 0}%`"></div>
                            </div>
                            <p class="text-xs text-gray-500 mt-1" 
                               x-text="`${formatBytes(systemResources.memory?.used || 0)} / ${formatBytes(systemResources.memory?.total || 0)}`"></p>
                        </div>
                    </div>

                    <!-- Disk Usage -->
                    <div class="metric-card bg-white p-6 rounded-lg shadow border-l-4 border-l-yellow-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm font-medium text-gray-600">Disk Usage</p>
                                <p class="text-3xl font-bold text-gray-900" x-text="`${systemResources.disk?.percent || 0}%`"></p>
                            </div>
                            <i class="fas fa-hdd text-yellow-500 text-2xl"></i>
                        </div>
                        <div class="mt-4">
                            <div class="bg-gray-200 rounded-full h-2">
                                <div class="bg-yellow-500 h-2 rounded-full transition-all duration-500" 
                                     :style="`width: ${systemResources.disk?.percent || 0}%`"></div>
                            </div>
                            <p class="text-xs text-gray-500 mt-1" 
                               x-text="`${formatBytes(systemResources.disk?.used || 0)} / ${formatBytes(systemResources.disk?.total || 0)}`"></p>
                        </div>
                    </div>

                    <!-- System Uptime -->
                    <div class="metric-card bg-white p-6 rounded-lg shadow border-l-4 border-l-purple-500">
                        <div class="flex items-center justify-between">
                            <div>
                                <p class="text-sm font-medium text-gray-600">System Uptime</p>
                                <p class="text-lg font-bold text-gray-900" x-text="formatUptime(systemResources.uptime?.seconds || 0)"></p>
                            </div>
                            <i class="fas fa-clock text-purple-500 text-2xl"></i>
                        </div>
                        <div class="mt-4">
                            <p class="text-xs text-gray-500">Since: <span x-text="new Date(systemResources.uptime?.formatted || Date.now()).toLocaleDateString()"></span></p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Blog Generation Section -->
            <div class="mb-8">
                <h2 class="text-2xl font-bold text-gray-900 mb-6">
                    <i class="fas fa-pen-fancy text-green-600 mr-2"></i>AI Blog Generator
                </h2>
                <div class="bg-white p-6 rounded-lg shadow">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Blog Topic</label>
                            <input type="text" x-model="newBlog.topic" 
                                   placeholder="e.g., AI, React, Next.js, Web Development"
                                   class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Content Length</label>
                            <select x-model="newBlog.length" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                <option value="short">Short (500 words)</option>
                                <option value="medium" selected>Medium (1000 words)</option>
                                <option value="long">Long (1500+ words)</option>
                            </select>
                        </div>
                        <div class="flex items-end">
                            <button @click="generateBlog()" 
                                    :disabled="generating"
                                    class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center">
                                <i class="fas fa-robot mr-2"></i>
                                <span x-show="!generating">Generate Blog</span>
                                <i class="fas fa-spinner loading mr-2" x-show="generating"></i>
                                <span x-show="generating">Generating...</span>
                            </button>
                        </div>
                    </div>
                    
                    <div class="mt-4 p-4 bg-blue-50 rounded-md" x-show="lastGenerationResult">
                        <h4 class="font-medium text-blue-900 mb-2">Generation Result:</h4>
                        <p class="text-blue-800" x-text="lastGenerationResult"></p>
                    </div>
                </div>
            </div>

            <!-- Blog Posts Section -->
            <div class="mb-8">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-gray-900">
                        <i class="fas fa-blog text-purple-600 mr-2"></i>Blog Posts
                        <span class="text-sm font-normal text-gray-500 ml-2" x-text="`(${blogs.length} posts)`"></span>
                    </h2>
                    <button @click="loadBlogs()" 
                            class="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700">
                        <i class="fas fa-sync-alt mr-2"></i>Refresh
                    </button>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
                    <template x-for="blog in blogs" :key="blog.id">
                        <div class="bg-white rounded-lg shadow-md border hover:shadow-lg transition-shadow">
                            <div class="p-6">
                                <div class="flex justify-between items-start mb-4">
                                    <h3 class="text-lg font-semibold text-gray-900 line-clamp-2" x-text="blog.title"></h3>
                                    <span class="px-2 py-1 text-xs font-medium rounded-full"
                                          :class="blog.status === 'published' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
                                          x-text="blog.status"></span>
                                </div>
                                
                                <p class="text-gray-600 text-sm mb-4 line-clamp-3" x-text="blog.content.substring(0, 150) + '...'"></p>
                                
                                <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
                                    <span x-text="new Date(blog.created_at).toLocaleDateString()"></span>
                                    <div class="flex items-center space-x-2">
                                        <span class="flex items-center" 
                                              :class="blog.nextjs_posted ? 'text-green-600' : 'text-red-600'">
                                            <i class="fas" 
                                               :class="blog.nextjs_posted ? 'fa-check-circle' : 'fa-times-circle'"></i>
                                            <span class="ml-1" x-text="blog.nextjs_posted ? 'celorisdesigns.com' : 'Not published'"></span>
                                        </span>
                                    </div>
                                </div>
                                
                                <div class="flex space-x-2">
                                    <button @click="editBlog(blog)" 
                                            class="flex-1 bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 text-sm">
                                        <i class="fas fa-edit mr-1"></i>Edit
                                    </button>
                                    <button @click="deleteBlog(blog.id)" 
                                            class="bg-red-600 text-white px-3 py-2 rounded-md hover:bg-red-700 text-sm">
                                        <i class="fas fa-trash mr-1"></i>Delete
                                    </button>
                                </div>
                            </div>
                        </div>
                    </template>
                </div>

                <!-- Empty State -->
                <div class="text-center py-12" x-show="blogs.length === 0">
                    <i class="fas fa-blog text-gray-300 text-6xl mb-4"></i>
                    <h3 class="text-lg font-medium text-gray-900 mb-2">No blog posts yet</h3>
                    <p class="text-gray-500">Generate your first AI-powered blog post to get started.</p>
                </div>
            </div>
        </div>

        <!-- Edit Blog Modal -->
        <div class="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center p-4" 
             x-show="showEditModal" 
             x-transition:enter="transition ease-out duration-300"
             x-transition:enter-start="opacity-0 transform scale-95"
             x-transition:enter-end="opacity-100 transform scale-100"
             x-transition:leave="transition ease-in duration-200"
             x-transition:leave-start="opacity-100 transform scale-100"
             x-transition:leave-end="opacity-0 transform scale-95">
            <div class="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <div class="p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg font-semibold text-gray-900">Edit Blog Post</h3>
                        <button @click="showEditModal = false" class="text-gray-400 hover:text-gray-600">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <form @submit.prevent="saveBlog()">
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
                                <input type="text" x-model="editingBlog.title" 
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Content</label>
                                <textarea x-model="editingBlog.content" rows="10"
                                          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"></textarea>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
                                <select x-model="editingBlog.status" 
                                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                                    <option value="draft">Draft</option>
                                    <option value="published">Published</option>
                                </select>
                            </div>
                            
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Platforms</label>
                                <input type="text" x-model="editingBlog.platforms" 
                                       placeholder="celorisdesigns, wordpress, medium"
                                       class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                            </div>
                        </div>
                        
                        <div class="flex justify-end space-x-3 mt-6">
                            <button type="button" @click="showEditModal = false" 
                                    class="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50">
                                Cancel
                            </button>
                            <button type="submit" 
                                    :disabled="saving"
                                    class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50">
                                <span x-show="!saving">Save Changes</span>
                                <i class="fas fa-spinner loading mr-2" x-show="saving"></i>
                                <span x-show="saving">Saving...</span>
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script>
        function dashboard() {
            return {
                connectionStatus: 'connecting',
                blogs: [],
                generating: false,
                saving: false,
                showEditModal: false,
                editingBlog: {},
                lastGenerationResult: '',
                systemResources: {
                    cpu: { percent: 0, count: 0 },
                    memory: { percent: 0, total: 0, used: 0 },
                    disk: { percent: 0, total: 0, used: 0 },
                    uptime: { seconds: 0, formatted: '' }
                },
                newBlog: {
                    topic: '',
                    length: 'medium'
                },

                init() {
                    this.connectWebSocket();
                    this.loadBlogs();
                    this.loadSystemResources();
                    setInterval(() => this.loadSystemResources(), 10000); // Update every 10 seconds
                },

                connectWebSocket() {
                    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                    const wsUrl = `${protocol}//${window.location.host}/ws`;
                    
                    const ws = new WebSocket(wsUrl);
                    
                    ws.onopen = () => {
                        this.connectionStatus = 'connected';
                        console.log('WebSocket connected');
                    };
                    
                    ws.onclose = () => {
                        this.connectionStatus = 'disconnected';
                        setTimeout(() => this.connectWebSocket(), 5000); // Reconnect after 5 seconds
                    };
                    
                    ws.onmessage = (event) => {
                        const data = JSON.parse(event.data);
                        console.log('WebSocket message:', data);
                        
                        if (data.type === 'blog_generated') {
                            this.blogs.unshift(data.blog);
                            this.lastGenerationResult = data.publish_result.success ? 
                                'Blog generated and published to celorisdesigns.com!' : 
                                `Blog generated but failed to publish to celorisdesigns.com: ${data.publish_result.error}`;
                        }
                    };
                    
                    // Store the WebSocket instance
                    this.ws = ws;
                },

                async loadBlogs() {
                    try {
                        const response = await fetch('/api/blog/posts');
                        const data = await response.json();
                        this.blogs = data.blogs || [];
                    } catch (error) {
                        console.error('Error loading blogs:', error);
                    }
                },

                async loadSystemResources() {
                    try {
                        const response = await fetch('/api/system/resources');
                        this.systemResources = await response.json();
                    } catch (error) {
                        console.error('Error loading system resources:', error);
                    }
                },

                async generateBlog() {
                    if (!this.newBlog.topic.trim()) {
                        alert('Please enter a blog topic');
                        return;
                    }
                    
                    this.generating = true;
                    this.lastGenerationResult = '';
                    
                    try {
                        const response = await fetch('/api/blog/generate', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(this.newBlog)
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            this.blogs.unshift(result.blog);
                            this.newBlog.topic = '';
                            this.lastGenerationResult = result.message;
                        } else {
                            alert('Error generating blog: ' + result.error);
                        }
                    } catch (error) {
                        console.error('Error generating blog:', error);
                        alert('Error generating blog. Please try again.');
                    } finally {
                        this.generating = false;
                    }
                },

                editBlog(blog) {
                    this.editingBlog = { ...blog };
                    this.editingBlog.platforms = blog.platforms.join(', ');
                    this.showEditModal = true;
                },

                async saveBlog() {
                    this.saving = true;
                    
                    try {
                        const response = await fetch(`/api/blog/${this.editingBlog.id}`, {
                            method: 'PUT',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                title: this.editingBlog.title,
                                content: this.editingBlog.content,
                                status: this.editingBlog.status,
                                platforms: this.editingBlog.platforms.split(',').map(p => p.trim()).filter(p => p)
                            })
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            const index = this.blogs.findIndex(b => b.id === this.editingBlog.id);
                            if (index !== -1) {
                                this.blogs[index] = result.blog;
                            }
                            this.showEditModal = false;
                        } else {
                            alert('Error saving blog: ' + result.error);
                        }
                    } catch (error) {
                        console.error('Error saving blog:', error);
                        alert('Error saving blog. Please try again.');
                    } finally {
                        this.saving = false;
                    }
                },

                async deleteBlog(blogId) {
                    if (!confirm('Are you sure you want to delete this blog post?')) {
                        return;
                    }
                    
                    try {
                        const response = await fetch(`/api/blog/${blogId}`, {
                            method: 'DELETE'
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            this.blogs = this.blogs.filter(b => b.id !== blogId);
                        } else {
                            alert('Error deleting blog: ' + result.error);
                        }
                    } catch (error) {
                        console.error('Error deleting blog:', error);
                        alert('Error deleting blog. Please try again.');
                    }
                },

                formatBytes(bytes) {
                    if (bytes === 0) return '0 Bytes';
                    const k = 1024;
                    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                },

                formatUptime(seconds) {
                    const days = Math.floor(seconds / 86400);
                    const hours = Math.floor((seconds % 86400) / 3600);
                    const minutes = Math.floor((seconds % 3600) / 60);
                    
                    if (days > 0) {
                        return `${days}d ${hours}h ${minutes}m`;
                    } else if (hours > 0) {
                        return `${hours}h ${minutes}m`;
                    } else {
                        return `${minutes}m`;
                    }
                }
            }
        }
    </script>
</body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
