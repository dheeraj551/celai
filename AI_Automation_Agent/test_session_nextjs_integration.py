#!/usr/bin/env python3
"""
Test Script for Next.js Session-Based Authentication Integration
This script tests the session-based authentication for Next.js blog publishing
"""

import os
import sys
import json
import requests
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.settings import settings
from modules.blog_automation.content_publisher import NextJSAPIPublisher


def test_session_configuration():
    """Test if session-based configuration is properly set"""
    print("🔍 Testing Session Configuration...")
    
    errors = []
    
    # Check required environment variables
    if not settings.NEXTJS_BLOG_API:
        errors.append("NEXTJS_BLOG_API not configured")
    else:
        print(f"✅ API URL: {settings.NEXTJS_BLOG_API}")
    
    if not settings.NEXTJS_ADMIN_SESSION:
        errors.append("NEXTJS_ADMIN_SESSION not configured")
    else:
        try:
            session_data = json.loads(settings.NEXTJS_ADMIN_SESSION)
            print(f"✅ Admin Session: {session_data}")
            
            # Validate session structure
            required_fields = ["id", "email", "role"]
            missing_fields = [field for field in required_fields if field not in session_data]
            if missing_fields:
                errors.append(f"Session missing required fields: {missing_fields}")
        except json.JSONDecodeError:
            errors.append("NEXTJS_ADMIN_SESSION is not valid JSON")
    
    if not settings.NEXTJS_AUTH_HEADER:
        print("⚠️ Using default auth header: x-admin-session")
    else:
        print(f"✅ Auth Header: {settings.NEXTJS_AUTH_HEADER}")
    
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    else:
        print("✅ Session configuration is valid")
        return True


def test_nextjs_api_connection():
    """Test connection to Next.js API"""
    print("\n🌐 Testing Next.js API Connection...")
    
    try:
        # Test with simple GET request
        headers = {
            settings.NEXTJS_AUTH_HEADER: settings.NEXTJS_ADMIN_SESSION,
            'Accept': 'application/json',
            'User-Agent': 'AI-Automation-Agent/2.0'
        }
        
        response = requests.get(
            settings.NEXTJS_BLOG_API,
            headers=headers,
            timeout=10
        )
        
        print(f"✅ API Connection Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API is accessible and responding")
            return True
        elif response.status_code == 401:
            print("❌ Authentication failed - check session data")
            return False
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - check API URL and network")
        return False
    except requests.exceptions.Timeout:
        print("⏰ Connection timeout - API may be slow")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


def test_publisher_initialization():
    """Test NextJSAPIPublisher initialization with session auth"""
    print("\n🤖 Testing Publisher Initialization...")
    
    try:
        publisher = NextJSAPIPublisher(
            api_url=settings.NEXTJS_BLOG_API,
            admin_session=settings.NEXTJS_ADMIN_SESSION,
            auth_header=settings.NEXTJS_AUTH_HEADER
        )
        
        print("✅ Publisher initialized successfully")
        print(f"   API URL: {publisher.api_url}")
        print(f"   Auth Header: {publisher.auth_header}")
        return publisher
        
    except Exception as e:
        print(f"❌ Publisher initialization failed: {e}")
        return None


def test_blog_structure():
    """Test blog post data structure"""
    print("\n📝 Testing Blog Post Structure...")
    
    # Sample blog post data with all recommended fields
    sample_blog = {
        "title": "Test Blog Post - AI Automation Agent",
        "content": """
# AI Automation Test Post

This is a test blog post created by the AI Automation Agent to verify 
the session-based authentication integration with Next.js.

## Testing Features

- Session-based authentication
- Enhanced blog post structure
- Draft/publish workflow
- Error handling

## Expected Behavior

The post should be created as a draft for testing purposes.
        """,
        "excerpt": "This is a test blog post created by the AI Automation Agent to verify session-based authentication integration with Next.js.",
        "slug": "test-blog-post-ai-automation",
        "featured_image": "https://celorisdesigns.com/images/test-blog.jpg",
        "status": "draft",
        "tags": ["ai", "automation", "test", "nextjs"],
        "category": "Technology",
        "seo_title": "AI Automation Agent - Session Authentication Test",
        "seo_description": "Testing session-based authentication for Next.js blog publishing with AI Automation Agent.",
        "author": "AI Automation Agent"
    }
    
    print("✅ Blog structure test data prepared")
    print(f"   Title: {sample_blog['title']}")
    print(f"   Slug: {sample_blog['slug']}")
    print(f"   Status: {sample_blog['status']}")
    print(f"   Tags: {', '.join(sample_blog['tags'])}")
    
    return sample_blog


def test_draft_creation(publisher, blog_data):
    """Test creating a draft blog post"""
    print("\n📄 Testing Draft Creation...")
    
    try:
        result = publisher.create_draft(
            title=blog_data['title'],
            content=blog_data['content'],
            excerpt=blog_data.get('excerpt'),
            slug=blog_data.get('slug'),
            featured_image=blog_data.get('featured_image'),
            tags=blog_data.get('tags'),
            category=blog_data.get('category'),
            seo_title=blog_data.get('seo_title'),
            seo_description=blog_data.get('seo_description')
        )
        
        print("📤 Draft Creation Result:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Post ID: {result.get('post_id', 'N/A')}")
        print(f"   URL: {result.get('url', 'N/A')}")
        
        if result.get('error'):
            print(f"   Error: {result['error']}")
        
        if result.get('api_response_time'):
            print(f"   Response Time: {result['api_response_time']:.2f}s")
        
        return result
        
    except Exception as e:
        print(f"❌ Draft creation failed: {e}")
        return {"success": False, "error": str(e)}


def test_publishing_with_session(publisher, blog_data):
    """Test publishing with session-based authentication"""
    print("\n🚀 Testing Direct Publishing...")
    
    try:
        # Modify for published status
        blog_data['status'] = 'published'
        
        result = publisher.publish_post(
            title=blog_data['title'] + " (Published Test)",
            content=blog_data['content'],
            excerpt=blog_data.get('excerpt'),
            slug=blog_data.get('slug') + "-published",
            featured_image=blog_data.get('featured_image'),
            tags=blog_data.get('tags'),
            category=blog_data.get('category'),
            seo_title=blog_data.get('seo_title'),
            seo_description=blog_data.get('seo_description')
        )
        
        print("📤 Publishing Result:")
        print(f"   Success: {result.get('success', False)}")
        print(f"   Post ID: {result.get('post_id', 'N/A')}")
        print(f"   URL: {result.get('url', 'N/A')}")
        print(f"   Published At: {result.get('published_at', 'N/A')}")
        
        if result.get('error'):
            print(f"   Error: {result['error']}")
        
        if result.get('api_response_time'):
            print(f"   Response Time: {result['api_response_time']:.2f}s")
        
        return result
        
    except Exception as e:
        print(f"❌ Publishing failed: {e}")
        return {"success": False, "error": str(e)}


def test_error_handling(publisher):
    """Test error handling with invalid session"""
    print("\n🛡️ Testing Error Handling...")
    
    try:
        # Test with invalid session
        invalid_session = '{"invalid": "data"}'
        invalid_publisher = NextJSAPIPublisher(
            api_url=settings.NEXTJS_BLOG_API,
            admin_session=invalid_session,
            auth_header=settings.NEXTJS_AUTH_HEADER
        )
        
        result = invalid_publisher.create_draft(
            title="Test with Invalid Session",
            content="This should fail due to invalid session data."
        )
        
        if not result.get('success'):
            print("✅ Error handling works correctly")
            print(f"   Expected error: {result.get('error', 'Unknown error')}")
            return True
        else:
            print("⚠️ Expected error but got success - check API validation")
            return False
            
    except Exception as e:
        print(f"✅ Error handling works: {e}")
        return True


def display_summary(results):
    """Display test summary"""
    print("\n" + "=" * 60)
    print("🎯 SESSION-BASED INTEGRATION TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Configuration", results.get('config', False)),
        ("API Connection", results.get('connection', False)),
        ("Publisher Init", results.get('publisher', False)),
        ("Draft Creation", results.get('draft', {}).get('success', False)),
        ("Publishing", results.get('publish', {}).get('success', False)),
        ("Error Handling", results.get('error_handling', False))
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print(f"\n📊 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Session-based authentication is working correctly")
        print("🚀 Ready for production use")
    else:
        print(f"\n⚠️ {total - passed} tests failed")
        print("🔧 Please check the configuration and try again")
    
    # Show specific recommendations
    print("\n💡 Recommendations:")
    if not results.get('config'):
        print("- Verify NEXTJS_ADMIN_SESSION is valid JSON with id, email, role")
    if not results.get('connection'):
        print("- Check NEXTJS_BLOG_API URL and network connectivity")
    if not results.get('draft', {}).get('success'):
        draft_error = results.get('draft', {}).get('error', '')
        if '401' in str(draft_error) or 'unauthorized' in str(draft_error).lower():
            print("- Verify admin session data is correct and has admin privileges")
        else:
            print("- Check API response format and required fields")
    
    print("\n📚 For more help, see:")
    print("- SETUP_GUIDE_UPDATED.md")
    print("- NEXTJS_INTEGRATION_GUIDE.md")


def main():
    """Main test execution"""
    print("🚀 Next.js Session-Based Authentication Test")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Test 1: Configuration
    results['config'] = test_session_configuration()
    
    if not results['config']:
        print("\n❌ Configuration issues detected. Please fix before continuing.")
        display_summary(results)
        return
    
    # Test 2: API Connection
    results['connection'] = test_nextjs_api_connection()
    
    # Test 3: Publisher Initialization
    if results['connection']:
        publisher = test_publisher_initialization()
        results['publisher'] = publisher is not None
    else:
        print("⚠️ Skipping publisher tests due to connection failure")
        publisher = None
        results['publisher'] = False
    
    # Test 4: Blog Structure
    blog_data = test_blog_structure()
    
    # Test 5: Draft Creation
    if publisher:
        results['draft'] = test_draft_creation(publisher, blog_data)
    else:
        results['draft'] = {"success": False, "error": "Publisher not initialized"}
    
    # Test 6: Publishing (optional - only if draft was successful)
    if publisher and results['draft'].get('success'):
        print("\n⚠️ Note: Skipping publish test. Draft creation successful.")
        results['publish'] = {"success": False, "skipped": True}
    else:
        results['publish'] = {"success": False, "skipped": True}
    
    # Test 7: Error Handling
    if publisher:
        results['error_handling'] = test_error_handling(publisher)
    else:
        results['error_handling'] = False
    
    # Display Summary
    display_summary(results)


if __name__ == "__main__":
    main()
