# Session-Based Authentication Migration Guide

This guide helps you migrate from API key-based authentication to the new session-based authentication for Next.js blog publishing.

## Overview

### What Changed
- **Before**: API key authentication with `NEXTJS_API_KEY`
- **After**: Session-based authentication with `NEXTJS_ADMIN_SESSION`
- **Benefits**: Enhanced security, better compatibility with modern Next.js admin APIs

### Migration Timeline
- **API Key Authentication**: Still supported but deprecated
- **Session Authentication**: Recommended and primary method
- **Deprecation Notice**: API keys will be removed in future versions

## Step-by-Step Migration

### Step 1: Backup Current Configuration

```bash
# Backup your current .env file
cp .env .env.backup-$(date +%Y%m%d)

# Backup your current settings
grep NEXTJS .env > nextjs-backup.txt
```

### Step 2: Update Environment Variables

#### Remove Old Variables
Remove these lines from your `.env` file:
```bash
# REMOVE THESE LINES:
NEXTJS_API_KEY=your_old_api_key_here
# (Optional) NEXTJS_AUTH_HEADER=Authorization  # if set to Authorization
```

#### Add New Variables
Add these lines to your `.env` file:
```bash
# ADD THESE NEW LINES:
# Session-based Authentication (REQUIRED)
NEXTJS_ADMIN_SESSION='{"id":"admin-user-id","email":"admin@your-site.com","role":"admin"}'
NEXTJS_AUTH_HEADER=x-admin-session

# Keep existing variables:
NEXTJS_BLOG_API=https://your-nextjs-site.com/api/blogs
NEXTJS_API_TIMEOUT=30
```

### Step 3: Obtain Admin Session Data

You need to get the actual admin session data from your Next.js application:

#### Option A: From Next.js Admin Dashboard
1. Login to your Next.js admin panel
2. Navigate to user/session settings
3. Copy your admin session data (should be in JSON format)

#### Option B: From Database
```javascript
// Example query for Next.js database
db.users.findOne(
  { email: "admin@your-site.com", role: "admin" },
  { _id: 1, email: 1, role: 1 }
)
```

#### Option C: From Next.js Code
```javascript
// In your Next.js application
const session = await getServerSession(req, res, authOptions);
console.log({
  id: session.user.id,
  email: session.user.email,
  role: session.user.role
});
```

### Step 4: Configure Session Data

#### For celorisdesigns.com (Specific Example)
```bash
# Replace with actual values from your celorisdesigns.com admin account
NEXTJS_ADMIN_SESSION='{"id":"12345","email":"admin@celorisdesigns.com","role":"admin"}'
```

#### For General Next.js Sites
```bash
# Replace with your actual admin session data
NEXTJS_AUTH_HEADER=x-admin-session
NEXTJS_ADMIN_SESSION='{"id":"your-admin-id","email":"admin@yourdomain.com","role":"admin"}'
```

### Step 5: Update Python Code

#### If you create NextJSAPIPublisher manually:

**Before (Deprecated):**
```python
from modules.blog_automation.content_publisher import NextJSAPIPublisher

publisher = NextJSAPIPublisher(
    api_url="https://your-site.com/api/blogs",
    api_key="your_api_key"  # OLD METHOD
)
```

**After (Recommended):**
```python
from modules.blog_automation.content_publisher import NextJSAPIPublisher

publisher = NextJSAPIPublisher(
    api_url="https://your-site.com/api/blogs",
    admin_session='{"id":"admin-id","email":"admin@site.com","role":"admin"}',  # NEW METHOD
    auth_header="x-admin-session"
)
```

#### If you use PublisherManager:

**Before (Deprecated):**
```python
from modules.blog_automation.content_publisher import PublisherManager

manager = PublisherManager()
manager.add_nextjs_publisher('nextjs', api_url, api_key)  # OLD METHOD
```

**After (Recommended):**
```python
from modules.blog_automation.content_publisher import PublisherManager

manager = PublisherManager()
manager.add_nextjs_publisher('nextjs', api_url, admin_session)  # NEW METHOD
```

### Step 6: Test the Migration

#### Run the Session Integration Test
```bash
python test_session_nextjs_integration.py
```

#### Manual Test
```python
from config.settings import settings
from modules.blog_automation.content_publisher import NextJSAPIPublisher

# Test with draft mode first
publisher = NextJSAPIPublisher(
    api_url=settings.NEXTJS_BLOG_API,
    admin_session=settings.NEXTJS_ADMIN_SESSION,
    auth_header=settings.NEXTJS_AUTH_HEADER
)

result = publisher.create_draft(
    title="Test Migration Post",
    content="Testing session-based authentication migration.",
    status="draft"
)

print("Migration test result:", result)
```

### Step 7: Verify Compatibility

#### Check Required Fields
Ensure your Next.js API accepts these blog post fields:
```json
{
  "title": "Blog Post Title",
  "content": "Full blog content",
  "excerpt": "Brief description (150-200 chars)",
  "slug": "url-friendly-slug",
  "status": "draft",
  "tags": ["tag1", "tag2"],
  "category": "Technology",
  "featured_image": "https://example.com/image.jpg"
}
```

#### Expected API Response
```json
{
  "success": true,
  "blog": {
    "id": 1,
    "title": "Blog Post Title",
    "slug": "blog-post-slug",
    "status": "draft",
    "created_at": "2025-11-22T15:13:12Z"
  }
}
```

## Troubleshooting Migration Issues

### Issue 1: Authentication Failed (401)
**Symptom**: `Authentication failed - check session data`

**Solutions**:
```bash
# Verify session JSON format
python -c "import json; print(json.loads('your-session-json'))"

# Check admin role permissions
# Ensure the admin session has publish permissions

# Verify session hasn't expired
# Regenerate session if needed
```

### Issue 2: Invalid JSON Session
**Symptom**: `NEXTJS_ADMIN_SESSION is not valid JSON`

**Solutions**:
```bash
# Validate JSON format
echo '{"id":"123","email":"admin@site.com","role":"admin"}' | python -m json.tool

# Common JSON errors:
# ❌ Missing quotes: {id:123, email:admin@site.com}
# ✅ Correct: {"id":"123","email":"admin@site.com","role":"admin"}

# ❌ Trailing commas: {"id":"123","email":"admin@site.com",}
# ✅ Correct: {"id":"123","email":"admin@site.com","role":"admin"}
```

### Issue 3: API Returns 400 Bad Request
**Symptom**: `Validation Error: missing required field`

**Solutions**:
```python
# Ensure all required fields are included
blog_data = {
    'title': title,
    'content': content,
    'status': status,
    'excerpt': excerpt or content[:150],  # Required
    'slug': slug or generate_slug(title)  # Required
}
```

### Issue 4: Headers Not Sent Correctly
**Symptom**: API doesn't receive authentication

**Solutions**:
```python
# Verify headers are set correctly
headers = {
    'Content-Type': 'application/json',
    'x-admin-session': admin_session  # Verify header name
}
```

## Migration Checklist

- [ ] **Backup Configuration**: Current .env and settings backed up
- [ ] **Remove API Key**: `NEXTJS_API_KEY` removed from .env
- [ ] **Add Session Config**: `NEXTJS_ADMIN_SESSION` added to .env
- [ ] **Update Auth Header**: `NEXTJS_AUTH_HEADER=x-admin-session`
- [ ] **Get Real Session**: Admin session data obtained from Next.js
- [ ] **Update Code**: Python code updated to use session auth
- [ ] **Test Integration**: Session test script passes
- [ ] **Test Publishing**: Draft/publish workflow works
- [ ] **Monitor Logs**: No authentication errors in logs
- [ ] **Production Ready**: Ready for production use

## Rollback Plan

If migration fails, you can rollback:

```bash
# 1. Restore backup configuration
cp .env.backup-YYYYMMDD .env

# 2. Temporarily use deprecated API key method
from modules.blog_automation.content_publisher import PublisherManager
manager = PublisherManager()
manager.add_nextjs_publisher_api_key('nextjs', api_url, api_key)

# 3. Investigate and retry migration
# 4. When ready, follow migration steps again
```

## Code Examples

### Complete Migration Example
```python
#!/usr/bin/env python3
"""
Migration example: API key to session authentication
"""

import os
from config.settings import settings
from modules.blog_automation.content_publisher import NextJSAPIPublisher, PublisherManager

def migrate_to_session_auth():
    """Migrate to session-based authentication"""
    
    # Verify configuration
    if not settings.NEXTJS_ADMIN_SESSION:
        print("❌ NEXTJS_ADMIN_SESSION not configured")
        return False
    
    # Create publisher with session auth
    try:
        publisher = NextJSAPIPublisher(
            api_url=settings.NEXTJS_BLOG_API,
            admin_session=settings.NEXTJS_ADMIN_SESSION,
            auth_header=settings.NEXTJS_AUTH_HEADER
        )
        
        # Test with draft
        result = publisher.create_draft(
            title="Migration Test Post",
            content="Testing session-based authentication migration.",
            status="draft"
        )
        
        if result['success']:
            print("✅ Migration successful!")
            print(f"   Draft ID: {result['post_id']}")
            
            # Optional: Clean up test post
            # publisher.update_post(result['post_id'], status="deleted")
            
            return True
        else:
            print(f"❌ Migration failed: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

if __name__ == "__main__":
    success = migrate_to_session_auth()
    if success:
        print("\n🎉 Migration completed successfully!")
        print("🚀 You can now use session-based authentication")
    else:
        print("\n⚠️ Migration failed. Please check configuration and try again.")
```

## Support Resources

### Documentation
- [SETUP_GUIDE_UPDATED.md](SETUP_GUIDE_UPDATED.md) - Complete setup guide
- [Next.js Integration Guide](NEXTJS_INTEGRATION_GUIDE.md) - Next.js specific setup

### Testing Tools
- `test_session_nextjs_integration.py` - Session authentication test
- `python test_installation.py` - General installation test

### Getting Help
1. Check logs: `tail -f logs/agent.log`
2. Run diagnostics: `python test_session_nextjs_integration.py`
3. Verify configuration: Check all environment variables
4. Test API manually: Use curl to test Next.js endpoint

---

**Next Step**: Once migration is complete, you can proceed with implementing additional modules or use the enhanced blog automation features.
