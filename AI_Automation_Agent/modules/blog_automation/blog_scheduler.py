"""
Blog Scheduler Module
Handles automated scheduling and publishing of blog posts
"""
import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from loguru import logger
import json
import queue

from config.settings import settings
from .blog_generator import BlogGenerator
from .content_publisher import PublisherManager
from config.database import get_collection

# Only import MySQL functions if using MySQL
if settings.DATABASE_TYPE.lower() == "mysql":
    from config.database import get_mysql_session, BlogPost
else:
    # For MongoDB, use None for MySQL-specific functions
    get_mysql_session = None
    BlogPost = None


class BlogScheduler:
    """
    Automated blog generation and publishing scheduler
    """
    
    def __init__(self):
        """Initialize the blog scheduler"""
        self.blog_generator = BlogGenerator()
        self.publisher_manager = PublisherManager()
        self.is_running = False
        self.scheduler_thread = None
        
        # Queue for scheduled tasks
        self.task_queue = queue.Queue()
        
        # Blog statistics
        self.stats = {
            'total_generated': 0,
            'total_published': 0,
            'failed_generations': 0,
            'failed_publications': 0,
            'last_generation': None,
            'last_publication': None
        }
        
        # Load saved statistics if available
        self._load_statistics()
        
        # Setup default publishers if configured
        self._setup_default_publishers()
    
    def _load_statistics(self):
        """Load statistics from database"""
        try:
            if settings.DATABASE_TYPE.lower() == "mongodb":
                collection = get_collection("blog_statistics")
                stats_doc = collection.find_one({"type": "scheduler_stats"})
                if stats_doc:
                    self.stats.update(stats_doc.get('stats', {}))
            else:
                # For MySQL, we'll store in a simple JSON file for now
                import os
                stats_file = "blog_stats.json"
                if os.path.exists(stats_file):
                    with open(stats_file, 'r') as f:
                        saved_stats = json.load(f)
                        self.stats.update(saved_stats)
        except Exception as e:
            logger.warning(f"Could not load statistics: {e}")
    
    def _save_statistics(self):
        """Save statistics to database"""
        try:
            if settings.DATABASE_TYPE.lower() == "mongodb":
                collection = get_collection("blog_statistics")
                collection.update_one(
                    {"type": "scheduler_stats"},
                    {"$set": {"stats": self.stats, "updated_at": datetime.now()}},
                    upsert=True
                )
            else:
                # For MySQL, save to JSON file
                import os
                stats_file = "blog_stats.json"
                with open(stats_file, 'w') as f:
                    json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.warning(f"Could not save statistics: {e}")
    
    def _setup_default_publishers(self):
        """Setup default publishers based on environment variables"""
        # WordPress publisher
        if hasattr(settings, 'WORDPRESS_URL') and settings.WORDPRESS_URL:
            try:
                self.publisher_manager.add_wordpress_publisher(
                    name="default_wordpress",
                    url=settings.WORDPRESS_URL,
                    username=settings.WORDPRESS_USERNAME,
                    password=settings.WORDPRESS_PASSWORD
                )
            except Exception as e:
                logger.error(f"Failed to setup WordPress publisher: {e}")
        
        # Medium publisher
        if hasattr(settings, 'MEDIUM_TOKEN') and settings.MEDIUM_TOKEN:
            try:
                self.publisher_manager.add_medium_publisher(
                    name="default_medium",
                    access_token=settings.MEDIUM_TOKEN
                )
            except Exception as e:
                logger.error(f"Failed to setup Medium publisher: {e}")
    
    def schedule_daily_blog_generation(self, topics: List[str], 
                                     max_words: int = 800,
                                     publish_immediately: bool = True,
                                     platforms: List[str] = None,
                                     time_str: str = "09:00") -> bool:
        """
        Schedule daily blog generation
        
        Args:
            topics: List of topics to rotate through
            max_words: Maximum word count for generated blogs
            publish_immediately: Whether to publish immediately
            platforms: List of platforms to publish to
            time_str: Time to generate blog (HH:MM format)
            
        Returns:
            Success status
        """
        try:
            def daily_blog_job():
                self._generate_and_publish_blog(
                    topics=topics,
                    max_words=max_words,
                    publish_immediately=publish_immediately,
                    platforms=platforms
                )
            
            schedule.every().day.at(time_str).do(daily_blog_job)
            logger.info(f"Scheduled daily blog generation at {time_str}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule daily blog generation: {e}")
            return False
    
    def schedule_weekly_blog_series(self, main_topic: str, 
                                  num_posts: int = 5,
                                  day_of_week: str = "monday",
                                  publish_immediately: bool = True,
                                  platforms: List[str] = None) -> bool:
        """
        Schedule weekly blog series generation
        
        Args:
            main_topic: Main topic for the series
            num_posts: Number of posts in series
            day_of_week: Day to generate series (monday, tuesday, etc.)
            publish_immediately: Whether to publish immediately
            platforms: List of platforms to publish to
            
        Returns:
            Success status
        """
        try:
            def weekly_series_job():
                self._generate_blog_series(
                    main_topic=main_topic,
                    num_posts=num_posts,
                    publish_immediately=publish_immediately,
                    platforms=platforms
                )
            
            schedule.every().week.on(getattr(schedule.every(), day_of_week.lower())).do(weekly_series_job)
            logger.info(f"Scheduled weekly blog series for {day_of_week}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule weekly blog series: {e}")
            return False
    
    def schedule_content_curation(self, sources: List[str], 
                                frequency_hours: int = 6,
                                max_articles: int = 10) -> bool:
        """
        Schedule content curation from various sources
        
        Args:
            sources: List of content sources to monitor
            frequency_hours: How often to check for new content
            max_articles: Maximum number of articles to curate
            
        Returns:
            Success status
        """
        try:
            def curation_job():
                self._curate_and_generate_content(
                    sources=sources,
                    max_articles=max_articles
                )
            
            schedule.every(frequency_hours).hours.do(curation_job)
            logger.info(f"Scheduled content curation every {frequency_hours} hours")
            return True
            
        except Exception as e:
            logger.error(f"Failed to schedule content curation: {e}")
            return False
    
    def _generate_and_publish_blog(self, topics: List[str], 
                                  max_words: int,
                                  publish_immediately: bool,
                                  platforms: List[str] = None) -> Dict:
        """
        Generate and optionally publish a blog post
        
        Args:
            topics: List of available topics
            max_words: Maximum word count
            publish_immediately: Whether to publish immediately
            platforms: Platforms to publish to
            
        Returns:
            Dictionary with generation and publishing results
        """
        try:
            # Select topic (rotate or random)
            topic = self._select_topic(topics)
            
            logger.info(f"Generating blog for topic: {topic}")
            
            # Generate blog content
            blog_data = self.blog_generator.generate_blog(
                topic=topic,
                max_words=max_words,
                target_audience="general",
                style="informative"
            )
            
            # Save to database
            self._save_blog_to_database(blog_data)
            
            # Update statistics
            self.stats['total_generated'] += 1
            self.stats['last_generation'] = datetime.now().isoformat()
            self._save_statistics()
            
            publish_result = {'success': False}
            
            # Publish if requested
            if publish_immediately:
                publish_result = self._publish_blog(blog_data, platforms)
            
            # Update statistics
            if publish_result['success']:
                self.stats['total_published'] += 1
                self.stats['last_publication'] = datetime.now().isoformat()
            else:
                self.stats['failed_publications'] += 1
            
            self._save_statistics()
            
            return {
                'generation_success': True,
                'publish_result': publish_result,
                'blog_data': blog_data
            }
            
        except Exception as e:
            logger.error(f"Failed to generate and publish blog: {e}")
            self.stats['failed_generations'] += 1
            self._save_statistics()
            return {
                'generation_success': False,
                'error': str(e)
            }
    
    def _generate_blog_series(self, main_topic: str, 
                            num_posts: int,
                            publish_immediately: bool,
                            platforms: List[str] = None) -> Dict:
        """
        Generate a series of related blog posts
        
        Args:
            main_topic: Main topic for the series
            num_posts: Number of posts in series
            publish_immediately: Whether to publish immediately
            platforms: Platforms to publish to
            
        Returns:
            Dictionary with series generation results
        """
        try:
            logger.info(f"Generating blog series: {main_topic} ({num_posts} posts)")
            
            # Generate series
            blog_series = self.blog_generator.generate_blog_series(
                main_topic=main_topic,
                num_posts=num_posts
            )
            
            results = []
            published_count = 0
            
            for i, blog_data in enumerate(blog_series, 1):
                try:
                    # Save to database
                    self._save_blog_to_database(blog_data)
                    
                    # Update statistics
                    self.stats['total_generated'] += 1
                    
                    # Publish if requested
                    if publish_immediately:
                        publish_result = self._publish_blog(blog_data, platforms)
                        
                        if publish_result['success']:
                            published_count += 1
                            self.stats['total_published'] += 1
                        else:
                            self.stats['failed_publications'] += 1
                    
                    results.append({
                        'post_number': i,
                        'generation_success': True,
                        'publish_result': publish_result if publish_immediately else None,
                        'blog_data': blog_data
                    })
                    
                    # Small delay between posts to avoid rate limiting
                    if publish_immediately and i < len(blog_series):
                        time.sleep(2)
                    
                except Exception as e:
                    logger.error(f"Failed to process post {i} in series: {e}")
                    results.append({
                        'post_number': i,
                        'generation_success': False,
                        'error': str(e)
                    })
                    self.stats['failed_generations'] += 1
            
            self.stats['last_generation'] = datetime.now().isoformat()
            self._save_statistics()
            
            return {
                'series_success': True,
                'total_posts': len(blog_series),
                'published_posts': published_count,
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Failed to generate blog series: {e}")
            return {
                'series_success': False,
                'error': str(e)
            }
    
    def _curate_and_generate_content(self, sources: List[str], max_articles: int) -> Dict:
        """
        Curate content from sources and generate related blog posts
        
        Args:
            sources: List of content sources
            max_articles: Maximum articles to process
            
        Returns:
            Dictionary with curation results
        """
        try:
            logger.info(f"Curating content from sources: {sources}")
            
            # This would integrate with web scraping or RSS feeds
            # For now, we'll simulate content curation
            
            curated_topics = self._extract_topics_from_sources(sources, max_articles)
            
            results = []
            for topic in curated_topics:
                try:
                    blog_result = self._generate_and_publish_blog(
                        topics=[topic],
                        max_words=600,  # Shorter for curated content
                        publish_immediately=False,  # Queue for review
                        platforms=None
                    )
                    
                    results.append({
                        'topic': topic,
                        'curation_result': blog_result
                    })
                    
                except Exception as e:
                    logger.error(f"Failed to curate and generate for topic {topic}: {e}")
                    results.append({
                        'topic': topic,
                        'error': str(e)
                    })
            
            return {
                'curation_success': True,
                'topics_found': len(curated_topics),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Failed to curate content: {e}")
            return {
                'curation_success': False,
                'error': str(e)
            }
    
    def _select_topic(self, topics: List[str]) -> str:
        """Select a topic from the list (implement rotation logic)"""
        if not topics:
            # Default topics if none provided
            topics = ["artificial intelligence", "technology trends", "programming", "web development"]
        
        # Simple round-robin selection
        import random
        return random.choice(topics)
    
    def _extract_topics_from_sources(self, sources: List[str], max_articles: int) -> List[str]:
        """Extract trending topics from content sources"""
        # This would integrate with news APIs, RSS feeds, etc.
        # For now, return some example trending topics
        
        trending_topics = [
            "AI in healthcare 2025",
            "Sustainable technology solutions",
            "Remote work technology",
            "Cybersecurity trends",
            "Cloud computing advances",
            "Machine learning applications",
            "Blockchain technology updates",
            "Internet of Things innovations"
        ]
        
        return trending_topics[:max_articles]
    
    def _save_blog_to_database(self, blog_data: Dict):
        """Save blog post to database"""
        try:
            if settings.DATABASE_TYPE.lower() == "mongodb":
                collection = get_collection("blog_posts")
                blog_data['saved_at'] = datetime.now()
                result = collection.insert_one(blog_data)
                logger.debug(f"Saved blog to MongoDB with ID: {result.inserted_id}")
                
            elif settings.DATABASE_TYPE.lower() == "mysql" and get_mysql_session and BlogPost:
                # MySQL implementation
                session = get_mysql_session()
                
                blog_post = BlogPost(
                    title=blog_data['title'],
                    content=blog_data['content'],
                    topic=blog_data.get('topic', 'general'),
                    status=blog_data.get('status', 'draft'),
                    word_count=blog_data.get('word_count', 0),
                    tags=json.dumps(blog_data.get('tags', [])),
                    is_auto_generated=True,
                    source_url=blog_data.get('source_url')
                )
                
                session.add(blog_post)
                session.commit()
                logger.debug(f"Saved blog to MySQL with ID: {blog_post.id}")
            else:
                logger.warning(f"Unsupported database type or missing MySQL dependencies: {settings.DATABASE_TYPE}")
                
        except Exception as e:
            logger.error(f"Failed to save blog to database: {e}")
            raise
    
    def _publish_blog(self, blog_data: Dict, platforms: List[str] = None) -> Dict:
        """Publish blog to specified platforms"""
        try:
            if not self.publisher_manager.publishers:
                logger.warning("No publishers configured")
                return {'success': False, 'error': 'No publishers configured'}
            
            # Use configured platforms or all publishers
            target_platforms = platforms or list(self.publisher_manager.publishers.keys())
            
            results = self.publisher_manager.publish_to_all(
                title=blog_data['title'],
                content=blog_data['content'],
                tags=blog_data.get('tags', []),
                platforms=target_platforms
            )
            
            # Check if any publication was successful
            successful_publications = sum(1 for result in results.values() if result.get('success', False))
            
            return {
                'success': successful_publications > 0,
                'successful_platforms': successful_publications,
                'total_platforms': len(target_platforms),
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Failed to publish blog: {e}")
            return {'success': False, 'error': str(e)}
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return
        
        self.is_running = True
        
        def scheduler_loop():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        
        self.scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        
        logger.info("Blog scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if not self.is_running:
            logger.warning("Scheduler is not running")
            return
        
        self.is_running = False
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        # Clear all scheduled jobs
        schedule.clear()
        
        logger.info("Blog scheduler stopped")
    
    def get_statistics(self) -> Dict:
        """Get scheduler statistics"""
        return {
            **self.stats,
            'is_running': self.is_running,
            'scheduled_jobs': len(schedule.jobs),
            'publishers_configured': len(self.publisher_manager.publishers)
        }
    
    def get_scheduled_jobs(self) -> List[Dict]:
        """Get list of scheduled jobs"""
        jobs = []
        for job in schedule.jobs:
            jobs.append({
                'next_run': job.next_run,
                'job_func': str(job.job_func),
                'interval': getattr(job, 'interval_unit', 'day')
            })
        return jobs
    
    def add_custom_job(self, job_func: Callable, schedule_config: Dict):
        """
        Add a custom scheduled job
        
        Args:
            job_func: Function to execute
            schedule_config: Dictionary with schedule configuration
                           e.g., {'type': 'daily', 'time': '10:00'}
        """
        try:
            schedule_type = schedule_config.get('type', 'daily')
            time_str = schedule_config.get('time', '09:00')
            
            if schedule_type == 'daily':
                schedule.every().day.at(time_str).do(job_func)
            elif schedule_type == 'weekly':
                day = schedule_config.get('day', 'monday')
                schedule.every().week.on(getattr(schedule.every(), day.lower())).do(job_func)
            elif schedule_type == 'hours':
                interval = schedule_config.get('interval', 1)
                schedule.every(interval).hours.do(job_func)
            
            logger.info(f"Added custom job: {schedule_type} at {time_str}")
            
        except Exception as e:
            logger.error(f"Failed to add custom job: {e}")
            raise
    
    def manual_blog_generation(self, topic: str, **kwargs) -> Dict:
        """Manually trigger blog generation"""
        return self._generate_and_publish_blog(
            topics=[topic],
            max_words=kwargs.get('max_words', 800),
            publish_immediately=kwargs.get('publish_immediately', False),
            platforms=kwargs.get('platforms')
        )
    
    def manual_blog_series(self, main_topic: str, num_posts: int = 5, **kwargs) -> Dict:
        """Manually trigger blog series generation"""
        return self._generate_blog_series(
            main_topic=main_topic,
            num_posts=num_posts,
            publish_immediately=kwargs.get('publish_immediately', False),
            platforms=kwargs.get('platforms')
        )


# Example usage and testing
if __name__ == "__main__":
    # Initialize scheduler
    scheduler = BlogScheduler()
    
    # Configure topics and schedule
    topics = ["AI in healthcare", "Sustainable technology", "Remote work", "Cybersecurity"]
    
    # Schedule daily blog generation
    success = scheduler.schedule_daily_blog_generation(
        topics=topics,
        max_words=800,
        publish_immediately=False,  # Set to True to publish immediately
        time_str="09:00"
    )
    
    if success:
        print("Successfully scheduled daily blog generation")
        
        # Start scheduler
        scheduler.start()
        
        # Test manual generation
        result = scheduler.manual_blog_generation(
            topic="Test AI Topic",
            publish_immediately=False
        )
        
        print("Manual generation result:", result)
        
        # Get statistics
        stats = scheduler.get_statistics()
        print("Scheduler statistics:", stats)
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping scheduler...")
            scheduler.stop()
    else:
        print("Failed to schedule blog generation")
