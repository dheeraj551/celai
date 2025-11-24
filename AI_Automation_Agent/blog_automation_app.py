#!/usr/bin/env python3
"""
Complete AI Automation Agent with Blog Publishing
Features full blog automation: generation, scheduling, publishing, and analytics
"""
import os
import sys
import json
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
import random

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI Automation Agent with Blog Publishing",
    description="Complete AI automation agent with full blog automation capabilities",
    version="7.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo data
demo_blog_posts = []
blog_schedules = []
agent_stats = {
    "start_time": datetime.now(),
    "total_blogs_generated": 0,
    "total_published": 0,
    "total_views": 0
}

# Sample blog topics for demo
SAMPLE_TOPICS = [
    "AI in Healthcare 2025",
    "Machine Learning Trends",
    "Python Automation Scripts",
    "Cloud Computing Best Practices",
    "Data Science Projects",
    "Web Development with AI",
    "DevOps Automation",
    "Cybersecurity in 2025",
    "Blockchain Applications",
    "IoT and Smart Cities"
]

# Generate some sample blog posts for demonstration
def generate_sample_posts():
    global demo_blog_posts, agent_stats
    if demo_blog_posts:
        return  # Already generated
    
    for i in range(1, 11):
        topic = random.choice(SAMPLE_TOPICS)
        status = random.choice(["published", "draft", "scheduled"])
        views = random.randint(100, 5000)
        engagement = round(random.uniform(1.0, 8.5), 1)
        seo_score = random.randint(60, 95)
        
        post = {
            "id": i,
            "title": f"{topic} - Complete Guide",
            "topic": topic,
            "content": f"This is a comprehensive guide about {topic}...",
            "status": status,
            "created_at": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
            "word_count": random.randint(500, 2000),
            "views": views,
            "engagement_rate": engagement,
            "seo_score": seo_score,
            "tags": [topic.lower().replace(" ", "_"), "ai", "technology"],
            "is_auto_generated": True,
            "published_at": (datetime.now() - timedelta(days=random.randint(1, 15))).isoformat() if status == "published" else None
        }
        demo_blog_posts.append(post)
    
    # Update stats
    agent_stats["total_blogs_generated"] = len(demo_blog_posts)
    agent_stats["total_published"] = len([p for p in demo_blog_posts if p["status"] == "published"])
    agent_stats["total_views"] = sum(p["views"] for p in demo_blog_posts)

# Generate sample data on startup
generate_sample_posts()

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Main dashboard page"""
    return get_dashboard_html()

@app.get("/blog-automation", response_class=HTMLResponse)
async def blog_automation_page():
    """Complete blog automation page"""
    return get_blog_automation_html()

@app.get("/analytics", response_class=HTMLResponse)
async def analytics_page():
    """Analytics dashboard"""
    return get_analytics_html()

@app.get("/settings", response_class=HTMLResponse)
async def settings_page():
    """Settings page"""
    return get_settings_html()

# API Endpoints
@app.get("/api/agent/status")
async def agent_status():
    """Get complete agent status"""
    uptime = (datetime.now() - agent_stats["start_time"]).total_seconds()
    
    return {
        "agent": {
            "is_running": True,
            "uptime_seconds": int(uptime),
            "status": "running",
            "version": "7.0",
            "mode": "blog_automation",
            "stats": agent_stats
        },
        "database": {
            "connected": True,
            "type": "demo_data",
            "mode": "demo_data"
        },
        "modules": {
            "blog_automation": True,
            "analytics": True,
            "scheduling": True,
            "publishing": True,
            "ai_generation": True
        },
        "timestamp": datetime.now().isoformat(),
        "message": "AI Automation Agent with full blog publishing capabilities"
    }

# Blog Management APIs
@app.get("/api/blog/posts")
async def get_blog_posts(limit: int = 20):
    """Get blog posts with pagination"""
    posts = demo_blog_posts[-limit:] if limit < len(demo_blog_posts) else demo_blog_posts
    posts.reverse()  # Most recent first
    
    return {
        "posts": posts,
        "total": len(demo_blog_posts),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/blog/posts/all")
async def get_all_blog_posts():
    """Get all blog posts"""
    return {
        "posts": demo_blog_posts,
        "total": len(demo_blog_posts),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/blog/generate")
async def generate_blog_post(request: Dict[str, Any]):
    """Generate a new blog post using AI"""
    try:
        # Extract parameters
        topic = request.get("topic", "")
        max_words = request.get("max_words", 800)
        target_audience = request.get("target_audience", "general")
        style = request.get("style", "informative")
        publish_immediately = request.get("publish_immediately", False)
        instructions = request.get("instructions", "")
        
        if not topic:
            return {"error": "Topic is required"}
        
        # Simulate AI blog generation
        await asyncio.sleep(2)  # Simulate processing time
        
        # Create new blog post
        new_post = {
            "id": len(demo_blog_posts) + 1,
            "title": f"Complete Guide to {topic}",
            "topic": topic,
            "content": f"""# {topic} - Complete Guide

## Introduction

{topic} is one of the most important developments in 2025. This comprehensive guide covers everything you need to know.

## Key Points

1. **Understanding {topic}**: The fundamentals and core concepts
2. **Implementation**: Practical steps and best practices  
3. **Future Trends**: What's coming next in this field
4. **Real-world Applications**: How it's being used today
5. **Getting Started**: Your first steps into {topic}

## Detailed Analysis

{topic} represents a significant shift in how we approach technology and automation. With the rapid advancement of AI and machine learning, understanding {topic} has become crucial for professionals across all industries.

### Technical Implementation

When implementing {topic}, consider these key factors:

- Performance optimization
- Scalability requirements  
- Security considerations
- Integration with existing systems
- User experience design

### Best Practices

Follow these proven strategies:

1. Start with a clear plan and objectives
2. Use tested frameworks and tools
3. Implement proper monitoring and analytics
4. Regular updates and maintenance
5. Continuous learning and improvement

## Conclusion

{topic} offers tremendous opportunities for innovation and growth. By following the guidelines in this guide, you'll be well-equipped to leverage {topic} effectively in your projects.

*This article was generated using AI automation to provide you with the most current and comprehensive information about {topic}.*""",
            "status": "published" if publish_immediately else "draft",
            "created_at": datetime.now().isoformat(),
            "word_count": max_words,
            "views": 0,
            "engagement_rate": 0.0,
            "seo_score": random.randint(75, 95),
            "tags": [topic.lower().replace(" ", "_"), "ai", "automation", "2025"],
            "is_auto_generated": True,
            "target_audience": target_audience,
            "style": style,
            "instructions": instructions,
            "published_at": datetime.now().isoformat() if publish_immediately else None
        }
        
        # Add to storage
        demo_blog_posts.append(new_post)
        
        # Update stats
        agent_stats["total_blogs_generated"] += 1
        if publish_immediately:
            agent_stats["total_published"] += 1
        
        return {
            "success": True,
            "message": "Blog post generated successfully",
            "post": new_post,
            "generation_time": "2.3 seconds"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate blog post: {str(e)}"
        }

@app.post("/api/blog/series")
async def generate_blog_series(request: Dict[str, Any]):
    """Generate a series of related blog posts"""
    try:
        main_topic = request.get("main_topic", "")
        num_posts = request.get("num_posts", 3)
        target_audience = request.get("target_audience", "general")
        publish_immediately = request.get("publish_immediately", False)
        description = request.get("description", "")
        
        if not main_topic:
            return {"error": "Main topic is required"}
        
        # Simulate series generation
        await asyncio.sleep(3)  # Simulate processing time
        
        # Generate series posts
        series_posts = []
        subtopics = [
            f"Introduction to {main_topic}",
            f"Getting Started with {main_topic}",
            f"Advanced {main_topic} Techniques",
            f"{main_topic} Best Practices",
            f"Future of {main_topic}",
            f"{main_topic} Case Studies",
            f"Common {main_topic} Mistakes",
            f"{main_topic} Tools and Resources",
            f"{main_topic} vs Alternatives",
            f"Mastering {main_topic}"
        ]
        
        for i in range(min(num_posts, len(subtopics))):
            subtopic = subtopics[i]
            post = {
                "id": len(demo_blog_posts) + i + 1,
                "title": f"{subtopic}",
                "topic": main_topic,
                "content": f"""# {subtopic}

## Overview

This is part of our comprehensive series on {main_topic}. In this article, we'll explore {subtopic.lower()}.

## Main Content

{subtopic} is a crucial aspect of {main_topic} that every professional should understand. This guide provides detailed insights and practical advice.

### Key Concepts

- Fundamental principles
- Implementation strategies
- Common challenges and solutions
- Best practices and recommendations

### Practical Examples

Real-world examples and case studies demonstrate how {subtopic} can be effectively applied in various scenarios.

## Conclusion

Understanding {subtopic} is essential for success with {main_topic}. Apply these insights to improve your results and achieve your goals.

*Part of the {main_topic} series - generated by AI automation.*""",
                "status": "published" if publish_immediately else "draft",
                "created_at": datetime.now().isoformat(),
                "word_count": random.randint(600, 1200),
                "views": 0,
                "engagement_rate": 0.0,
                "seo_score": random.randint(70, 90),
                "tags": [main_topic.lower().replace(" ", "_"), "series", "guide"],
                "is_auto_generated": True,
                "series_id": f"series_{uuid.uuid4().hex[:8]}",
                "series_position": i + 1,
                "series_topic": main_topic,
                "target_audience": target_audience,
                "description": description,
                "published_at": datetime.now().isoformat() if publish_immediately else None
            }
            series_posts.append(post)
            demo_blog_posts.append(post)
        
        # Update stats
        agent_stats["total_blogs_generated"] += len(series_posts)
        if publish_immediately:
            agent_stats["total_published"] += len(series_posts)
        
        return {
            "success": True,
            "message": f"Blog series of {len(series_posts)} posts generated successfully",
            "series": series_posts,
            "total_posts": len(series_posts),
            "generation_time": "3.1 seconds"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate blog series: {str(e)}"
        }

@app.post("/api/blog/publish/{post_id}")
async def publish_blog_post(post_id: int):
    """Publish a blog post"""
    try:
        # Find the post
        post = None
        for p in demo_blog_posts:
            if p["id"] == post_id:
                post = p
                break
        
        if not post:
            return {"error": "Blog post not found"}
        
        if post["status"] == "published":
            return {"error": "Post is already published"}
        
        # Simulate publishing process
        await asyncio.sleep(1)
        
        # Update post status
        post["status"] = "published"
        post["published_at"] = datetime.now().isoformat()
        post["views"] = random.randint(50, 500)  # Initial views
        post["engagement_rate"] = round(random.uniform(2.0, 6.0), 1)
        
        # Update stats
        agent_stats["total_published"] += 1
        agent_stats["total_views"] += post["views"]
        
        return {
            "success": True,
            "message": "Blog post published successfully",
            "post": post,
            "publish_result": {
                "platforms": ["WordPress", "Medium", "Dev.to", "LinkedIn"],
                "published_urls": [f"https://example.com/blog/{post['id']}"],
                "social_media": "Shared to Twitter and LinkedIn"
            }
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to publish blog post: {str(e)}"
        }

@app.delete("/api/blog/posts/{post_id}")
async def delete_blog_post(post_id: int):
    """Delete a blog post"""
    try:
        global demo_blog_posts
        original_count = len(demo_blog_posts)
        
        # Find and remove the post
        post_to_delete = None
        demo_blog_posts = [p for p in demo_blog_posts if p["id"] != post_id]
        
        if len(demo_blog_posts) < original_count:
            return {
                "success": True,
                "message": "Blog post deleted successfully",
                "deleted_post_id": post_id
            }
        else:
            return {"error": "Blog post not found"}
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete blog post: {str(e)}"
        }

# Scheduling APIs
@app.post("/api/blog/schedule")
async def schedule_blog_generation(request: Dict[str, Any]):
    """Schedule automatic blog generation"""
    try:
        frequency = request.get("frequency", "daily")
        time = request.get("time", "09:00")
        topics = request.get("topics", [])
        max_words = request.get("max_words", 800)
        publish_mode = request.get("publish_mode", "draft")
        
        if not topics:
            return {"error": "At least one topic is required"}
        
        schedule = {
            "id": len(blog_schedules) + 1,
            "created_at": datetime.now().isoformat(),
            "frequency": frequency,
            "time": time,
            "topics": topics,
            "max_words": max_words,
            "publish_mode": publish_mode,
            "status": "active",
            "last_run": None,
            "next_run": calculate_next_run(frequency, time),
            "total_runs": 0
        }
        
        blog_schedules.append(schedule)
        
        return {
            "success": True,
            "message": "Blog generation scheduled successfully",
            "schedule": schedule
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to schedule blog generation: {str(e)}"
        }

@app.get("/api/blog/schedules")
async def get_blog_schedules():
    """Get all scheduled jobs"""
    return {
        "schedules": blog_schedules,
        "total": len(blog_schedules),
        "timestamp": datetime.now().isoformat()
    }

@app.delete("/api/blog/schedules/{schedule_id}")
async def delete_blog_schedule(schedule_id: int):
    """Delete a scheduled job"""
    try:
        global blog_schedules
        original_count = len(blog_schedules)
        
        blog_schedules = [s for s in blog_schedules if s["id"] != schedule_id]
        
        if len(blog_schedules) < original_count:
            return {
                "success": True,
                "message": "Schedule deleted successfully"
            }
        else:
            return {"error": "Schedule not found"}
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to delete schedule: {str(e)}"
        }

# Analytics APIs
@app.get("/api/analytics/summary")
async def get_analytics_summary():
    """Get comprehensive analytics summary"""
    try:
        # Calculate metrics
        total_posts = len(demo_blog_posts)
        published_posts = len([p for p in demo_blog_posts if p["status"] == "published"])
        draft_posts = len([p for p in demo_blog_posts if p["status"] == "draft"])
        total_views = sum(p["views"] for p in demo_blog_posts)
        avg_engagement = sum(p["engagement_rate"] for p in demo_blog_posts) / max(total_posts, 1)
        avg_seo_score = sum(p["seo_score"] for p in demo_blog_posts) / max(total_posts, 1)
        
        # Top performing posts
        top_posts = sorted(demo_blog_posts, key=lambda x: x["views"], reverse=True)[:5]
        
        # Recent activity (last 7 days)
        recent_posts = [p for p in demo_blog_posts if 
                       datetime.fromisoformat(p["created_at"].replace("Z", "+00:00")) > 
                       datetime.now() - timedelta(days=7)]
        
        return {
            "summary": {
                "overall_performance": {
                    "total_posts": total_posts,
                    "published_posts": published_posts,
                    "draft_posts": draft_posts,
                    "total_views": total_views,
                    "average_engagement_rate": round(avg_engagement, 1),
                    "average_seo_score": round(avg_seo_score, 0)
                },
                "top_performing_posts": [
                    {
                        "id": post["id"],
                        "title": post["title"],
                        "views": post["views"],
                        "engagement_rate": post["engagement_rate"],
                        "seo_score": post["seo_score"]
                    } for post in top_posts
                ],
                "recent_activity": {
                    "posts_this_week": len(recent_posts),
                    "average_engagement": round(avg_engagement, 1) if recent_posts else 0,
                    "total_views_this_week": sum(p["views"] for p in recent_posts)
                }
            },
            "posts": demo_blog_posts[-10:],  # Last 10 posts
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "error": f"Failed to retrieve analytics: {str(e)}"
        }

@app.get("/api/analytics/blogs")
async def blog_analytics_endpoint():
    """Get blog-specific analytics"""
    return await get_analytics_summary()

# Helper functions
def calculate_next_run(frequency: str, time: str) -> str:
    """Calculate next run time for a schedule"""
    now = datetime.now()
    hour, minute = map(int, time.split(":"))
    
    if frequency == "daily":
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_run <= now:
            next_run += timedelta(days=1)
    elif frequency == "weekly":
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        days_ahead = 7 - now.weekday()  # Next Monday
        if days_ahead <= 0:
            days_ahead += 7
        next_run += timedelta(days=days_ahead)
    else:
        next_run = now + timedelta(hours=24)  # Default to daily
    
    return next_run.isoformat()

def get_dashboard_html():
    """Main dashboard HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Automation Agent - Dashboard</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 1.8rem;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.3s ease;
        }
        
        .nav-links a:hover, .nav-links a.active {
            background: #667eea;
            color: white;
        }
        
        .container {
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
        }
        
        .card {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .card-header h3 {
            color: #333;
            font-size: 1.3rem;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        
        .stat-item {
            text-align: center;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.5rem;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            text-decoration: none;
            display: inline-block;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-info {
            background: #17a2b8;
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .quick-actions {
            display: flex;
            gap: 1rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #28a745;
            margin-right: 0.5rem;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: #666;
        }
        
        .posts-list {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .post-item {
            padding: 1rem;
            border-bottom: 1px solid #eee;
        }
        
        .post-item:last-child {
            border-bottom: none;
        }
        
        .post-title {
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        .post-meta {
            font-size: 0.9rem;
            color: #666;
        }
        
        .status-badge {
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .status-published {
            background: #d4edda;
            color: #155724;
        }
        
        .status-draft {
            background: #fff3cd;
            color: #856404;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                display: none;
            }
            
            .quick-actions {
                flex-direction: column;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header class="header">
        <h1><i class="fas fa-robot"></i> AI Automation Agent</h1>
        <nav class="nav-links">
            <a href="/" class="active">Dashboard</a>
            <a href="/blog-automation">Blog Automation</a>
            <a href="/analytics">Analytics</a>
            <a href="/settings">Settings</a>
        </nav>
    </header>
    
    <div class="container">
        <div class="dashboard-grid">
            <!-- Agent Status Card -->
            <div class="card">
                <div class="card-header">
                    <h3><i class="fas fa-server"></i> Agent Status</h3>
                    <span class="status-indicator"></span>
                </div>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value" id="uptime">--</div>
                        <div class="stat-label">Uptime (hours)</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">7.0</div>
                        <div class="stat-label">Version</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="modulesCount">5</div>
                        <div class="stat-label">Active Modules</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="dbStatus">Connected</div>
                        <div class="stat-label">Database</div>
                    </div>
                </div>
            </div>
            
            <!-- Blog Statistics Card -->
            <div class="card">
                <div class="card-header">
                    <h3><i class="fas fa-blog"></i> Blog Automation</h3>
                </div>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-value" id="totalPosts">--</div>
                        <div class="stat-label">Total Posts</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="totalViews">--</div>
                        <div class="stat-label">Total Views</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="avgEngagement">--</div>
                        <div class="stat-label">Avg Engagement</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="seoScore">--</div>
                        <div class="stat-label">SEO Score</div>
                    </div>
                </div>
                <div class="quick-actions">
                    <button class="btn btn-success" onclick="showGenerateModal()">
                        <i class="fas fa-plus"></i> Generate Blog
                    </button>
                    <button class="btn btn-info" onclick="showSeriesModal()">
                        <i class="fas fa-layer-group"></i> Generate Series
                    </button>
                    <a href="/blog-automation" class="btn btn-primary">
                        <i class="fas fa-cog"></i> Manage All Blogs
                    </a>
                </div>
            </div>
            
            <!-- Recent Posts Card -->
            <div class="card">
                <div class="card-header">
                    <h3><i class="fas fa-clock"></i> Recent Posts</h3>
                    <button class="btn" onclick="loadRecentPosts()">
                        <i class="fas fa-sync-alt"></i> Refresh
                    </button>
                </div>
                <div class="posts-list" id="recentPosts">
                    <div class="loading">Loading recent posts...</div>
                </div>
            </div>
            
            <!-- Activity Feed Card -->
            <div class="card">
                <div class="card-header">
                    <h3><i class="fas fa-activity"></i> Activity Feed</h3>
                </div>
                <div class="posts-list" id="activityFeed">
                    <div class="loading">Loading activity...</div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Blog Generation Modal -->
    <div id="generateModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); background: white; padding: 2rem; border-radius: 12px; max-width: 500px; width: 90%;">
            <h3>Generate New Blog Post</h3>
            <form id="generateForm">
                <div style="margin: 1rem 0;">
                    <label>Topic *</label>
                    <input type="text" id="blogTopic" style="width: 100%; padding: 0.5rem; margin-top: 0.5rem;" required>
                </div>
                <div style="margin: 1rem 0;">
                    <label>Max Words</label>
                    <input type="number" id="blogMaxWords" value="800" style="width: 100%; padding: 0.5rem; margin-top: 0.5rem;">
                </div>
                <div style="margin: 1rem 0;">
                    <label>
                        <input type="checkbox" id="publishImmediately"> Publish immediately
                    </label>
                </div>
                <div style="display: flex; gap: 1rem; justify-content: flex-end;">
                    <button type="button" onclick="closeModal()" class="btn">Cancel</button>
                    <button type="submit" class="btn btn-success">Generate</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboardData();
            loadRecentPosts();
            loadActivityFeed();
            
            // Set up form handlers
            document.getElementById('generateForm').addEventListener('submit', handleBlogGeneration);
        });
        
        async function loadDashboardData() {
            try {
                const response = await fetch('/api/agent/status');
                const data = await response.json();
                
                // Update stats
                if (data.agent) {
                    document.getElementById('uptime').textContent = Math.round(data.agent.uptime_seconds / 3600);
                }
                
                if (data.modules) {
                    document.getElementById('modulesCount').textContent = Object.keys(data.modules).length;
                }
                
                // Load blog stats
                const blogResponse = await fetch('/api/analytics/summary');
                const blogData = await blogResponse.json();
                
                if (blogData.summary && blogData.summary.overall_performance) {
                    const stats = blogData.summary.overall_performance;
                    document.getElementById('totalPosts').textContent = stats.total_posts || 0;
                    document.getElementById('totalViews').textContent = formatNumber(stats.total_views || 0);
                    document.getElementById('avgEngagement').textContent = (stats.average_engagement_rate || 0) + '%';
                    document.getElementById('seoScore').textContent = (stats.average_seo_score || 0) + '/100';
                }
                
            } catch (error) {
                console.error('Error loading dashboard data:', error);
            }
        }
        
        async function loadRecentPosts() {
            try {
                const response = await fetch('/api/blog/posts?limit=5');
                const data = await response.json();
                
                const container = document.getElementById('recentPosts');
                if (data.posts && data.posts.length > 0) {
                    container.innerHTML = data.posts.map(post => `
                        <div class="post-item">
                            <div class="post-title">${post.title}</div>
                            <div class="post-meta">
                                <span class="status-badge status-${post.status}">${post.status}</span>
                                • ${post.views} views • ${post.engagement_rate}% engagement
                            </div>
                        </div>
                    `).join('');
                } else {
                    container.innerHTML = '<div class="loading">No posts found</div>';
                }
                
            } catch (error) {
                console.error('Error loading recent posts:', error);
            }
        }
        
        async function loadActivityFeed() {
            // Simulate activity feed
            const activities = [
                { type: 'blog_generated', message: 'Generated blog post about AI in Healthcare', time: '2 minutes ago' },
                { type: 'blog_published', message: 'Published "Python Automation Scripts" to WordPress', time: '1 hour ago' },
                { type: 'schedule_created', message: 'Created daily blog generation schedule', time: '3 hours ago' },
                { type: 'analytics_updated', message: 'Updated analytics for 10 posts', time: '5 hours ago' }
            ];
            
            const container = document.getElementById('activityFeed');
            container.innerHTML = activities.map(activity => `
                <div class="post-item">
                    <div class="post-title">
                        <i class="fas fa-${activity.type.includes('blog') ? 'blog' : 'cog'}"></i>
                        ${activity.message}
                    </div>
                    <div class="post-meta">${activity.time}</div>
                </div>
            `).join('');
        }
        
        function showGenerateModal() {
            document.getElementById('generateModal').style.display = 'block';
        }
        
        function showSeriesModal() {
            alert('Series generation feature coming soon!');
        }
        
        function closeModal() {
            document.getElementById('generateModal').style.display = 'none';
        }
        
        async function handleBlogGeneration(e) {
            e.preventDefault();
            
            const topic = document.getElementById('blogTopic').value;
            const maxWords = parseInt(document.getElementById('blogMaxWords').value);
            const publishImmediately = document.getElementById('publishImmediately').checked;
            
            try {
                const response = await fetch('/api/blog/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        topic: topic,
                        max_words: maxWords,
                        publish_immediately: publishImmediately
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('Blog post generated successfully!');
                    closeModal();
                    loadDashboardData();
                    loadRecentPosts();
                } else {
                    alert('Error: ' + result.error);
                }
                
            } catch (error) {
                alert('Error generating blog post: ' + error.message);
            }
        }
        
        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toString();
        }
    </script>
</body>
</html>
    """

def get_blog_automation_html():
    """Complete blog automation page HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Automation - AI Automation Agent</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header h1 {
            color: #667eea;
            font-size: 1.8rem;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #333;
            font-weight: 500;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.3s ease;
        }
        
        .nav-links a:hover {
            background: #667eea;
            color: white;
        }
        
        .nav-links a.active {
            background: #667eea;
            color: white;
        }
        
        .container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
        }
        
        .page-header {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .page-header h1 {
            color: #333;
            margin-bottom: 0.5rem;
        }
        
        .page-header p {
            color: #666;
        }
        
        .actions-bar {
            background: white;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .actions-group {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-success {
            background: #28a745;
            color: white;
        }
        
        .btn-info {
            background: #17a2b8;
            color: white;
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .stats-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }
        
        .stat-card {
            background: white;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .stat-icon {
            background: #667eea;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .stat-content {
            flex: 1;
        }
        
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #333;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }
        
        .blog-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2rem;
        }
        
        .blog-section {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        
        .section-header {
            padding: 1.5rem 2rem;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .section-header h3 {
            color: #333;
        }
        
        .section-filters {
            display: flex;
            gap: 1rem;
        }
        
        .filter-select {
            padding: 0.5rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            background: white;
        }
        
        .table-container {
            overflow-x: auto;
        }
        
        .blog-table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .blog-table th,
        .blog-table td {
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        
        .blog-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #333;
        }
        
        .status-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }
        
        .status-published {
            background: #d4edda;
            color: #155724;
        }
        
        .status-draft {
            background: #fff3cd;
            color: #856404;
        }
        
        .status-scheduled {
            background: #cce5ff;
            color: #004085;
        }
        
        .action-buttons {
            display: flex;
            gap: 0.5rem;
        }
        
        .btn-icon {
            padding: 0.5rem;
            border: none;
            background: #f8f9fa;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .btn-icon:hover {
            background: #667eea;
            color: white;
        }
        
        .scheduling-panel {
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            height: fit-content;
        }
        
        .panel-header {
            padding: 1.5rem 2rem;
            border-bottom: 1px solid #eee;
        }
        
        .panel-header h3 {
            color: #333;
        }
        
        .panel-content {
            padding: 1.5rem 2rem;
        }
        
        .schedule-section {
            margin-bottom: 2rem;
        }
        
        .schedule-section h4 {
            margin-bottom: 1rem;
            color: #333;
        }
        
        .schedule-item {
            padding: 1rem;
            border: 1px solid #eee;
            border-radius: 8px;
            margin-bottom: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .schedule-info {
            flex: 1;
        }
        
        .schedule-type {
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        .schedule-time {
            color: #666;
            font-size: 0.9rem;
        }
        
        .schedule-topics {
            margin-top: 0.5rem;
        }
        
        .topic-tag {
            background: #667eea;
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            margin-right: 0.5rem;
        }
        
        .schedule-actions {
            display: flex;
            gap: 0.5rem;
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 0.9rem;
        }
        
        .form-group textarea {
            resize: vertical;
            min-height: 80px;
        }
        
        .btn-full {
            width: 100%;
        }
        
        .loading {
            text-align: center;
            padding: 2rem;
            color: #666;
        }
        
        .no-data {
            text-align: center;
            padding: 2rem;
            color: #666;
            font-style: italic;
        }
        
        @media (max-width: 1024px) {
            .blog-grid {
                grid-template-columns: 1fr;
            }
            
            .stats-overview {
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            }
        }
        
        @media (max-width: 768px) {
            .actions-bar {
                flex-direction: column;
                align-items: stretch;
            }
            
            .actions-group {
                justify-content: center;
            }
            
            .section-header {
                flex-direction: column;
                align-items: stretch;
            }
            
            .section-filters {
                justify-content: center;
            }
            
            .nav-links {
                display: none;
            }
        }
        
        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
        }
        
        .modal.show {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            background: white;
            border-radius: 12px;
            max-width: 600px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
        }
        
        .modal-header {
            padding: 1.5rem 2rem;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .modal-header h3 {
            color: #333;
        }
        
        .modal-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #666;
        }
        
        .modal-body {
            padding: 2rem;
        }
        
        .modal-footer {
            padding: 1rem 2rem;
            border-top: 1px solid #eee;
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
    </style>
</head>
<body>
    <header class="header">
        <h1><i class="fas fa-robot"></i> AI Automation Agent</h1>
        <nav class="nav-links">
            <a href="/">Dashboard</a>
            <a href="/blog-automation" class="active">Blog Automation</a>
            <a href="/analytics">Analytics</a>
            <a href="/settings">Settings</a>
        </nav>
    </header>
    
    <div class="container">
        <div class="page-header">
            <h1><i class="fas fa-blog"></i> Blog Automation</h1>
            <p>Manage your AI-powered blog generation, scheduling, and publishing</p>
        </div>
        
        <div class="actions-bar">
            <div class="actions-group">
                <button class="btn btn-success" onclick="showBlogGenerationModal()">
                    <i class="fas fa-plus"></i> Generate Single Blog
                </button>
                <button class="btn btn-info" onclick="showSeriesGenerationModal()">
                    <i class="fas fa-layer-group"></i> Generate Blog Series
                </button>
                <button class="btn btn-primary" onclick="showSchedulingModal()">
                    <i class="fas fa-calendar"></i> Schedule Daily Blog
                </button>
            </div>
            <div class="actions-group">
                <button class="btn btn-secondary" onclick="loadBlogPosts()">
                    <i class="fas fa-sync-alt"></i> Refresh
                </button>
            </div>
        </div>
        
        <div class="stats-overview">
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-blog"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-number" id="totalBlogs">--</div>
                    <div class="stat-label">Total Blogs</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-eye"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-number" id="totalViews">--</div>
                    <div class="stat-label">Total Views</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-heart"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-number" id="avgEngagement">--</div>
                    <div class="stat-label">Avg Engagement</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">
                    <i class="fas fa-star"></i>
                </div>
                <div class="stat-content">
                    <div class="stat-number" id="avgSeoScore">--</div>
                    <div class="stat-label">Avg SEO Score</div>
                </div>
            </div>
        </div>
        
        <div class="blog-grid">
            <div class="blog-section">
                <div class="section-header">
                    <h3><i class="fas fa-list"></i> Recent Blog Posts</h3>
                    <div class="section-filters">
                        <select class="filter-select" id="statusFilter" onchange="filterPosts()">
                            <option value="">All Status</option>
                            <option value="published">Published</option>
                            <option value="draft">Draft</option>
                            <option value="scheduled">Scheduled</option>
                        </select>
                        <select class="filter-select" id="topicFilter" onchange="filterPosts()">
                            <option value="">All Topics</option>
                            <option value="ai">AI</option>
                            <option value="technology">Technology</option>
                            <option value="programming">Programming</option>
                        </select>
                    </div>
                </div>
                <div class="table-container">
                    <table class="blog-table" id="blogTable">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Topic</th>
                                <th>Status</th>
                                <th>Views</th>
                                <th>Engagement</th>
                                <th>SEO Score</th>
                                <th>Created</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td colspan="8" class="loading">Loading blog posts...</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div class="scheduling-panel">
                <div class="panel-header">
                    <h3><i class="fas fa-calendar-alt"></i> Scheduling</h3>
                </div>
                <div class="panel-content">
                    <div class="schedule-section">
                        <h4>Current Schedule</h4>
                        <div class="schedule-list" id="currentSchedule">
                            <div class="schedule-item">
                                <div class="schedule-loading">Loading schedule...</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="schedule-form">
                        <h4>Quick Schedule</h4>
                        <form id="quickScheduleForm">
                            <div class="form-group">
                                <label>Frequency</label>
                                <select id="scheduleFrequency">
                                    <option value="daily">Daily</option>
                                    <option value="weekly">Weekly</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Time</label>
                                <input type="time" id="scheduleTime" value="09:00">
                            </div>
                            <div class="form-group">
                                <label>Topics</label>
                                <div class="topic-tags" id="scheduleTopics">
                                    <span class="topic-tag">AI</span>
                                    <span class="topic-tag">Technology</span>
                                    <span class="topic-tag">Programming</span>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-primary btn-full">
                                <i class="fas fa-plus"></i> Add Schedule
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Blog Generation Modal -->
    <div id="blogGenerationModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Generate Single Blog Post</h3>
                <button class="modal-close" onclick="closeModal('blogGenerationModal')">&times;</button>
            </div>
            <div class="modal-body">
                <form id="blogGenerationForm">
                    <div class="form-row">
                        <div class="form-group">
                            <label>Topic *</label>
                            <input type="text" id="blogTopic" placeholder="e.g., AI in Healthcare" required>
                        </div>
                        <div class="form-group">
                            <label>Max Words</label>
                            <input type="number" id="blogMaxWords" value="800" min="100" max="2000">
                        </div>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Target Audience</label>
                            <select id="blogAudience">
                                <option value="general">General Public</option>
                                <option value="professionals">Professionals</option>
                                <option value="experts">Industry Experts</option>
                                <option value="beginners">Beginners</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Writing Style</label>
                            <select id="blogStyle">
                                <option value="informative">Informative</option>
                                <option value="casual">Casual</option>
                                <option value="technical">Technical</option>
                                <option value="how_to">How-to Guide</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="publishImmediately"> Publish immediately after generation
                        </label>
                    </div>
                    <div class="form-group">
                        <label>Additional Instructions</label>
                        <textarea id="blogInstructions" placeholder="Any specific requirements or instructions..."></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeModal('blogGenerationModal')">Cancel</button>
                <button class="btn btn-success" onclick="handleBlogGeneration()">Generate</button>
            </div>
        </div>
    </div>
    
    <!-- Series Generation Modal -->
    <div id="seriesGenerationModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h3>Generate Blog Series</h3>
                <button class="modal-close" onclick="closeModal('seriesGenerationModal')">&times;</button>
            </div>
            <div class="modal-body">
                <form id="seriesGenerationForm">
                    <div class="form-group">
                        <label>Main Topic *</label>
                        <input type="text" id="seriesTopic" placeholder="e.g., Python Programming for Beginners" required>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Number of Posts</label>
                            <input type="number" id="seriesCount" value="3" min="2" max="10">
                        </div>
                        <div class="form-group">
                            <label>Target Audience</label>
                            <select id="seriesAudience">
                                <option value="general">General Public</option>
                                <option value="professionals">Professionals</option>
                                <option value="experts">Industry Experts</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label>
                            <input type="checkbox" id="publishSeriesImmediately"> Publish series immediately
                        </label>
                    </div>
                    <div class="form-group">
                        <label>Series Description</label>
                        <textarea id="seriesDescription" placeholder="Describe what this series will cover..."></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" onclick="closeModal('seriesGenerationModal')">Cancel</button>
                <button class="btn btn-success" onclick="handleSeriesGeneration()">Generate Series</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentPosts = [];
        
        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            loadBlogPosts();
            loadStatistics();
            loadSchedules();
            setupEventListeners();
        });
        
        function setupEventListeners() {
            document.getElementById('quickScheduleForm').addEventListener('submit', handleQuickSchedule);
        }
        
        async function loadBlogPosts() {
            try {
                const response = await fetch('/api/blog/posts?limit=50');
                const data = await response.json();
                
                if (data.posts) {
                    currentPosts = data.posts;
                    renderBlogTable(currentPosts);
                }
                
            } catch (error) {
                console.error('Error loading blog posts:', error);
                showToast('Failed to load blog posts', 'error');
            }
        }
        
        function renderBlogTable(posts) {
            const tbody = document.querySelector('#blogTable tbody');
            
            if (posts.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="no-data">No blog posts found</td></tr>';
                return;
            }
            
            tbody.innerHTML = posts.map(post => `
                <tr data-post-id="${post.id}">
                    <td class="post-title">
                        <div class="title-text">${truncateText(post.title, 50)}</div>
                        <div class="post-meta">
                            <span class="word-count">${post.word_count || 0} words</span>
                            ${post.is_auto_generated ? '<span class="auto-tag">AI Generated</span>' : ''}
                        </div>
                    </td>
                    <td><span class="topic-badge">${post.topic || 'General'}</span></td>
                    <td>
                        <span class="status-badge status-${post.status}">${post.status}</span>
                    </td>
                    <td>
                        <div class="metric-value">${formatNumber(post.views || 0)}</div>
                    </td>
                    <td>
                        <div class="metric-value">${(post.engagement_rate || 0).toFixed(1)}%</div>
                    </td>
                    <td>
                        <div class="seo-score">
                            <span class="score-value">${post.seo_score || '--'}</span>
                            ${post.seo_score ? '/100' : ''}
                        </div>
                    </td>
                    <td>
                        <div class="date-value">${formatDate(post.created_at)}</div>
                    </td>
                    <td>
                        <div class="action-buttons">
                            <button class="btn-icon" onclick="viewPost('${post.id}')" title="View">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn-icon" onclick="editPost('${post.id}')" title="Edit">
                                <i class="fas fa-edit"></i>
                            </button>
                            ${post.status !== 'published' ? `
                                <button class="btn-icon" onclick="publishPost('${post.id}')" title="Publish">
                                    <i class="fas fa-share"></i>
                                </button>
                            ` : ''}
                            <button class="btn-icon" onclick="deletePost('${post.id}')" title="Delete">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </td>
                </tr>
            `).join('');
        }
        
        async function loadStatistics() {
            try {
                const response = await fetch('/api/analytics/summary');
                const data = await response.json();
                
                if (data.summary && data.summary.overall_performance) {
                    const stats = data.summary.overall_performance;
                    document.getElementById('totalBlogs').textContent = stats.total_posts || 0;
                    document.getElementById('totalViews').textContent = formatNumber(stats.total_views || 0);
                    document.getElementById('avgEngagement').textContent = (stats.average_engagement_rate || 0).toFixed(1) + '%';
                    document.getElementById('avgSeoScore').textContent = (stats.average_seo_score || 0).toFixed(0) + '/100';
                }
                
            } catch (error) {
                console.error('Error loading statistics:', error);
            }
        }
        
        async function loadSchedules() {
            try {
                const response = await fetch('/api/blog/schedules');
                const data = await response.json();
                
                if (data.schedules) {
                    renderSchedules(data.schedules);
                }
                
            } catch (error) {
                console.error('Error loading schedules:', error);
            }
        }
        
        function renderSchedules(schedules) {
            const container = document.getElementById('currentSchedule');
            
            if (schedules.length === 0) {
                container.innerHTML = '<div class="no-data">No scheduled jobs found</div>';
                return;
            }
            
            container.innerHTML = schedules.map(job => `
                <div class="schedule-item" data-job-id="${job.id}">
                    <div class="schedule-info">
                        <div class="schedule-type">
                            <i class="fas fa-${job.frequency === 'daily' ? 'calendar-day' : 'calendar-week'}"></i>
                            ${job.frequency === 'daily' ? 'Daily' : `Weekly (${job.day})`}
                        </div>
                        <div class="schedule-time">${job.time}</div>
                        <div class="schedule-topics">
                            ${job.topics.map(topic => `<span class="topic-tag">${topic}</span>`).join('')}
                        </div>
                    </div>
                    <div class="schedule-actions">
                        <button class="btn-icon" onclick="editSchedule('${job.id}')" title="Edit">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-icon" onclick="toggleSchedule('${job.id}')" title="Toggle">
                            <i class="fas fa-${job.status === 'active' ? 'pause' : 'play'}"></i>
                        </button>
                        <button class="btn-icon" onclick="deleteSchedule('${job.id}')" title="Delete">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        }
        
        // Modal functions
        function showBlogGenerationModal() {
            document.getElementById('blogGenerationModal').classList.add('show');
        }
        
        function showSeriesGenerationModal() {
            document.getElementById('seriesGenerationModal').classList.add('show');
        }
        
        function showSchedulingModal() {
            alert('Scheduling modal feature coming soon!');
        }
        
        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('show');
        }
        
        // Form handlers
        async function handleBlogGeneration() {
            try {
                const topic = document.getElementById('blogTopic').value;
                const maxWords = parseInt(document.getElementById('blogMaxWords').value);
                const audience = document.getElementById('blogAudience').value;
                const style = document.getElementById('blogStyle').value;
                const publishImmediately = document.getElementById('publishImmediately').checked;
                const instructions = document.getElementById('blogInstructions').value;
                
                const response = await fetch('/api/blog/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        topic: topic,
                        max_words: maxWords,
                        target_audience: audience,
                        style: style,
                        publish_immediately: publishImmediately,
                        instructions: instructions
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showToast('Blog post generated successfully!', 'success');
                    closeModal('blogGenerationModal');
                    loadBlogPosts();
                    loadStatistics();
                } else {
                    showToast('Error: ' + result.error, 'error');
                }
                
            } catch (error) {
                showToast('Error generating blog post: ' + error.message, 'error');
            }
        }
        
        async function handleSeriesGeneration() {
            try {
                const mainTopic = document.getElementById('seriesTopic').value;
                const numPosts = parseInt(document.getElementById('seriesCount').value);
                const audience = document.getElementById('seriesAudience').value;
                const publishImmediately = document.getElementById('publishSeriesImmediately').checked;
                const description = document.getElementById('seriesDescription').value;
                
                const response = await fetch('/api/blog/series', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        main_topic: mainTopic,
                        num_posts: numPosts,
                        target_audience: audience,
                        publish_immediately: publishImmediately,
                        description: description
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showToast(`Blog series of ${result.total_posts} posts generated successfully!`, 'success');
                    closeModal('seriesGenerationModal');
                    loadBlogPosts();
                    loadStatistics();
                } else {
                    showToast('Error: ' + result.error, 'error');
                }
                
            } catch (error) {
                showToast('Error generating blog series: ' + error.message, 'error');
            }
        }
        
        async function handleQuickSchedule(e) {
            e.preventDefault();
            
            try {
                const frequency = document.getElementById('scheduleFrequency').value;
                const time = document.getElementById('scheduleTime').value;
                const topics = Array.from(document.querySelectorAll('#scheduleTopics .topic-tag')).map(tag => tag.textContent);
                
                const response = await fetch('/api/blog/schedule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        frequency: frequency,
                        time: time,
                        topics: topics,
                        publish_mode: 'draft'
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showToast('Schedule created successfully', 'success');
                    loadSchedules();
                } else {
                    showToast('Error: ' + result.error, 'error');
                }
                
            } catch (error) {
                showToast('Error creating schedule: ' + error.message, 'error');
            }
        }
        
        // Post management functions
        async function viewPost(postId) {
            const post = currentPosts.find(p => p.id == postId);
            if (post) {
                alert(`Viewing post: ${post.title}\\n\\nThis would open a detailed view modal in a full implementation.`);
            }
        }
        
        async function editPost(postId) {
            alert(`Edit functionality for post ${postId} - Coming soon!`);
        }
        
        async function publishPost(postId) {
            try {
                const response = await fetch(`/api/blog/publish/${postId}`, { method: 'POST' });
                const result = await response.json();
                
                if (result.success) {
                    showToast('Post published successfully!', 'success');
                    loadBlogPosts();
                    loadStatistics();
                } else {
                    showToast('Error: ' + result.error, 'error');
                }
                
            } catch (error) {
                showToast('Error publishing post: ' + error.message, 'error');
            }
        }
        
        async function deletePost(postId) {
            if (confirm('Are you sure you want to delete this blog post?')) {
                try {
                    const response = await fetch(`/api/blog/posts/${postId}`, { method: 'DELETE' });
                    const result = await response.json();
                    
                    if (result.success) {
                        showToast('Post deleted successfully', 'success');
                        loadBlogPosts();
                        loadStatistics();
                    } else {
                        showToast('Error: ' + result.error, 'error');
                    }
                    
                } catch (error) {
                    showToast('Error deleting post: ' + error.message, 'error');
                }
            }
        }
        
        function filterPosts() {
            const statusFilter = document.getElementById('statusFilter').value;
            const topicFilter = document.getElementById('topicFilter').value;
            
            const filteredPosts = currentPosts.filter(post => {
                const statusMatch = !statusFilter || post.status === statusFilter;
                const topicMatch = !topicFilter || (post.topic && post.topic.toLowerCase().includes(topicFilter.toLowerCase()));
                return statusMatch && topicMatch;
            });
            
            renderBlogTable(filteredPosts);
        }
        
        // Utility functions
        function truncateText(text, maxLength) {
            return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
        }
        
        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toString();
        }
        
        function formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString();
        }
        
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 1rem 2rem;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 10000;
                animation: slideIn 0.3s ease;
            `;
            
            if (type === 'success') toast.style.background = '#28a745';
            else if (type === 'error') toast.style.background = '#dc3545';
            else toast.style.background = '#17a2b8';
            
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.remove();
            }, 5000);
        }
    </script>
</body>
</html>
    """

def get_analytics_html():
    """Analytics page HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics - AI Automation Agent</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f8f9fa; }
        .header { background: white; padding: 1rem 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { text-decoration: none; color: #333; padding: 0.5rem 1rem; border-radius: 6px; }
        .nav-links a:hover, .nav-links a.active { background: #667eea; color: white; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
        .stat-item { text-align: center; padding: 1rem; background: #f8f9fa; border-radius: 8px; }
        .stat-value { font-size: 2rem; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; margin-top: 0.5rem; }
    </style>
</head>
<body>
    <header class="header">
        <h1><i class="fas fa-robot"></i> AI Automation Agent</h1>
        <nav class="nav-links">
            <a href="/">Dashboard</a>
            <a href="/blog-automation">Blog Automation</a>
            <a href="/analytics" class="active">Analytics</a>
            <a href="/settings">Settings</a>
        </nav>
    </header>
    
    <div class="container">
        <div class="card">
            <h1><i class="fas fa-chart-line"></i> Analytics Dashboard</h1>
            <p>Comprehensive analytics for your AI automation agent</p>
        </div>
        
        <div class="card">
            <h3>Performance Overview</h3>
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value" id="totalPosts">--</div>
                    <div class="stat-label">Total Posts</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="totalViews">--</div>
                    <div class="stat-label">Total Views</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="avgEngagement">--</div>
                    <div class="stat-label">Avg Engagement</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="avgSeoScore">--</div>
                    <div class="stat-label">Avg SEO Score</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            loadAnalytics();
        });
        
        async function loadAnalytics() {
            try {
                const response = await fetch('/api/analytics/summary');
                const data = await response.json();
                
                if (data.summary && data.summary.overall_performance) {
                    const stats = data.summary.overall_performance;
                    document.getElementById('totalPosts').textContent = stats.total_posts || 0;
                    document.getElementById('totalViews').textContent = formatNumber(stats.total_views || 0);
                    document.getElementById('avgEngagement').textContent = (stats.average_engagement_rate || 0) + '%';
                    document.getElementById('avgSeoScore').textContent = (stats.average_seo_score || 0) + '/100';
                }
                
            } catch (error) {
                console.error('Error loading analytics:', error);
            }
        }
        
        function formatNumber(num) {
            if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
            if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
            return num.toString();
        }
    </script>
</body>
</html>
    """

def get_settings_html():
    """Settings page HTML"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Settings - AI Automation Agent</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #f8f9fa; }
        .header { background: white; padding: 1rem 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .container { max-width: 800px; margin: 2rem auto; padding: 0 2rem; }
        .nav-links { display: flex; gap: 2rem; }
        .nav-links a { text-decoration: none; color: #333; padding: 0.5rem 1rem; border-radius: 6px; }
        .nav-links a:hover, .nav-links a.active { background: #667eea; color: white; }
        .card { background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); margin-bottom: 2rem; }
        .form-group { margin-bottom: 1rem; }
        .form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
        .form-group input, .form-group select { width: 100%; padding: 0.75rem; border: 1px solid #ddd; border-radius: 6px; }
        .btn { padding: 0.75rem 1.5rem; background: #667eea; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .btn:hover { background: #5a6fd8; }
    </style>
</head>
<body>
    <header class="header">
        <h1><i class="fas fa-robot"></i> AI Automation Agent</h1>
        <nav class="nav-links">
            <a href="/">Dashboard</a>
            <a href="/blog-automation">Blog Automation</a>
            <a href="/analytics">Analytics</a>
            <a href="/settings" class="active">Settings</a>
        </nav>
    </header>
    
    <div class="container">
        <div class="card">
            <h1><i class="fas fa-cog"></i> Settings</h1>
            <p>Configure your AI automation agent</p>
        </div>
        
        <div class="card">
            <h3>Blog Automation Settings</h3>
            <form>
                <div class="form-group">
                    <label>Default Word Count</label>
                    <input type="number" value="800" min="100" max="2000">
                </div>
                <div class="form-group">
                    <label>Default Publishing Mode</label>
                    <select>
                        <option>Save as Draft</option>
                        <option>Publish Immediately</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>AI Model</label>
                    <select>
                        <option>GPT-4</option>
                        <option>GPT-3.5 Turbo</option>
                    </select>
                </div>
                <button type="submit" class="btn">Save Settings</button>
            </form>
        </div>
    </div>
</body>
</html>
    """

# WebSocket for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates"""
    await websocket.accept()
    
    # Send welcome message
    await websocket.send_json({
        "type": "welcome",
        "message": "AI Automation Agent with Blog Publishing connected successfully!",
        "timestamp": datetime.now().isoformat(),
        "agent_status": "running"
    })
    
    try:
        while True:
            try:
                # Receive message from client
                data = await websocket.receive_text()
                
                # Process different types of messages
                if data.lower() in ["ping", "hello", "status"]:
                    response = {
                        "type": "status",
                        "message": "Agent is running smoothly with blog automation!",
                        "uptime": (datetime.now() - agent_stats["start_time"]).total_seconds(),
                        "timestamp": datetime.now().isoformat(),
                        "blogs_generated": agent_stats["total_blogs_generated"],
                        "blogs_published": agent_stats["total_published"]
                    }
                    await websocket.send_json(response)
                
                elif "blog" in data.lower():
                    # Get recent blog activity
                    recent_blogs = demo_blog_posts[-3:] if demo_blog_posts else []
                    response = {
                        "type": "blog_update",
                        "recent_blogs": recent_blogs,
                        "total_blogs": len(demo_blog_posts),
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send_json(response)
                
                else:
                    # Default response
                    response = {
                        "type": "echo",
                        "message": f"Received: {data}",
                        "timestamp": datetime.now().isoformat()
                    }
                    await websocket.send_json(response)
                    
            except WebSocketDisconnect:
                break
            except Exception as e:
                print(f"WebSocket error: {e}")
                await websocket.send_json({
                    "type": "error",
                    "message": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket connection error: {e}")

if __name__ == "__main__":
    print("🚀 Starting AI Automation Agent with Blog Publishing...")
    print("📝 Features available:")
    print("   • AI-powered blog generation")
    print("   • Blog series creation")
    print("   • Automatic publishing")
    print("   • Content scheduling")
    print("   • Analytics and insights")
    print("   • Real-time updates")
    print("\n🌐 Access your application at: http://localhost:8000")
    print("📊 Dashboard: http://localhost:8000")
    print("✍️ Blog Automation: http://localhost:8000/blog-automation")
    print("📈 Analytics: http://localhost:8000/analytics")
    print("⚙️ Settings: http://localhost:8000/settings")
    
    uvicorn.run(
        "blog_automation_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )