"""
Blog Automation Example Script
Demonstrates how to use the blog automation module
"""
import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loguru import logger
from config.settings import settings
from modules.blog_automation.blog_generator import BlogGenerator
from modules.blog_automation.content_publisher import PublisherManager, NextJSAPIPublisher
from modules.blog_automation.blog_scheduler import BlogScheduler
from modules.blog_automation.blog_analytics import BlogAnalytics


def setup_logging():
    """Setup logging for the example"""
    logger.remove()  # Remove default handler
    logger.add(
        "logs/blog_automation_example.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="INFO"
    )
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | {message}",
        level="INFO"
    )


def demonstrate_blog_generation():
    """Demonstrate blog content generation"""
    logger.info("=== Blog Generation Demo ===")
    
    try:
        # Initialize blog generator
        generator = BlogGenerator()
        
        # Generate a single blog post
        logger.info("Generating blog post on 'Artificial Intelligence in Healthcare'")
        blog_post = generator.generate_blog(
            topic="Artificial Intelligence in Healthcare",
            max_words=600,
            target_audience="medical professionals",
            style="informative"
        )
        
        logger.info(f"Generated blog: '{blog_post['title']}'")
        logger.info(f"Word count: {blog_post['word_count']}")
        logger.info(f"Tags: {', '.join(blog_post['tags'])}")
        logger.info(f"SEO Score: {generator.optimize_for_seo(blog_post['content'], blog_post['tags'])['seo_score']}")
        
        # Show content preview
        content_preview = blog_post['content'][:300] + "..."
        logger.info(f"Content preview:\n{content_preview}")
        
        return blog_post
        
    except Exception as e:
        logger.error(f"Blog generation failed: {e}")
        return None


def demonstrate_blog_series():
    """Demonstrate blog series generation"""
    logger.info("=== Blog Series Generation Demo ===")
    
    try:
        generator = BlogGenerator()
        
        # Generate a 3-post series
        logger.info("Generating blog series on 'Python Programming'")
        blog_series = generator.generate_blog_series(
            main_topic="Python Programming for Beginners",
            num_posts=3
        )
        
        logger.info(f"Generated {len(blog_series)} blog posts in series")
        
        for i, blog in enumerate(blog_series, 1):
            logger.info(f"Post {i}: {blog['title']} ({blog['word_count']} words)")
        
        return blog_series
        
    except Exception as e:
        logger.error(f"Blog series generation failed: {e}")
        return []


def demonstrate_nextjs_integration():
    """Demonstrate Next.js API integration with session-based authentication"""
    logger.info("=== Next.js Integration Demo ===")
    
    try:
        # Check if Next.js settings are configured (session-based)
        if not settings.NEXTJS_BLOG_API or not settings.NEXTJS_ADMIN_SESSION:
            logger.warning("⚠️  Next.js integration not configured!")
            logger.info("📝 To enable Next.js integration, set in .env:")
            logger.info("   NEXTJS_BLOG_API=https://your-site.com/api/blogs")
            logger.info("   NEXTJS_ADMIN_SESSION='{\"id\":\"admin-id\",\"email\":\"admin@site.com\",\"role\":\"admin\"}'")
            logger.info("   NEXTJS_AUTH_HEADER=x-admin-session")
            return None
        
        # Initialize Next.js publisher with session-based authentication
        nextjs_publisher = NextJSAPIPublisher(
            api_url=settings.NEXTJS_BLOG_API,
            admin_session=settings.NEXTJS_ADMIN_SESSION,
            auth_header=settings.NEXTJS_AUTH_HEADER
        )
        
        logger.info("✅ Next.js publisher initialized successfully (Session-based auth)")
        
        # Test connection (dry run - doesn't publish)
        logger.info("🔍 Testing API connection...")
        
        # Example blog data for testing
        test_blog_data = {
            "title": "AI Automation: The Future of Content Creation",
            "content": """
# The Future of AI-Powered Content Creation

Artificial Intelligence is revolutionizing how we create and manage content. With advanced automation tools, content creators can focus on strategy while AI handles the heavy lifting.

## Key Benefits

- **Efficiency**: Generate high-quality content in minutes
- **Consistency**: Maintain brand voice across all platforms  
- **Scalability**: Produce content at scale without sacrificing quality
- **SEO Optimization**: AI understands search patterns

## Getting Started

Start with a single platform and gradually expand your automation capabilities.
            """,
            "tags": ["ai", "automation", "content-creation", "technology"],
            "category": "Technology",
            "seo_title": "AI Content Creation: Automation Guide 2025",
            "seo_description": "Discover how AI automation is transforming content creation and helping businesses scale their content strategy efficiently."
        }
        
        logger.info("📝 Test blog post prepared")
        logger.info(f"   Title: {test_blog_data['title']}")
        logger.info(f"   Category: {test_blog_data['category']}")
        logger.info(f"   Tags: {', '.join(test_blog_data['tags'])}")
        
        # Show usage examples
        logger.info("\n🚀 Usage Examples:")
        logger.info("1. Create as draft (recommended for testing):")
        logger.info("   draft_result = nextjs_publisher.create_draft(title, content, **kwargs)")
        logger.info("   if draft_result['success']:")
        logger.info("       print('Draft created:', draft_result['post_id'])")
        
        logger.info("\n2. Direct publish (for production):")
        logger.info("   result = nextjs_publisher.publish_post(title, content, status='published')")
        
        logger.info("\n3. Update existing post:")
        logger.info("   update_result = nextjs_publisher.update_post(post_id, status='published')")
        
        logger.info("\n4. Publisher Manager integration:")
        logger.info("   manager = PublisherManager()")
        logger.info("   manager.add_nextjs_publisher('nextjs_site', api_url, api_key)")
        logger.info("   results = manager.publish_to_all(title, content, platforms=['nextjs_site'])")
        
        return nextjs_publisher
        
    except Exception as e:
        logger.error(f"❌ Next.js integration setup failed: {e}")
        logger.info("🔧 Troubleshooting:")
        logger.info("1. Check NEXTJS_BLOG_API URL is correct and accessible")
        logger.info("2. Verify NEXTJS_ADMIN_SESSION is valid JSON with id, email, role")
        logger.info("3. Ensure NEXTJS_AUTH_HEADER is set to 'x-admin-session'")
        logger.info("4. Test admin session has proper permissions on Next.js site")
        return None


def demonstrate_publishing_setup():
    """Demonstrate publisher setup (with Next.js as primary)"""
    logger.info("=== Publisher Setup Demo ===")
    
    publisher_manager = PublisherManager()
    
    # Note: In a real scenario, you would configure these with actual credentials
    logger.info("Publisher Manager initialized")
    logger.info("Available publishers:")
    
    # Next.js integration (recommended)
    logger.info("  - nextjs (PRIMARY - Recommended for Next.js sites)")
    logger.info("  - wordpress (Legacy - For WordPress sites)")
    logger.info("  - medium (Legacy - For Medium publications)")
    logger.info("  - custom_website (Generic - For any REST API)")
    
    logger.info("\n🔧 To add publishers, use:")
    logger.info("# Recommended: Next.js API integration (Session-based)")
    logger.info("publisher_manager.add_nextjs_publisher('nextjs_site', 'https://your-site.com/api/blogs', '{\"id\":\"admin-id\",\"email\":\"admin@site.com\",\"role\":\"admin\"}')")
    logger.info("")
    logger.info("# Legacy: Next.js API integration (API key - deprecated)")
    logger.info("publisher_manager.add_nextjs_publisher_api_key('nextjs_site', 'https://your-site.com/api/blogs', 'your_api_key')")
    
    logger.info("\n# Legacy platforms (optional)")
    logger.info("publisher_manager.add_wordpress_publisher('main', 'https://yoursite.com', 'user', 'password')")
    logger.info("publisher_manager.add_medium_publisher('main', 'your_medium_token')")
    logger.info("publisher_manager.add_custom_publisher('custom', 'https://api.site.com', 'api_key')")
    
    return publisher_manager


def demonstrate_scheduler():
    """Demonstrate blog scheduler setup"""
    logger.info("=== Blog Scheduler Demo ===")
    
    try:
        scheduler = BlogScheduler()
        
        # Configure publishers (in real scenario, add actual credentials)
        logger.info("Scheduler initialized")
        
        # Schedule a daily blog generation (for demo, using test configuration)
        topics = ["AI trends", "Web development", "Python programming", "Data science"]
        
        success = scheduler.schedule_daily_blog_generation(
            topics=topics,
            max_words=800,
            publish_immediately=False,  # Don't publish in demo
            time_str="09:00"
        )
        
        if success:
            logger.info("Successfully scheduled daily blog generation")
            
            # Show scheduled jobs
            jobs = scheduler.get_scheduled_jobs()
            logger.info(f"Scheduled jobs: {len(jobs)}")
            
            # Get statistics
            stats = scheduler.get_statistics()
            logger.info(f"Scheduler statistics: {stats}")
            
        return scheduler
        
    except Exception as e:
        logger.error(f"Scheduler setup failed: {e}")
        return None


def demonstrate_analytics():
    """Demonstrate blog analytics"""
    logger.info("=== Blog Analytics Demo ===")
    
    try:
        analytics = BlogAnalytics()
        
        # Track a demo blog post
        demo_post_id = f"demo_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        success = analytics.track_blog_post(
            post_id=demo_post_id,
            title="Demo Blog Post: AI Automation",
            platform="demo",
            url="https://example.com/demo-post"
        )
        
        if success:
            logger.info(f"Tracked demo blog post: {demo_post_id}")
            
            # Update engagement metrics
            metrics_update = analytics.update_engagement_metrics(
                post_id=demo_post_id,
                platform="demo",
                metrics={
                    'views': 250,
                    'likes': 18,
                    'shares': 7,
                    'comments': 4,
                    'engagement_rate': 11.6,
                    'time_spent': 180.5,  # seconds
                    'bounce_rate': 0.35
                }
            )
            
            logger.info(f"Updated engagement metrics: {metrics_update}")
            
            # Generate performance report
            report = analytics.generate_performance_report(days=30)
            logger.info("Generated performance report:")
            logger.info(report)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Analytics demo failed: {e}")
        return None


def demonstrate_seo_analysis():
    """Demonstrate SEO analysis"""
    logger.info("=== SEO Analysis Demo ===")
    
    try:
        analytics = BlogAnalytics()
        
        # Analyze a demo URL (this would fail in real scenario without actual URL)
        demo_url = "https://example.com/demo-post"
        
        logger.info(f"SEO analysis would be performed on: {demo_url}")
        logger.info("SEO analysis features include:")
        logger.info("  - Meta title and description validation")
        logger.info("  - H1 tag structure analysis")
        logger.info("  - Image alt tag checking")
        logger.info("  - Word count and readability scoring")
        logger.info("  - Performance and accessibility metrics")
        logger.info("  - SEO recommendations")
        
        # Show example of what SEO analysis would look like
        example_analysis = {
            'meta_title': 'Demo Post: AI Automation Guide',
            'meta_description': 'Learn about AI automation and its applications in modern technology.',
            'h1_tags': ['AI Automation Guide'],
            'word_count': 850,
            'seo_score': 85,
            'readability_score': 78,
            'performance_score': 92,
            'accessibility_score': 88,
            'recommendations': [
                'Consider adding more internal links',
                'Optimize image alt text for better accessibility',
                'Add more subheadings to improve structure'
            ]
        }
        
        logger.info("Example SEO analysis results:")
        for key, value in example_analysis.items():
            if key != 'recommendations':
                logger.info(f"  {key}: {value}")
            else:
                logger.info(f"  {key}:")
                for rec in value:
                    logger.info(f"    - {rec}")
        
        return analytics
        
    except Exception as e:
        logger.error(f"SEO analysis demo failed: {e}")
        return None


def main():
    """Main demonstration function"""
    print("=" * 60)
    print("BLOG AUTOMATION MODULE DEMONSTRATION")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    logger.info("Starting blog automation demonstration")
    
    # Check if we have required environment variables
    if not settings.OPENAI_API_KEY:
        logger.warning("OPENAI_API_KEY not set. Some features may not work properly.")
        logger.info("Set OPENAI_API_KEY in your .env file to enable AI generation.")
    
    try:
        # 1. Blog Generation Demo
        blog_post = demonstrate_blog_generation()
        
        # 2. Blog Series Demo
        blog_series = demonstrate_blog_series()
        
        # 3. Publisher Setup Demo
        publisher_manager = demonstrate_publishing_setup()
        
        # 4. Next.js Integration Demo (NEW)
        nextjs_publisher = demonstrate_nextjs_integration()
        
        # 5. Scheduler Demo
        scheduler = demonstrate_scheduler()
        
        # 5. Analytics Demo
        analytics = demonstrate_analytics()
        
        # 6. SEO Analysis Demo
        seo_analytics = demonstrate_seo_analysis()
        
        # Summary
        logger.info("=== DEMONSTRATION COMPLETE ===")
        logger.info("Features demonstrated:")
        logger.info("✓ AI-powered blog content generation")
        logger.info("✓ Blog series creation")
        logger.info("✓ Multi-platform publishing setup")
        logger.info("✓ Next.js API integration (RECOMMENDED)")
        logger.info("✓ Automated scheduling")
        logger.info("✓ Performance analytics")
        logger.info("✓ SEO optimization")
        
        logger.info("\n🚀 Next.js Integration (Recommended):")
        if nextjs_publisher:
            logger.info("✅ Next.js integration configured and ready")
            logger.info("📝 Use NextJSAPIPublisher for direct API publishing")
            logger.info("🔄 Consider using draft mode for testing")
        else:
            logger.info("⚠️  Next.js integration not configured")
            logger.info("📝 Set NEXTJS_BLOG_API and NEXTJS_API_KEY in .env")
        
        logger.info("\nTo use this module in production:")
        logger.info("1. Set up your environment variables in .env")
        logger.info("2. Configure your database connection")
        logger.info("3. Configure Next.js API integration (recommended)")
        logger.info("4. Optionally add legacy platform credentials (WordPress/Medium)")
        logger.info("5. Customize topics and scheduling preferences")
        logger.info("6. Start the scheduler for automated publishing")
        
    except Exception as e:
        logger.error(f"Demonstration failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    # Create necessary directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Run the demonstration
    success = main()
    
    if success:
        print("\n✓ Blog automation demonstration completed successfully!")
    else:
        print("\n✗ Demonstration encountered errors. Check logs for details.")
    
    # Keep the script running briefly to show logs
    import time
    time.sleep(1)
