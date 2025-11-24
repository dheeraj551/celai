#!/usr/bin/env python3
"""
Next.js Integration Test Script
This script tests the Next.js API integration for the AI Automation Agent

MIGRATION NOTE:
We have successfully migrated from API key authentication to session-based authentication.
The system now uses NEXTJS_ADMIN_SESSION instead of NEXTJS_API_KEY for better security.
If you see "NEXTJS_API_KEY not configured" errors, this is EXPECTED and NORMAL - 
the system is now using the recommended session-based approach.

Configuration in .env.celorisdesigns:
- NEXTJS_BLOG_API=https://celorisdesigns.com/api/admin/blog
- NEXTJS_ADMIN_SESSION='{"id":"admin-user-id","email":"admin@celorisdesigns.com","role":"admin"}'
- NEXTJS_AUTH_HEADER=x-admin-session
"""
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config.settings import settings
from modules.blog_automation.content_publisher import NextJSAPIPublisher

def setup_logging():
    """Setup logging for testing"""
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{function}</cyan> | {message}",
        level="INFO"
    )
    logger.add(
        "logs/nextjs_integration_test.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="DEBUG"
    )

def test_configuration():
    """Test if Next.js integration is configured"""
    logger.info("🔧 Testing Configuration...")
    
    # Check required environment variables
    if not settings.NEXTJS_BLOG_API:
        logger.error("❌ NEXTJS_BLOG_API not configured")
        return False
    
    # Check for session-based authentication (RECOMMENDED)
    if settings.NEXTJS_ADMIN_SESSION:
        logger.info("✅ Using SESSION-BASED authentication (RECOMMENDED)")
        logger.info(f"✅ API URL: {settings.NEXTJS_BLOG_API}")
        logger.info(f"✅ Admin Session: {'*' * 20 + settings.NEXTJS_ADMIN_SESSION[-10:] if len(settings.NEXTJS_ADMIN_SESSION) > 30 else 'Configured'}")
        logger.info(f"✅ Auth Header: {settings.NEXTJS_AUTH_HEADER}")
        logger.info(f"✅ Timeout: {settings.NEXTJS_API_TIMEOUT}s")
        return True
    
    # Check for legacy API key authentication (DEPRECATED)
    elif settings.NEXTJS_API_KEY:
        logger.warning("⚠️  Using LEGACY API KEY authentication (DEPRECATED)")
        logger.warning("💡 Migrate to session-based authentication for better security")
        logger.info(f"✅ API URL: {settings.NEXTJS_BLOG_API}")
        logger.info(f"✅ API Key: {'*' * (len(settings.NEXTJS_API_KEY) - 4) + settings.NEXTJS_API_KEY[-4:] if len(settings.NEXTJS_API_KEY) > 4 else '***'}")
        logger.info(f"✅ Auth Header: {settings.NEXTJS_AUTH_HEADER}")
        logger.info(f"✅ Timeout: {settings.NEXTJS_API_TIMEOUT}s")
        return True
    else:
        logger.error("❌ No authentication configured")
        logger.error("💡 Configure NEXTJS_ADMIN_SESSION for session-based auth")
        return False

def test_api_connection():
    """Test API connection (dry run)"""
    logger.info("🔍 Testing API Connection...")
    
    try:
        # Initialize publisher with session-based authentication
        publisher = NextJSAPIPublisher(
            api_url=settings.NEXTJS_BLOG_API,
            admin_session=settings.NEXTJS_ADMIN_SESSION,
            auth_header=settings.NEXTJS_AUTH_HEADER
        )
        
        logger.info("✅ Publisher initialized successfully with session-based auth")
        return publisher
        
    except Exception as e:
        logger.error(f"❌ API connection failed: {e}")
        return None

def test_draft_creation(publisher):
    """Test creating a draft blog post"""
    logger.info("📝 Testing Draft Creation...")
    
    # Create test blog data
    test_data = {
        "title": f"AI Automation Test Post {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "content": """
# Next.js Integration Test

This is a test post to verify the AI Automation Agent can successfully create drafts via API.

## Test Results

✅ Configuration valid
✅ API connection successful  
✅ Authentication working
✅ Draft creation tested

## Conclusion

The Next.js integration is working correctly!
        """,
        "tags": ["test", "integration", "nextjs", "automation"],
        "category": "Testing",
        "seo_title": "Next.js Integration Test - AI Automation Agent",
        "seo_description": "Testing the Next.js API integration for the AI Automation Agent"
    }
    
    try:
        # Create draft
        result = publisher.create_draft(**test_data)
        
        if result['success']:
            logger.info(f"✅ Draft created successfully!")
            logger.info(f"   Post ID: {result['post_id']}")
            if result.get('url'):
                logger.info(f"   URL: {result['url']}")
            if result.get('api_response_time'):
                logger.info(f"   Response time: {result['api_response_time']:.2f}s")
            return result['post_id']
        else:
            logger.error(f"❌ Draft creation failed: {result.get('error', 'Unknown error')}")
            return None
            
    except Exception as e:
        logger.error(f"❌ Draft creation exception: {e}")
        return None

def test_status_update(publisher, post_id):
    """Test updating post status"""
    logger.info("🔄 Testing Status Update...")
    
    try:
        # Update status to published
        result = publisher.update_post(
            post_id=post_id,
            status="published"
        )
        
        if result['success']:
            logger.info(f"✅ Status updated successfully!")
            logger.info(f"   Post ID: {result['post_id']}")
            return True
        else:
            logger.error(f"❌ Status update failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Status update exception: {e}")
        return False

def cleanup_test_post(publisher, post_id):
    """Clean up test post (optional)"""
    logger.info("🧹 Cleaning up test post...")
    
    try:
        # In a real scenario, you might want to delete the test post
        # For now, we'll just leave it as a draft or published
        logger.info(f"Test post {post_id} left as-is for manual review")
        logger.info("   You can delete it manually if needed")
        return True
        
    except Exception as e:
        logger.warning(f"⚠️  Cleanup warning: {e}")
        return False

def run_integration_test():
    """Run the complete Next.js integration test"""
    logger.info("🚀 Starting Next.js Integration Test")
    logger.info("=" * 50)
    
    # Step 1: Test configuration
    if not test_configuration():
        logger.error("💥 Configuration test failed - aborting test")
        return False
    
    logger.info("")
    
    # Step 2: Test API connection
    publisher = test_api_connection()
    if not publisher:
        logger.error("💥 API connection test failed - aborting test")
        return False
    
    logger.info("")
    
    # Step 3: Test draft creation
    post_id = test_draft_creation(publisher)
    if not post_id:
        logger.error("💥 Draft creation test failed - aborting test")
        return False
    
    logger.info("")
    
    # Step 4: Test status update
    success = test_status_update(publisher, post_id)
    if not success:
        logger.warning("⚠️  Status update test failed, but draft was created")
    
    logger.info("")
    
    # Step 5: Cleanup (optional)
    cleanup_test_post(publisher, post_id)
    
    logger.info("")
    logger.info("🎉 Integration Test Complete!")
    logger.info("=" * 50)
    
    if success:
        logger.info("✅ ALL TESTS PASSED!")
        logger.info("✅ Next.js integration is working correctly")
        logger.info("🚀 You can now use NextJSAPIPublisher in production")
        logger.info("")
        logger.info("Next steps:")
        logger.info("1. Review the test post in your Next.js admin/dashboard")
        logger.info("2. If satisfied, delete the test post")
        logger.info("3. Configure automated scheduling")
        logger.info("4. Start using the agent for production content")
        return True
    else:
        logger.warning("⚠️  Some tests failed")
        logger.info("🔧 Check the logs for specific error messages")
        logger.info("📝 Review your Next.js API implementation")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("NEXT.JS INTEGRATION TEST")
    print("=" * 60)
    print("This script tests the Next.js API integration")
    print("for the AI Automation Agent")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    
    try:
        # Run the integration test
        success = run_integration_test()
        
        if success:
            print("\n🎉 Integration test completed successfully!")
            print("✅ Next.js API integration is working correctly")
            return 0
        else:
            print("\n⚠️  Integration test completed with warnings")
            print("🔧 Check the logs for specific error details")
            return 1
            
    except KeyboardInterrupt:
        logger.info("\n⏹️  Test interrupted by user")
        return 130
    except Exception as e:
        logger.error(f"💥 Unexpected error during test: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)