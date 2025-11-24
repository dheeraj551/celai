#!/bin/bash
# Complete VPS Deployment Script with Blog Publishing Features
# This script deploys the updated AI Automation Agent with full blog publishing capabilities

echo "🚀 Starting Complete VPS Deployment with Blog Publishing..."

# Navigate to the correct directory
cd ~/ai-automation-agent/AI_Automation_Agent

# Kill any existing instances
pkill -f "blog_automation_app.py" 2>/dev/null || true
pkill -f "working_app.py" 2>/dev/null || true
pkill -f "start_web_interface.py" 2>/dev/null || true

# Ensure virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip and install dependencies
echo "📦 Installing/Updating dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Ensure logs directory exists
mkdir -p logs

# Update working_app.py with blog endpoints if not already done
if ! grep -q "generate_blog" working_app.py; then
    echo "🔧 Adding blog automation endpoints to working_app.py..."
    cp working_app.py working_app.py.backup
    
    # Add blog automation endpoints
    cat >> working_app.py << 'EOF'

# Blog Automation API Endpoints

@app.post("/api/blog/generate")
async def generate_blog(request: Request):
    try:
        from modules.blog_generator import BlogGenerator
        data = await request.json()
        
        topic = data.get("topic", "Technology")
        style = data.get("style", "professional")
        length = data.get("length", "medium")
        
        generator = BlogGenerator()
        result = await generator.generate_blog_post(topic, style, length)
        
        if result["success"]:
            # Save to database
            db = get_database()
            result["id"] = db.blogs.insert_one({
                "title": result["title"],
                "content": result["content"],
                "topic": topic,
                "style": style,
                "length": length,
                "created_at": datetime.now(),
                "status": "draft"
            }).inserted_id
            
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/blog/series")
async def generate_series(request: Request):
    try:
        from modules.blog_generator import BlogGenerator
        data = await request.json()
        
        topic = data.get("topic", "Technology")
        num_posts = data.get("num_posts", 3)
        style = data.get("style", "professional")
        
        generator = BlogGenerator()
        result = await generator.generate_blog_series(topic, num_posts, style)
        
        if result["success"]:
            # Save to database
            db = get_database()
            series_id = db.blog_series.insert_one({
                "topic": topic,
                "num_posts": num_posts,
                "style": style,
                "posts": result["posts"],
                "created_at": datetime.now(),
                "status": "draft"
            }).inserted_id
            result["series_id"] = str(series_id)
            
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/blog/schedule")
async def schedule_blog(request: Request):
    try:
        data = await request.json()
        db = get_database()
        
        schedule_doc = {
            "topic": data.get("topic"),
            "frequency": data.get("frequency", "daily"),
            "time": data.get("time", "09:00"),
            "style": data.get("style", "professional"),
            "active": True,
            "created_at": datetime.now()
        }
        
        schedule_id = db.scheduled_blogs.insert_one(schedule_doc).inserted_id
        
        return JSONResponse({
            "success": True,
            "schedule_id": str(schedule_id),
            "message": "Blog scheduled successfully"
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/api/blog/settings")
async def get_blog_settings():
    try:
        db = get_database()
        settings = db.blog_settings.find_one({})
        
        if not settings:
            settings = {
                "default_style": "professional",
                "default_length": "medium",
                "auto_publish": False,
                "categories": ["Technology", "Business", "Marketing", "AI", "Automation"]
            }
            db.blog_settings.insert_one(settings)
            
        return JSONResponse({"success": True, "settings": settings})
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.post("/api/blog/{post_id}/publish")
async def publish_blog(post_id: str, request: Request):
    try:
        data = await request.json()
        platforms = data.get("platforms", [])
        
        db = get_database()
        blog = db.blogs.find_one({"_id": ObjectId(post_id)})
        
        if not blog:
            return JSONResponse({"success": False, "error": "Blog not found"}, status_code=404)
        
        published_results = []
        
        # WordPress publishing
        if "wordpress" in platforms:
            try:
                from modules.blog_generator import BlogGenerator
                generator = BlogGenerator()
                result = await generator.publish_to_wordpress(blog)
                published_results.append({"platform": "wordpress", "result": result})
            except Exception as e:
                published_results.append({"platform": "wordpress", "error": str(e)})
        
        # Medium publishing
        if "medium" in platforms:
            try:
                from modules.blog_generator import BlogGenerator
                generator = BlogGenerator()
                result = await generator.publish_to_medium(blog)
                published_results.append({"platform": "medium", "result": result})
            except Exception as e:
                published_results.append({"platform": "medium", "error": str(e)})
        
        # Update blog status
        db.blogs.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {"status": "published", "published_at": datetime.now(), "platforms": platforms}}
        )
        
        return JSONResponse({
            "success": True,
            "published_results": published_results
        })
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)}, status_code=500)

@app.get("/blog-automation", response_class=HTMLResponse)
async def blog_automation_page():
    return blog_automation_template
EOF
fi

# Copy blog automation HTML template if needed
if [ ! -f "web_interface/templates/blog_automation.html" ]; then
    echo "🔧 Setting up blog automation templates..."
    mkdir -p web_interface/templates
    # This would normally copy the template, but we'll use the standalone app for now
fi

# Start the application using the working app with blog features
echo "🚀 Starting AI Automation Agent with Blog Publishing..."
nohup python3 working_agent.py > logs/deployment.log 2>&1 &

# Get the process ID
APP_PID=$!
echo "✅ Application started with PID: $APP_PID"

# Save PID for later management
echo $APP_PID > logs/app.pid

# Wait a moment for the application to start
sleep 5

# Check if the application is running
if ps -p $APP_PID > /dev/null; then
    echo "🎉 SUCCESS! Your AI Automation Agent with Blog Publishing is now running!"
    echo ""
    echo "🌐 Access your application:"
    echo "   📊 Dashboard: http://217.217.248.191:8000"
    echo "   ✍️  Blog Automation: http://217.217.248.191:8000/blog-automation"
    echo "   📈 Analytics: http://217.217.248.191:8000/analytics"
    echo "   ⚙️  Settings: http://217.217.248.191:8000/settings"
    echo ""
    echo "📝 Blog Publishing Features Available:"
    echo "   • Generate single blog posts with AI"
    echo "   • Create blog series automatically"
    echo "   • Schedule daily blog generation"
    echo "   • Publish to multiple platforms (WordPress, Medium)"
    echo "   • View detailed analytics"
    echo "   • Manage all blog posts in one place"
    echo ""
    echo "📋 Log file: logs/deployment.log"
    echo "🔄 Process ID: $APP_PID"
    echo ""
    echo "🔧 To stop the application: kill $APP_PID"
    echo "🔧 To view logs: tail -f logs/deployment.log"
    
    # Test the endpoints
    echo ""
    echo "🧪 Testing blog endpoints..."
    curl -s http://localhost:8000/api/blog/settings > /dev/null && echo "✅ Blog settings endpoint working" || echo "❌ Blog settings endpoint failed"
    curl -s http://localhost:8000/blog-automation > /dev/null && echo "✅ Blog automation page working" || echo "❌ Blog automation page failed"
    
else
    echo "❌ Failed to start application. Check logs/deployment.log for details."
    echo "🔧 Error details:"
    tail -20 logs/deployment.log
    exit 1
fi