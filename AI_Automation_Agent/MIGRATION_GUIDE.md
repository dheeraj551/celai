# Migration Guide: From Web Automation to Next.js API Integration

## Overview

This guide helps you migrate from the previous web automation approach to the new Next.js API integration for the AI Automation Agent.

## What Changed

### System Architecture
**Before:**
```
AI Agent → Browser Automation → WordPress/Medium Website
             ↓
         Selenium/Playwright
             ↓
         DOM Manipulation
```

**After:**
```
AI Agent → Next.js API → Your Database
    ↓           ↓            ↓
OpenAI      HTTP POST    Content
GPT API     JSON Auth    Storage
```

### Dependencies Removed
- ❌ **Node.js**: No longer required
- ❌ **Selenium/Playwright**: No browser automation
- ❌ **Chrome/Firefox drivers**: Not needed
- ❌ **Browser timeouts**: No more waiting for DOM elements

### New Dependencies Added
- ✅ **Next.js API endpoints**: Direct HTTP communication
- ✅ **JSON authentication**: API keys or JWT tokens
- ✅ **HTTP request handling**: Standard REST API calls

## Step-by-Step Migration

### Step 1: Update Environment Variables

#### Remove Old Variables
```bash
# Remove these from your .env file
BROWSER_HEADLESS=true
BROWSER_TIMEOUT=30
USER_AGENT=Mozilla/5.0...
```

#### Add New Variables
```bash
# Add to your .env file
NEXTJS_BLOG_API=https://your-nextjs-site.com/api/blogs
NEXTJS_API_KEY=your_secure_api_key_here
NEXTJS_AUTH_HEADER=Authorization
NEXTJS_API_TIMEOUT=30

# Optional: Keep for backward compatibility
WORDPRESS_URL=https://yourblog.com
MEDIUM_ACCESS_TOKEN=your_medium_token
```

### Step 2: Create Next.js API Endpoints

If you don't have a Next.js site yet, create these API routes:

#### Create Blog Post Endpoint
```typescript
// pages/api/blogs.ts or app/api/blogs/route.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { createBlogPost } from '../../lib/blog-service';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const {
      title,
      content,
      tags = [],
      category,
      status = 'draft',
      ai_generated = false,
      seo_title,
      seo_description,
      metadata = {}
    } = req.body;

    // Validate required fields
    if (!title || !content) {
      return res.status(400).json({ 
        error: 'Missing required fields: title, content' 
      });
    }

    // Create blog post
    const blogPost = await createBlogPost({
      title,
      content,
      tags,
      category,
      status,
      ai_generated,
      seo_title,
      seo_description,
      metadata: {
        ...metadata,
        source: 'ai_automation_agent',
        version: '1.0',
        generated_at: new Date().toISOString()
      }
    });

    res.status(201).json({
      success: true,
      id: blogPost.id,
      url: blogPost.slug,
      status: blogPost.status,
      created_at: blogPost.created_at
    });

  } catch (error) {
    console.error('Error creating blog post:', error);
    res.status(500).json({ 
      error: 'Internal server error',
      message: error.message 
    });
  }
}
```

#### Update Blog Post Endpoint
```typescript
// pages/api/blogs/[id].ts or app/api/blogs/[id]/route.ts
import { NextApiRequest, NextApiResponse } from 'next';
import { updateBlogPost } from '../../../lib/blog-service';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const { id } = req.query;

  if (req.method === 'PUT') {
    try {
      const updates = req.body;
      
      const updatedPost = await updateBlogPost(id, updates);
      
      res.status(200).json({
        success: true,
        id: updatedPost.id,
        url: updatedPost.slug,
        status: updatedPost.status
      });

    } catch (error) {
      console.error('Error updating blog post:', error);
      res.status(500).json({ 
        error: 'Internal server error',
        message: error.message 
      });
    }
  }

  // Add other HTTP methods as needed
}
```

### Step 3: Set Up Authentication

#### Option A: API Key Authentication
```typescript
// pages/api/_lib/auth.ts
export function validateApiKey(req: NextApiRequest): boolean {
  const apiKey = req.headers['x-api-key'];
  return apiKey === process.env.NEXTJS_API_KEY;
}

// Usage in your API endpoint
if (!validateApiKey(req)) {
  return res.status(401).json({ error: 'Unauthorized' });
}
```

#### Option B: JWT Token Authentication (Recommended)
```typescript
// pages/api/_lib/auth.ts
import jwt from 'jsonwebtoken';

export function validateJwt(req: NextApiRequest): boolean {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return false;
  }

  const token = authHeader.substring(7);
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    return true;
  } catch (error) {
    return false;
  }
}

// Generate token (admin endpoint)
export function generateToken(payload: any): string {
  return jwt.sign(payload, process.env.JWT_SECRET, { 
    expiresIn: '24h' 
  });
}
```

### Step 4: Update Code Usage

#### Old Code (Web Automation)
```python
# Old approach with WordPress
from modules.blog_automation.content_publisher import WordPressPublisher

wp_publisher = WordPressPublisher(
    url="https://yourblog.com",
    username="your_username",
    password="your_password"
)

result = wp_publisher.publish_post(
    title="AI Generated Blog",
    content="Content here...",
    tags=["ai", "tech"]
)
```

#### New Code (API Integration)
```python
# New approach with Next.js API
from modules.blog_automation.content_publisher import NextJSAPIPublisher

# Initialize with Next.js settings
publisher = NextJSAPIPublisher(
    api_url=settings.NEXTJS_BLOG_API,
    api_key=settings.NEXTJS_API_KEY
)

# Create draft first (recommended for testing)
draft_result = publisher.create_draft(
    title="AI Generated Blog",
    content="Content here...",
    tags=["ai", "tech"],
    seo_title="AI Blog: Complete Guide 2025",
    seo_description="Learn about AI automation in content creation"
)

if draft_result['success']:
    print(f"✅ Draft created: {draft_result['post_id']}")
    
    # Later, publish when ready
    publisher.update_post(
        post_id=draft_result['post_id'],
        status="published"
    )
```

### Step 5: Update PublisherManager Usage

#### Old Configuration
```python
# Old publisher manager setup
manager = PublisherManager()
manager.add_wordpress_publisher("my_blog", "https://blog.com", "user", "pass")
manager.add_medium_publisher("my_medium", "medium_token")

# Publish to all platforms
results = manager.publish_to_all(
    title="Blog Post",
    content="Content...",
    tags=["tech"]
)
```

#### New Configuration
```python
# New publisher manager setup
manager = PublisherManager()

# Primary: Next.js API
manager.add_nextjs_publisher(
    name="nextjs_site",
    api_url="https://your-site.com/api/blogs",
    api_key="your_api_key"
)

# Optional: Keep legacy platforms
manager.add_wordpress_publisher("my_blog", "https://blog.com", "user", "pass")

# Publish to all platforms (or specific ones)
results = manager.publish_to_all(
    title="Blog Post",
    content="Content...",
    tags=["tech"],
    platforms=["nextjs_site"]  # Only publish to Next.js
)
```

### Step 6: Test the Migration

#### Test Script
```python
# test_migration.py
from modules.blog_automation.content_publisher import NextJSAPIPublisher
import logging

def test_nextjs_integration():
    logging.basicConfig(level=logging.INFO)
    
    publisher = NextJSAPIPublisher(
        api_url="https://your-site.com/api/blogs",
        api_key="your_api_key"
    )
    
    # Test 1: Create draft
    print("🧪 Testing draft creation...")
    draft_result = publisher.create_draft(
        title="Migration Test Post",
        content="""
# Migration Test

This is a test post to verify the Next.js API integration is working correctly.

## Test Results

- ✅ API connection successful
- ✅ Authentication working
- ✅ Content creation verified
        """,
        tags=["migration", "test", "nextjs"],
        category="Testing"
    )
    
    if draft_result['success']:
        print(f"✅ Draft created successfully: {draft_result['post_id']}")
        
        # Test 2: Update status
        print("🧪 Testing status update...")
        update_result = publisher.update_post(
            post_id=draft_result['post_id'],
            status="published"
        )
        
        if update_result['success']:
            print("✅ Status update successful")
            print("🎉 Migration test PASSED!")
        else:
            print(f"❌ Status update failed: {update_result['error']}")
    else:
        print(f"❌ Draft creation failed: {draft_result['error']}")
        print("💥 Migration test FAILED!")

if __name__ == "__main__":
    test_nextjs_integration()
```

#### Run Test
```bash
python test_migration.py
```

### Step 7: Remove Web Automation Dependencies

#### Remove Node.js (Optional)
```bash
# If you no longer need Node.js for other projects
sudo apt remove nodejs npm

# If you need it for other purposes, keep it
# Node.js is no longer required for the AI agent
```

#### Clean up Browser Drivers
```bash
# Remove any browser driver installations
# (These are no longer needed)
rm -rf ~/.cache/selenium/
rm -rf ~/.cache/ms-playwright/
```

### Step 8: Update Documentation

Update any internal documentation to reflect the new approach:

#### Before
- "Install Node.js for web automation"
- "Configure browser settings"
- "Use Selenium for publishing"

#### After
- "Configure Next.js API endpoints"
- "Set up API authentication"
- "Use direct HTTP requests for publishing"

## Rollback Plan

If you encounter issues during migration:

### Quick Rollback
1. **Revert Environment Variables**: Restore old settings
2. **Use Legacy Publishers**: Continue with WordPress/Medium temporarily
3. **Debug Separately**: Fix Next.js integration without affecting production

### Troubleshooting Steps
1. **Check API Endpoint**: Ensure your Next.js API is accessible
2. **Verify Authentication**: Test API key/token manually
3. **Review Logs**: Check detailed API logging
4. **Test Incrementally**: Start with simple API calls

## Performance Comparison

| Metric | Web Automation | Next.js API |
|--------|---------------|-------------|
| Setup Complexity | High (Node.js, drivers) | Low (API only) |
| Reliability | Medium (browser issues) | High (HTTP only) |
| Speed | Slow (DOM interaction) | Fast (direct API) |
| Debugging | Complex (browser logs) | Simple (HTTP logs) |
| Maintenance | High (browser updates) | Low (stable API) |

## Support

If you encounter issues:

1. **Check Logs**: Review `logs/agent.log` for detailed error messages
2. **Test API Manually**: Use curl or Postman to test your Next.js endpoints
3. **Enable Debug Mode**: Set `LOG_LEVEL=DEBUG` for detailed logging
4. **Validate Response**: Ensure your API returns proper JSON responses

## Next Steps After Migration

1. ✅ **Monitor Performance**: Watch for successful API calls and response times
2. ✅ **Optimize SEO**: Use the new SEO fields (seo_title, seo_description)
3. ✅ **Implement Analytics**: Track publishing success rates
4. ✅ **Scale Up**: Move from draft mode to production publishing
5. ✅ **Add Features**: Implement batch operations, content optimization, etc.

---

**Success!** You've successfully migrated from web automation to Next.js API integration. Your AI Automation Agent is now more reliable, faster, and easier to maintain.