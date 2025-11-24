"""
Blog Analytics Module
Tracks and analyzes blog performance, engagement, and SEO metrics
"""
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from loguru import logger
import sqlite3
from urllib.parse import urlparse

from config.settings import settings


class BlogAnalytics:
    """
    Tracks and analyzes blog performance across different platforms
    """
    
    def __init__(self):
        """Initialize the blog analytics tracker"""
        self.analytics_db = "blog_analytics.db"
        self._init_database()
        
        # Platform-specific analytics clients
        self.google_analytics = None
        self.medium_analytics = None
        
        # Initialize analytics tracking
        self._setup_analytics_tracking()
    
    def _init_database(self):
        """Initialize analytics database"""
        try:
            conn = sqlite3.connect(self.analytics_db)
            cursor = conn.cursor()
            
            # Create analytics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS blog_analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id TEXT,
                    title TEXT,
                    platform TEXT,
                    url TEXT,
                    views INTEGER DEFAULT 0,
                    likes INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    reading_time INTEGER,
                    engagement_rate REAL,
                    seo_score INTEGER,
                    keywords_ranking TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create SEO metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS seo_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT,
                    meta_title TEXT,
                    meta_description TEXT,
                    h1_tags TEXT,
                    image_alt_tags TEXT,
                    word_count INTEGER,
                    keyword_density TEXT,
                    readability_score REAL,
                    performance_score REAL,
                    accessibility_score REAL,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create engagement tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS engagement_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id TEXT,
                    platform TEXT,
                    date DATE,
                    views INTEGER DEFAULT 0,
                    unique_visitors INTEGER DEFAULT 0,
                    time_spent REAL,
                    bounce_rate REAL,
                    social_shares INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    email_signups INTEGER DEFAULT 0,
                    click_through_rate REAL
                )
            ''')
            
            conn.commit()
            conn.close()
            
            logger.info("Analytics database initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize analytics database: {e}")
    
    def _setup_analytics_tracking(self):
        """Setup analytics tracking for different platforms"""
        # Google Analytics 4 setup (if configured)
        if hasattr(settings, 'GA4_MEASUREMENT_ID') and settings.GA4_MEASUREMENT_ID:
            self.google_analytics = GoogleAnalytics4(settings.GA4_MEASUREMENT_ID)
        
        # Medium analytics setup
        if hasattr(settings, 'MEDIUM_TOKEN') and settings.MEDIUM_TOKEN:
            self.medium_analytics = MediumAnalytics(settings.MEDIUM_TOKEN)
    
    def track_blog_post(self, post_id: str, title: str, platform: str, 
                       url: str, metadata: Dict = None) -> bool:
        """
        Track a newly published blog post
        
        Args:
            post_id: Unique identifier for the post
            title: Blog post title
            platform: Platform where published
            url: URL of the blog post
            metadata: Additional metadata
            
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.analytics_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO blog_analytics 
                (post_id, title, platform, url, reading_time, seo_score)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                post_id,
                title,
                platform,
                url,
                metadata.get('reading_time') if metadata else None,
                metadata.get('seo_score') if metadata else None
            ))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Tracked blog post: {title} on {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to track blog post: {e}")
            return False
    
    def update_engagement_metrics(self, post_id: str, platform: str, 
                                 metrics: Dict) -> bool:
        """
        Update engagement metrics for a blog post
        
        Args:
            post_id: Unique identifier for the post
            platform: Platform where published
            metrics: Dictionary with engagement metrics
            
        Returns:
            Success status
        """
        try:
            conn = sqlite3.connect(self.analytics_db)
            cursor = conn.cursor()
            
            # Update main analytics table
            cursor.execute('''
                UPDATE blog_analytics 
                SET views = ?, likes = ?, shares = ?, comments = ?,
                    engagement_rate = ?, updated_at = CURRENT_TIMESTAMP
                WHERE post_id = ? AND platform = ?
            ''', (
                metrics.get('views', 0),
                metrics.get('likes', 0),
                metrics.get('shares', 0),
                metrics.get('comments', 0),
                metrics.get('engagement_rate', 0.0),
                post_id,
                platform
            ))
            
            # Update daily engagement tracking
            today = datetime.now().date().isoformat()
            cursor.execute('''
                INSERT OR REPLACE INTO engagement_tracking
                (post_id, platform, date, views, unique_visitors, 
                 time_spent, bounce_rate, social_shares, comments, 
                 click_through_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                post_id, platform, today,
                metrics.get('views', 0),
                metrics.get('unique_visitors', 0),
                metrics.get('time_spent', 0.0),
                metrics.get('bounce_rate', 0.0),
                metrics.get('social_shares', 0),
                metrics.get('comments', 0),
                metrics.get('click_through_rate', 0.0)
            ))
            
            conn.commit()
            conn.close()
            
            logger.debug(f"Updated engagement metrics for {post_id} on {platform}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update engagement metrics: {e}")
            return False
    
    def analyze_seo_performance(self, url: str) -> Dict:
        """
        Analyze SEO performance of a blog post URL
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary with SEO analysis results
        """
        try:
            # Fetch the webpage content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            html_content = response.text
            
            # Perform SEO analysis
            seo_analysis = self._perform_seo_analysis(html_content, url)
            
            # Save results to database
            self._save_seo_analysis(url, seo_analysis)
            
            return seo_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze SEO performance for {url}: {e}")
            return {'error': str(e)}
    
    def _perform_seo_analysis(self, html_content: str, url: str) -> Dict:
        """Perform detailed SEO analysis on HTML content"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        analysis = {
            'url': url,
            'meta_title': '',
            'meta_description': '',
            'h1_tags': [],
            'image_alt_tags': [],
            'word_count': 0,
            'keyword_density': {},
            'readability_score': 0.0,
            'performance_score': 0,
            'accessibility_score': 0,
            'seo_issues': [],
            'recommendations': []
        }
        
        try:
            # Extract meta title and description
            title_tag = soup.find('title')
            if title_tag:
                analysis['meta_title'] = title_tag.get_text().strip()
                analysis['seo_issues'].append('Missing meta title') if not analysis['meta_title'] else None
            
            description_tag = soup.find('meta', attrs={'name': 'description'})
            if description_tag:
                analysis['meta_description'] = description_tag.get('content', '')
            
            # Extract H1 tags
            h1_tags = soup.find_all('h1')
            analysis['h1_tags'] = [h1.get_text().strip() for h1 in h1_tags]
            
            # Check for multiple H1s
            if len(analysis['h1_tags']) == 0:
                analysis['seo_issues'].append('Missing H1 tag')
                analysis['recommendations'].append('Add an H1 tag to your page')
            elif len(analysis['h1_tags']) > 1:
                analysis['seo_issues'].append('Multiple H1 tags found')
                analysis['recommendations'].append('Use only one H1 tag per page')
            
            # Extract image alt tags
            images = soup.find_all('img')
            images_without_alt = []
            for img in images:
                alt_text = img.get('alt', '')
                if not alt_text.strip():
                    images_without_alt.append(img.get('src', 'unknown'))
                else:
                    analysis['image_alt_tags'].append(alt_text)
            
            if images_without_alt:
                analysis['seo_issues'].append(f'{len(images_without_alt)} images missing alt text')
                analysis['recommendations'].append('Add alt text to all images for better accessibility and SEO')
            
            # Count words
            text_content = soup.get_text()
            words = text_content.split()
            analysis['word_count'] = len(words)
            
            # Check word count recommendations
            if analysis['word_count'] < 300:
                analysis['seo_issues'].append('Content too short (less than 300 words)')
                analysis['recommendations'].append('Consider adding more content (300+ words recommended)')
            elif analysis['word_count'] > 2500:
                analysis['recommendations'].append('Consider breaking long content into multiple pages')
            
            # Calculate readability score (simple estimation)
            sentences = text_content.count('.') + text_content.count('!') + text_content.count('?')
            avg_words_per_sentence = analysis['word_count'] / max(sentences, 1)
            analysis['readability_score'] = max(0, 100 - (avg_words_per_sentence - 15) * 2)
            
            # Calculate performance score based on content length and structure
            performance_score = 50  # Base score
            if analysis['h1_tags']:
                performance_score += 10
            if analysis['meta_description']:
                performance_score += 10
            if analysis['word_count'] >= 300:
                performance_score += 15
            if analysis['readability_score'] >= 70:
                performance_score += 15
            
            analysis['performance_score'] = min(100, performance_score)
            
            # Accessibility score
            accessibility_score = 50  # Base score
            if not images_without_alt:
                accessibility_score += 30
            if analysis['h1_tags']:
                accessibility_score += 20
            
            analysis['accessibility_score'] = min(100, accessibility_score)
            
            # SEO score calculation
            seo_score = 50  # Base score
            if analysis['meta_title'] and len(analysis['meta_title']) <= 60:
                seo_score += 20
            if analysis['meta_description'] and len(analysis['meta_description']) <= 160:
                seo_score += 20
            if analysis['h1_tags']:
                seo_score += 10
            
            analysis['seo_score'] = min(100, seo_score)
            
            # Generate specific recommendations
            if not analysis['meta_title']:
                analysis['recommendations'].append('Add a meta title (50-60 characters)')
            if not analysis['meta_description']:
                analysis['recommendations'].append('Add a meta description (150-160 characters)')
            if len(analysis['h1_tags']) > 1:
                analysis['recommendations'].append('Use only one H1 tag per page')
            
        except Exception as e:
            logger.error(f"Error performing SEO analysis: {e}")
            analysis['error'] = str(e)
        
        return analysis
    
    def _save_seo_analysis(self, url: str, analysis: Dict):
        """Save SEO analysis results to database"""
        try:
            conn = sqlite3.connect(self.analytics_db)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO seo_metrics
                (url, meta_title, meta_description, h1_tags, image_alt_tags,
                 word_count, keyword_density, readability_score, 
                 performance_score, accessibility_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                url,
                analysis.get('meta_title', ''),
                analysis.get('meta_description', ''),
                json.dumps(analysis.get('h1_tags', [])),
                json.dumps(analysis.get('image_alt_tags', [])),
                analysis.get('word_count', 0),
                json.dumps(analysis.get('keyword_density', {})),
                analysis.get('readability_score', 0.0),
                analysis.get('performance_score', 0),
                analysis.get('accessibility_score', 0)
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to save SEO analysis: {e}")
    
    def get_blog_performance_summary(self, days: int = 30) -> Dict:
        """
        Get comprehensive performance summary for blog posts
        
        Args:
            days: Number of days to include in summary
            
        Returns:
            Dictionary with performance summary
        """
        try:
            conn = sqlite3.connect(self.analytics_db)
            cursor = conn.cursor()
            
            # Calculate date range
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
            # Get overall statistics
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_posts,
                    SUM(views) as total_views,
                    SUM(likes) as total_likes,
                    SUM(shares) as total_shares,
                    SUM(comments) as total_comments,
                    AVG(engagement_rate) as avg_engagement_rate,
                    AVG(seo_score) as avg_seo_score
                FROM blog_analytics
                WHERE created_at >= ?
            ''', (start_date.isoformat(),))
            
            overall_stats = cursor.fetchone()
            
            # Get platform breakdown
            cursor.execute('''
                SELECT platform, COUNT(*) as posts, SUM(views) as views, AVG(seo_score) as avg_seo
                FROM blog_analytics
                WHERE created_at >= ?
                GROUP BY platform
            ''', (start_date.isoformat(),))
            
            platform_stats = cursor.fetchall()
            
            # Get top performing posts
            cursor.execute('''
                SELECT title, platform, views, likes, shares, engagement_rate, seo_score
                FROM blog_analytics
                WHERE created_at >= ?
                ORDER BY views DESC
                LIMIT 10
            ''', (start_date.isoformat(),))
            
            top_posts = cursor.fetchall()
            
            # Get SEO performance summary
            cursor.execute('''
                SELECT 
                    AVG(seo_score) as avg_seo_score,
                    AVG(readability_score) as avg_readability,
                    AVG(performance_score) as avg_performance,
                    AVG(accessibility_score) as avg_accessibility
                FROM seo_metrics
                WHERE checked_at >= ?
            ''', (start_date.isoformat(),))
            
            seo_summary = cursor.fetchone()
            
            conn.close()
            
            return {
                'period': {
                    'start_date': start_date.isoformat(),
                    'end_date': end_date.isoformat(),
                    'days': days
                },
                'overall_performance': {
                    'total_posts': overall_stats[0] or 0,
                    'total_views': overall_stats[1] or 0,
                    'total_likes': overall_stats[2] or 0,
                    'total_shares': overall_stats[3] or 0,
                    'total_comments': overall_stats[4] or 0,
                    'average_engagement_rate': round(overall_stats[5] or 0, 2),
                    'average_seo_score': round(overall_stats[6] or 0, 1)
                },
                'platform_breakdown': [
                    {
                        'platform': row[0],
                        'posts': row[1],
                        'total_views': row[2] or 0,
                        'average_seo_score': round(row[3] or 0, 1)
                    }
                    for row in platform_stats
                ],
                'top_performing_posts': [
                    {
                        'title': row[0],
                        'platform': row[1],
                        'views': row[2] or 0,
                        'likes': row[3] or 0,
                        'shares': row[4] or 0,
                        'engagement_rate': round(row[5] or 0, 2),
                        'seo_score': round(row[6] or 0, 1)
                    }
                    for row in top_posts
                ],
                'seo_performance': {
                    'average_seo_score': round(seo_summary[0] or 0, 1),
                    'average_readability_score': round(seo_summary[1] or 0, 1),
                    'average_performance_score': round(seo_summary[2] or 0, 1),
                    'average_accessibility_score': round(seo_summary[3] or 0, 1)
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance summary: {e}")
            return {'error': str(e)}
    
    def get_trending_topics(self, days: int = 30) -> List[Dict]:
        """
        Identify trending topics based on engagement
        
        Args:
            days: Number of days to analyze
            
        Returns:
            List of trending topics with engagement data
        """
        try:
            conn = sqlite3.connect(self.analytics_db)
            cursor = conn.cursor()
            
            # This is a simplified implementation
            # In a real system, you might extract topics from post titles
            # and correlate with engagement metrics
            
            cursor.execute('''
                SELECT title, SUM(views) as total_views, COUNT(*) as post_count
                FROM blog_analytics
                WHERE created_at >= ?
                GROUP BY title
                ORDER BY total_views DESC
                LIMIT 20
            ''', (days,))
            
            trending_data = cursor.fetchall()
            
            # Extract topic keywords (simple implementation)
            trending_topics = []
            for title, views, count in trending_data:
                # Simple keyword extraction
                words = title.lower().split()
                topics = [word for word in words if len(word) > 3]
                
                for topic in topics:
                    trending_topics.append({
                        'topic': topic,
                        'total_views': views,
                        'post_count': count
                    })
            
            # Group by topic
            topic_aggregation = {}
            for item in trending_topics:
                topic = item['topic']
                if topic not in topic_aggregation:
                    topic_aggregation[topic] = {
                        'topic': topic,
                        'total_views': 0,
                        'post_count': 0
                    }
                
                topic_aggregation[topic]['total_views'] += item['total_views']
                topic_aggregation[topic]['post_count'] += item['post_count']
            
            # Sort by total views
            result = sorted(topic_aggregation.values(), 
                          key=lambda x: x['total_views'], 
                          reverse=True)[:10]
            
            conn.close()
            return result
            
        except Exception as e:
            logger.error(f"Failed to get trending topics: {e}")
            return []
    
    def generate_performance_report(self, days: int = 30) -> str:
        """
        Generate a comprehensive performance report
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Formatted performance report as string
        """
        try:
            summary = self.get_blog_performance_summary(days)
            trending_topics = self.get_trending_topics(days)
            
            if 'error' in summary:
                return f"Error generating report: {summary['error']}"
            
            report = f"""
# Blog Performance Report
**Period:** {summary['period']['start_date']} to {summary['period']['end_date']}

## Overall Performance
- **Total Posts:** {summary['overall_performance']['total_posts']}
- **Total Views:** {summary['overall_performance']['total_views']:,}
- **Total Engagement:**
  - Likes: {summary['overall_performance']['total_likes']:,}
  - Shares: {summary['overall_performance']['total_shares']:,}
  - Comments: {summary['overall_performance']['total_comments']:,}
- **Average Engagement Rate:** {summary['overall_performance']['average_engagement_rate']}%
- **Average SEO Score:** {summary['overall_performance']['average_seo_score']}/100

## Platform Performance
"""
            
            for platform in summary['platform_breakdown']:
                report += f"""
### {platform['platform']}
- Posts: {platform['posts']}
- Views: {platform['total_views']:,}
- Average SEO Score: {platform['average_seo_score']}/100
"""
            
            report += "\n## Top Performing Posts\n"
            for i, post in enumerate(summary['top_performing_posts'][:5], 1):
                report += f"""
### {i}. {post['title']}
- Platform: {post['platform']}
- Views: {post['views']:,}
- Likes: {post['likes']:,}
- Shares: {post['shares']:,}
- Engagement Rate: {post['engagement_rate']}%
- SEO Score: {post['seo_score']}/100
"""
            
            report += "\n## SEO Performance Summary\n"
            seo = summary['seo_performance']
            report += f"""
- Average SEO Score: {seo['average_seo_score']}/100
- Average Readability Score: {seo['average_readability_score']}/100
- Average Performance Score: {seo['average_performance_score']}/100
- Average Accessibility Score: {seo['average_accessibility_score']}/100
"""
            
            report += "\n## Trending Topics\n"
            for topic in trending_topics:
                report += f"- **{topic['topic']}**: {topic['total_views']:,} views across {topic['post_count']} posts\n"
            
            report += f"\n---\n*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            return f"Error generating report: {str(e)}"


# Platform-specific analytics implementations
class GoogleAnalytics4:
    """Google Analytics 4 integration"""
    
    def __init__(self, measurement_id: str):
        self.measurement_id = measurement_id
        # This would integrate with GA4 API for more detailed analytics
    
    def get_page_views(self, page_path: str, start_date: str, end_date: str) -> Dict:
        """Get page views for a specific page"""
        # This would use GA4 API to get real analytics data
        return {'views': 0, 'sessions': 0, 'users': 0}


class MediumAnalytics:
    """Medium platform analytics integration"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.medium.com/v1"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_post_analytics(self, post_id: str) -> Dict:
        """Get analytics for a Medium post"""
        try:
            # Medium API doesn't provide detailed analytics
            # This would be a placeholder for future implementation
            return {'views': 0, 'claps': 0, 'responses': 0}
        except Exception as e:
            logger.error(f"Failed to get Medium analytics: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    # Initialize analytics tracker
    analytics = BlogAnalytics()
    
    # Track a blog post
    success = analytics.track_blog_post(
        post_id="test_post_001",
        title="AI in Healthcare: 2025 Trends",
        platform="wordpress",
        url="https://example.com/ai-healthcare-2025"
    )
    
    print(f"Tracked blog post: {success}")
    
    # Update engagement metrics
    metrics_update = analytics.update_engagement_metrics(
        post_id="test_post_001",
        platform="wordpress",
        metrics={
            'views': 150,
            'likes': 12,
            'shares': 5,
            'comments': 3,
            'engagement_rate': 13.3
        }
    )
    
    print(f"Updated metrics: {metrics_update}")
    
    # Generate performance report
    report = analytics.generate_performance_report(days=30)
    print("\nPerformance Report:")
    print(report)
