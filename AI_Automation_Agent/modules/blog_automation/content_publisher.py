"""
Content Publisher Module
Handles publishing blog posts to various platforms (WordPress, Medium, etc.)
"""
import requests
import json
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
import xmlrpc.client

from config.settings import settings


class WordPressPublisher:
    """
    Publishes blog posts to WordPress using XML-RPC API
    """
    
    def __init__(self, url: str, username: str, password: str):
        """
        Initialize WordPress publisher
        
        Args:
            url: WordPress site URL
            username: WordPress username
            password: Application password (not regular password)
        """
        self.url = url.rstrip('/')
        self.username = username
        self.password = password
        
        # WordPress XML-RPC endpoint
        self.rpc_url = f"{self.url}/xmlrpc.php"
        
        # Initialize XML-RPC client
        try:
            self.rpc = xmlrpc.client.ServerProxy(self.rpc_url)
            self._test_connection()
        except Exception as e:
            logger.error(f"Failed to initialize WordPress connection: {e}")
            raise
    
    def _test_connection(self):
        """Test WordPress connection"""
        try:
            users = self.rpc.wp.getUsers({}, self.username, self.password)
            logger.info(f"WordPress connection successful. Found {len(users)} users")
        except Exception as e:
            raise Exception(f"WordPress connection failed: {e}")
    
    def publish_post(self, title: str, content: str, 
                    tags: List[str] = None, category: str = None,
                    status: str = "publish", featured_image: str = None) -> Dict:
        """
        Publish a blog post to WordPress
        
        Args:
            title: Blog post title
            content: Blog post content (HTML or markdown)
            tags: List of tags
            category: Post category
            status: Post status (publish, draft, pending, future)
            featured_image: URL of featured image
            
        Returns:
            Dictionary with publishing results
        """
        try:
            # Get blog info
            blog_info = self._get_blog_info()
            
            # Prepare post data
            post_data = self._prepare_post_data(
                title=title,
                content=content,
                tags=tags,
                category=category,
                status=status,
                featured_image=featured_image
            )
            
            # Publish the post
            if status == "publish":
                post_id = self.rpc.wp.newPost(blog_info['blog_id'], 
                                            self.username, 
                                            self.password, 
                                            post_data)
            else:
                # For drafts and other statuses
                post_id = self.rpc.wp.newPost(blog_info['blog_id'], 
                                            self.username, 
                                            self.password, 
                                            post_data)
            
            # Get post URL
            post_url = f"{self.url}/?p={post_id}"
            
            result = {
                'success': True,
                'post_id': post_id,
                'url': post_url,
                'status': status,
                'published_at': datetime.now().isoformat()
            }
            
            logger.info(f"Successfully published WordPress post ID {post_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to publish to WordPress: {e}")
            return {
                'success': False,
                'error': str(e),
                'post_id': None
            }
    
    def _get_blog_info(self) -> Dict:
        """Get WordPress blog information"""
        try:
            users = self.rpc.wp.getUsers({}, self.username, self.password)
            # Assume first blog for single site
            return {'blog_id': 1}
        except Exception as e:
            raise Exception(f"Failed to get blog info: {e}")
    
    def _prepare_post_data(self, title: str, content: str, 
                          tags: List[str], category: str, 
                          status: str, featured_image: str) -> Dict:
        """Prepare post data for WordPress"""
        
        post_data = {
            'post_title': title,
            'post_content': content,
            'post_status': status,
            'post_type': 'post',
            'post_author': 1  # Default author
        }
        
        # Add tags
        if tags:
            post_data['terms_names'] = {
                'post_tag': tags
            }
        
        # Add category
        if category:
            post_data['terms_names']['category'] = [category]
        
        # Add custom fields for AI-generated content
        post_data['custom_fields'] = [
            {
                'key': 'ai_generated',
                'value': 'true'
            },
            {
                'key': 'generated_at',
                'value': datetime.now().isoformat()
            }
        ]
        
        return post_data
    
    def get_categories(self) -> List[Dict]:
        """Get available WordPress categories"""
        try:
            categories = self.rpc.wp.getTerms(1, self.username, self.password, 'category')
            return [{'id': cat['term_id'], 'name': cat['name'], 'slug': cat['slug']} 
                   for cat in categories]
        except Exception as e:
            logger.error(f"Failed to get categories: {e}")
            return []
    
    def get_tags(self) -> List[Dict]:
        """Get available WordPress tags"""
        try:
            tags = self.rpc.wp.getTerms(1, self.username, self.password, 'post_tag')
            return [{'id': tag['term_id'], 'name': tag['name'], 'slug': tag['slug']} 
                   for tag in tags]
        except Exception as e:
            logger.error(f"Failed to get tags: {e}")
            return []
    
    def update_post(self, post_id: int, **kwargs) -> Dict:
        """Update an existing WordPress post"""
        try:
            post_data = {}
            
            if 'title' in kwargs:
                post_data['post_title'] = kwargs['title']
            if 'content' in kwargs:
                post_data['post_content'] = kwargs['content']
            if 'status' in kwargs:
                post_data['post_status'] = kwargs['status']
            
            result = self.rpc.wp.editPost(post_id, self.username, self.password, post_data)
            
            logger.info(f"Successfully updated WordPress post {post_id}")
            return {'success': True, 'result': result}
            
        except Exception as e:
            logger.error(f"Failed to update WordPress post: {e}")
            return {'success': False, 'error': str(e)}


class MediumPublisher:
    """
    Publishes blog posts to Medium using their API
    """
    
    def __init__(self, access_token: str):
        """
        Initialize Medium publisher
        
        Args:
            access_token: Medium access token
        """
        self.access_token = access_token
        self.base_url = "https://api.medium.com/v1"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Get user info on initialization
        self.user_id = self._get_user_id()
    
    def _get_user_id(self) -> str:
        """Get Medium user ID"""
        try:
            response = requests.get(f"{self.base_url}/me", headers=self.headers)
            response.raise_for_status()
            
            user_data = response.json()
            user_id = user_data['data']['id']
            logger.info(f"Connected to Medium user: {user_data['data']['username']}")
            return user_id
            
        except Exception as e:
            raise Exception(f"Failed to get Medium user info: {e}")
    
    def publish_post(self, title: str, content: str, 
                    tags: List[str] = None, 
                    publish_status: str = "draft",
                    canonical_url: str = None,
                    content_format: str = "markdown") -> Dict:
        """
        Publish a blog post to Medium
        
        Args:
            title: Blog post title
            content: Blog post content
            tags: List of tags (max 5 for Medium)
            publish_status: publish, draft, or unlisted
            canonical_url: Original URL if cross-posting
            content_format: markdown or html
            
        Returns:
            Dictionary with publishing results
        """
        try:
            # Prepare post data
            post_data = {
                'title': title,
                'contentFormat': content_format,
                'content': content,
                'publishStatus': publish_status,
                'tags': tags[:5] if tags else []  # Medium limits to 5 tags
            }
            
            # Add canonical URL if provided
            if canonical_url:
                post_data['canonicalUrl'] = canonical_url
            
            # Add custom metadata for AI-generated content
            post_data['notifyFollowers'] = False
            post_data['license'] = "all-rights-reserved"
            
            # Add custom fields via content (Medium doesn't support custom fields like WordPress)
            # We can add this info in the content footer
            content_with_metadata = f"""{content}

---
*This article was AI-generated and published automatically on {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}*
*Topic: Generated by AI Automation Agent*
"""
            
            post_data['content'] = content_with_metadata
            
            # Publish the post
            response = requests.post(
                f"{self.base_url}/users/{self.user_id}/posts",
                headers=self.headers,
                json=post_data
            )
            
            response.raise_for_status()
            result_data = response.json()
            
            post_url = result_data['data']['url']
            post_id = result_data['data']['id']
            
            result = {
                'success': True,
                'post_id': post_id,
                'url': post_url,
                'status': publish_status,
                'published_at': result_data['data']['publishedAt']
            }
            
            logger.info(f"Successfully published Medium post {post_id}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Medium API error: {e}")
            return {
                'success': False,
                'error': f"API Error: {str(e)}",
                'post_id': None
            }
        except Exception as e:
            logger.error(f"Failed to publish to Medium: {e}")
            return {
                'success': False,
                'error': str(e),
                'post_id': None
            }
    
    def get_published_posts(self, limit: int = 10) -> List[Dict]:
        """Get published posts from Medium"""
        try:
            response = requests.get(
                f"{self.base_url}/users/{self.user_id}/posts",
                headers=self.headers,
                params={'limit': limit}
            )
            
            response.raise_for_status()
            posts_data = response.json()
            
            posts = []
            for post in posts_data['data']:
                posts.append({
                    'id': post['id'],
                    'title': post['title'],
                    'url': post['url'],
                    'publish_status': post['publishStatus'],
                    'published_at': post['publishedAt'],
                    'tags': post.get('tags', [])
                })
            
            return posts
            
        except Exception as e:
            logger.error(f"Failed to get Medium posts: {e}")
            return []
    
    def update_post(self, post_id: str, **kwargs) -> Dict:
        """Update an existing Medium post (Limited functionality)"""
        try:
            # Medium has limited update capabilities
            # Most fields cannot be updated after publication
            
            if 'title' in kwargs:
                # This would require re-publishing as Medium doesn't support title updates
                logger.warning("Medium doesn't support post title updates. Consider re-publishing.")
                return {'success': False, 'error': 'Medium does not support post updates'}
            
            return {'success': False, 'error': 'Medium posts cannot be updated via API'}
            
        except Exception as e:
            logger.error(f"Failed to update Medium post: {e}")
            return {'success': False, 'error': str(e)}


class NextJSAPIPublisher:
    """
    Optimized publisher for Next.js applications with REST API endpoints
    Designed for direct integration with Next.js blog systems
    Uses session-based authentication for enhanced security
    """
    
    def __init__(self, api_url: str, admin_session: str, auth_header: str = "x-admin-session"):
        """
        Initialize Next.js API publisher with session-based authentication
        
        Args:
            api_url: Next.js API endpoint (e.g., https://your-site.com/api/blogs)
            admin_session: JSON string containing admin session data
                          Format: {"id":"admin-user-id","email":"admin@site.com","role":"admin"}
            auth_header: Authentication header name (default: "x-admin-session")
        """
        self.api_url = api_url.rstrip('/')
        self.admin_session = admin_session
        self.auth_header = auth_header
        
        # Prepare headers for session-based authentication
        self.headers = {
            auth_header: admin_session,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'AI-Automation-Agent/1.0'
        }
        
        # Test connection on initialization
        self._test_connection()
    
    def _test_connection(self):
        """Test Next.js API connection"""
        try:
            # Test with a simple health check if available
            response = requests.get(
                f"{self.api_url}/health", 
                headers=self.headers, 
                timeout=10
            )
            logger.info(f"Next.js API connection successful (Status: {response.status_code})")
        except requests.exceptions.RequestException:
            # Health endpoint might not exist, that's okay
            logger.info("Next.js API connection initiated (health check optional)")
    
    def publish_post(self, title: str, content: str, 
                    tags: List[str] = None, category: str = None,
                    status: str = "draft", featured_image: str = None,
                    seo_title: str = None, seo_description: str = None,
                    excerpt: str = None, slug: str = None,
                    **kwargs) -> Dict:
        """
        Publish blog post to Next.js API with session-based authentication
        
        Args:
            title: Blog post title
            content: Blog post content (HTML or markdown)
            tags: List of tags
            category: Post category
            status: Post status (draft, published, private)
            featured_image: URL of featured image
            seo_title: SEO-optimized title
            seo_description: SEO meta description
            excerpt: Brief description (150-200 chars)
            slug: URL-friendly slug
            **kwargs: Additional fields for the API
            
        Returns:
            Dictionary with publishing results
        """
        start_time = datetime.now()
        
        try:
            # Prepare post data optimized for Next.js Admin API
            post_data = {
                'title': title,
                'content': content,
                'status': status,
                'ai_generated': True,
                'generated_at': start_time.isoformat(),
                'metadata': {
                    'source': 'ai_automation_agent',
                    'version': '2.0',
                    'auth_type': 'session'
                }
            }
            
            # Add required/optional fields for Next.js Admin API
            if excerpt:
                post_data['excerpt'] = excerpt
            elif len(content) > 150:
                # Auto-generate excerpt from content if not provided
                post_data['excerpt'] = content[:150].strip() + "..."
            else:
                post_data['excerpt'] = content
                
            if slug:
                post_data['slug'] = slug
            else:
                # Auto-generate slug from title
                import re
                post_data['slug'] = re.sub(r'[^a-zA-Z0-9\s]', '', title).lower().replace(' ', '-')
            
            if featured_image:
                post_data['featured_image'] = featured_image
                
            if tags:
                post_data['tags'] = tags
            
            if category:
                post_data['category'] = category
                
            if seo_title:
                post_data['seo_title'] = seo_title
                
            if seo_description:
                post_data['seo_description'] = seo_description
            
            # Add any additional fields
            post_data.update(kwargs)
            
            # Log the publishing attempt
            logger.info(f"Publishing to Next.js API: '{title}' (status: {status})")
            
            # Make API request with timeout and retry logic
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            # Handle different response status codes
            if response.status_code == 201:
                result_data = response.json()
                
                result = {
                    'success': True,
                    'post_id': result_data.get('id') or result_data.get('_id'),
                    'url': result_data.get('url') or result_data.get('slug'),
                    'status': status,
                    'published_at': start_time.isoformat(),
                    'api_response_time': (datetime.now() - start_time).total_seconds()
                }
                
                logger.info(f"✅ Successfully published to Next.js API (ID: {result['post_id']}) in {result['api_response_time']:.2f}s")
                return result
                
            elif response.status_code == 400:
                error_detail = response.json().get('message', 'Bad Request')
                logger.error(f"❌ Bad Request: {error_detail}")
                return {
                    'success': False,
                    'error': f"Validation Error: {error_detail}",
                    'post_id': None,
                    'api_response_time': (datetime.now() - start_time).total_seconds()
                }
                
            elif response.status_code == 401:
                logger.error("❌ Unauthorized: Invalid session or authentication")
                return {
                    'success': False,
                    'error': "Session authentication failed - check admin session data",
                    'post_id': None,
                    'auth_type': 'session',
                    'api_response_time': (datetime.now() - start_time).total_seconds()
                }
                
            elif response.status_code == 429:
                logger.warning("⚠️ Rate limit exceeded - retrying in 5 seconds")
                # Could implement retry logic here
                return {
                    'success': False,
                    'error': "Rate limit exceeded - please try again later",
                    'post_id': None
                }
                
            else:
                response.raise_for_status()
                
        except requests.exceptions.Timeout:
            logger.error(f"⏰ Timeout publishing to Next.js API after 30 seconds")
            return {
                'success': False,
                'error': "Request timeout - API may be unavailable",
                'post_id': None
            }
        except requests.exceptions.ConnectionError:
            logger.error(f"🔌 Connection error to Next.js API: {self.api_url}")
            return {
                'success': False,
                'error': "Failed to connect to API - check URL and network",
                'post_id': None
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"🌐 Next.js API request error: {e}")
            return {
                'success': False,
                'error': f"API Request Error: {str(e)}",
                'post_id': None
            }
        except json.JSONDecodeError:
            logger.error(f"📄 Invalid JSON response from Next.js API")
            return {
                'success': False,
                'error': "Invalid API response format",
                'post_id': None
            }
        except Exception as e:
            logger.error(f"💥 Unexpected error publishing to Next.js API: {e}")
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'post_id': None
            }
    
    def create_draft(self, title: str, content: str, **kwargs) -> Dict:
        """
        Create a draft post (convenience method)
        """
        return self.publish_post(title, content, status="draft", **kwargs)
    
    def update_post(self, post_id: str, **kwargs) -> Dict:
        """
        Update an existing post
        """
        try:
            update_url = f"{self.api_url}/{post_id}"
            
            response = requests.put(
                update_url,
                headers=self.headers,
                json=kwargs,
                timeout=30
            )
            
            response.raise_for_status()
            result_data = response.json()
            
            logger.info(f"✅ Successfully updated Next.js post {post_id}")
            return {
                'success': True,
                'post_id': post_id,
                'data': result_data
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to update Next.js post {post_id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'post_id': post_id
            }
    
    def get_post_status(self, post_id: str) -> Dict:
        """
        Get post status from API
        """
        try:
            status_url = f"{self.api_url}/{post_id}"
            
            response = requests.get(
                status_url,
                headers=self.headers,
                timeout=10
            )
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get post status for {post_id}: {e}")
            return {'error': str(e)}


class CustomWebsitePublisher:
    """
    Generic publisher for custom websites with REST API endpoints
    """
    
    def __init__(self, base_url: str, api_key: str, auth_header: str = "X-API-Key"):
        """
        Initialize custom website publisher
        
        Args:
            base_url: Base URL of the website API
            api_key: API key for authentication
            auth_header: Authentication header name
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            auth_header: api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def publish_post(self, title: str, content: str, 
                    tags: List[str] = None, category: str = None,
                    status: str = "publish", **kwargs) -> Dict:
        """
        Publish to custom website API
        
        Args:
            title: Blog post title
            content: Blog post content
            tags: List of tags
            category: Post category
            status: Post status
            **kwargs: Additional fields for the API
            
        Returns:
            Dictionary with publishing results
        """
        try:
            # Prepare post data
            post_data = {
                'title': title,
                'content': content,
                'status': status,
                'ai_generated': True,
                'generated_at': datetime.now().isoformat()
            }
            
            if tags:
                post_data['tags'] = tags
            
            if category:
                post_data['category'] = category
            
            # Add any additional fields
            post_data.update(kwargs)
            
            # Publish to API
            response = requests.post(
                f"{self.base_url}/api/posts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            response.raise_for_status()
            result_data = response.json()
            
            result = {
                'success': True,
                'post_id': result_data.get('id'),
                'url': result_data.get('url'),
                'status': status,
                'published_at': datetime.now().isoformat()
            }
            
            logger.info(f"✅ Successfully published to custom website")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Custom website API error: {e}")
            return {
                'success': False,
                'error': f"API Error: {str(e)}",
                'post_id': None
            }
        except Exception as e:
            logger.error(f"💥 Failed to publish to custom website: {e}")
            return {
                'success': False,
                'error': str(e),
                'post_id': None
            }


# Publisher manager for handling multiple platforms
class PublisherManager:
    """
    Manages multiple publishers and handles publishing to multiple platforms
    """
    
    def __init__(self):
        self.publishers = {}
    
    def add_wordpress_publisher(self, name: str, url: str, username: str, password: str):
        """Add WordPress publisher"""
        try:
            self.publishers[name] = WordPressPublisher(url, username, password)
            logger.info(f"Added WordPress publisher: {name}")
        except Exception as e:
            logger.error(f"Failed to add WordPress publisher {name}: {e}")
    
    def add_medium_publisher(self, name: str, access_token: str):
        """Add Medium publisher"""
        try:
            self.publishers[name] = MediumPublisher(access_token)
            logger.info(f"Added Medium publisher: {name}")
        except Exception as e:
            logger.error(f"Failed to add Medium publisher {name}: {e}")
    
    def add_nextjs_publisher(self, name: str, api_url: str, admin_session: str, auth_header: str = "x-admin-session"):
        """Add Next.js API publisher with session-based authentication"""
        try:
            self.publishers[name] = NextJSAPIPublisher(api_url, admin_session, auth_header)
            logger.info(f"✅ Added Next.js API publisher: {name} (Session-based auth)")
        except Exception as e:
            logger.error(f"❌ Failed to add Next.js publisher {name}: {e}")
    
    def add_nextjs_publisher_api_key(self, name: str, api_url: str, api_key: str, auth_header: str = "Authorization"):
        """Add Next.js API publisher with legacy API key authentication (DEPRECATED)"""
        logger.warning("⚠️ API key authentication is deprecated. Use session-based authentication.")
        try:
            # Convert API key to session format for compatibility
            session_data = {"auth": "api_key", "key": api_key}
            self.publishers[name] = NextJSAPIPublisher(api_url, json.dumps(session_data), auth_header)
            logger.info(f"✅ Added Next.js API publisher: {name} (API key - deprecated)")
        except Exception as e:
            logger.error(f"❌ Failed to add Next.js publisher {name}: {e}")
    
    def add_custom_publisher(self, name: str, base_url: str, api_key: str):
        """Add custom website publisher"""
        try:
            self.publishers[name] = CustomWebsitePublisher(base_url, api_key)
            logger.info(f"✅ Added custom publisher: {name}")
        except Exception as e:
            logger.error(f"❌ Failed to add custom publisher {name}: {e}")
    
    def publish_to_all(self, title: str, content: str, 
                      tags: List[str] = None, platforms: List[str] = None) -> Dict:
        """
        Publish to all configured platforms or specified platforms
        
        Args:
            title: Blog post title
            content: Blog post content
            tags: List of tags
            platforms: List of platform names to publish to (None for all)
            
        Returns:
            Dictionary with results for each platform
        """
        results = {}
        
        # Determine which platforms to use
        target_platforms = platforms or list(self.publishers.keys())
        
        for platform_name in target_platforms:
            if platform_name in self.publishers:
                try:
                    publisher = self.publishers[platform_name]
                    
                    # Platform-specific publishing
                    if isinstance(publisher, WordPressPublisher):
                        result = publisher.publish_post(title, content, tags)
                    elif isinstance(publisher, MediumPublisher):
                        result = publisher.publish_post(title, content, tags)
                    elif isinstance(publisher, NextJSAPIPublisher):
                        result = publisher.publish_post(title, content, tags)
                    elif isinstance(publisher, CustomWebsitePublisher):
                        result = publisher.publish_post(title, content, tags)
                    else:
                        result = {'success': False, 'error': 'Unknown publisher type'}
                    
                    results[platform_name] = result
                    
                except Exception as e:
                    logger.error(f"Failed to publish to {platform_name}: {e}")
                    results[platform_name] = {
                        'success': False,
                        'error': str(e)
                    }
            else:
                logger.warning(f"Publisher {platform_name} not found")
                results[platform_name] = {
                    'success': False,
                    'error': 'Publisher not configured'
                }
        
        return results


# Example usage
if __name__ == "__main__":
    # Example Next.js API publishing (recommended for Next.js integration)
    print("🚀 Next.js API Publishing Example")
    print("=" * 50)
    
    try:
        # Session-based authentication (RECOMMENDED)
        admin_session = '{"id":"admin-user-id","email":"admin@your-site.com","role":"admin"}'
        nextjs_publisher = NextJSAPIPublisher(
            api_url="https://your-nextjs-site.com/api/blogs",
            admin_session=admin_session,
            auth_header="x-admin-session"
        )
        
        # Create a draft first (recommended for testing)
        draft_result = nextjs_publisher.create_draft(
            title="AI Automation: The Future of Content Creation",
            content="""
# The Future of AI-Powered Content Creation

Artificial Intelligence is revolutionizing how we create and manage content. 
With advanced automation tools, content creators can focus on strategy while 
AI handles the heavy lifting of content generation, optimization, and distribution.

## Key Benefits

- **Efficiency**: Generate high-quality content in minutes
- **Consistency**: Maintain brand voice across all platforms
- **Scalability**: Produce content at scale without sacrificing quality
- **SEO Optimization**: AI understands search patterns and optimizes accordingly

## Getting Started

Start with a single platform and gradually expand your automation capabilities.
The key is to maintain quality while increasing productivity.
            """,
            tags=["ai", "automation", "content-creation", "technology"],
            category="Technology",
            excerpt="Discover how AI automation is transforming content creation and helping businesses scale their content strategy efficiently.",
            slug="ai-automation-future-content-creation",
            featured_image="https://your-site.com/images/ai-automation.jpg",
            seo_title="AI Content Creation: Automation Tools for 2025",
            seo_description="Discover how AI automation is transforming content creation and helping businesses scale their content strategy efficiently."
        )
        
        print("📝 Draft Creation Result:", draft_result)
        
        # If draft successful, publish it
        if draft_result['success']:
            post_id = draft_result['post_id']
            
            # Update status to published
            update_result = nextjs_publisher.update_post(
                post_id=post_id,
                status="published"
            )
            
            print("🚀 Publication Result:", update_result)
        
    except Exception as e:
        print(f"❌ Next.js test failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Next.js Integration Complete!")
    print("\nNext steps:")
    print("1. Configure your Next.js API endpoint")
    print("2. Set up session-based authentication (x-admin-session)")
    print("3. Use draft mode for testing before publishing")
    print("4. Include all required fields (title, content, excerpt, slug)")
    print("5. Monitor logs for successful publishing")
    
    # Legacy platform examples (optional)
    print("\n" + "=" * 30)
    print("📚 Legacy Platform Examples")
    print("=" * 30)
    
    # WordPress (if still needed)
    try:
        wp_publisher = WordPressPublisher(
            url="https://yourblog.com",
            username="your_username", 
            password="your_app_password"
        )
        print("✅ WordPress publisher configured")
    except Exception as e:
        print(f"⚠️ WordPress setup skipped: {e}")
    
    # Medium (if still needed)
    try:
        medium_publisher = MediumPublisher(access_token="your_medium_token")
        print("✅ Medium publisher configured")
    except Exception as e:
        print(f"⚠️ Medium setup skipped: {e}")
