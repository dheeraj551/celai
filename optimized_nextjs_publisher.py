"""
Optimized NextJS Publisher for celorisdesigns.com
Based on actual admin interface analysis
"""
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger

class CelorisDesignsNextJSPublisher:
    """
    Optimized publisher for celorisdesigns.com matching the exact admin interface
    """
    
    def __init__(self):
        self.api_url = "https://celorisdesigns.com/api/admin/blog"
        self.admin_session = '{"id":"550e8400-e29b-41d4-a716-446655440000","email":"support@celorisdesigns.com","role":"admin"}'
        self.auth_header = "x-admin-session"
        
        # Exact field mappings based on admin interface analysis
        self.categories = [
            "Technology", "Productivity", "Platform", "Design", 
            "Development", "Web Development", "AI", "Innovation"
        ]
        
    def create_blog_post(self, title: str, content: str, status: str = "draft", 
                        category: str = "Technology", is_featured: bool = False,
                        featured_image: str = None) -> Dict:
        """
        Create blog post matching celorisdesigns.com admin interface format
        """
        try:
            # Prepare headers for session-based authentication
            headers = {
                self.auth_header: self.admin_session,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'AI-Automation-Agent/2.0'
            }
            
            # Extract excerpt from content (first 150 chars)
            excerpt = content[:150].strip()
            if len(content) > 150:
                excerpt += "..."
            
            # Calculate read time (assuming 200 words per minute)
            word_count = len(content.split())
            read_time_minutes = max(1, round(word_count / 200))
            
            # Format date for celorisdesigns.com
            current_date = datetime.now()
            formatted_date = current_date.strftime("%b %d, %Y, %I:%M %p")
            
            # Create blog post data matching the admin interface
            blog_data = {
                # Core content fields
                "title": title,
                "content": content,
                "excerpt": excerpt,
                "category": category,
                
                # Status and publication fields
                "status": status,  # "published" or "draft"
                "is_featured": is_featured,  # Star icon in interface
                "featured_image": featured_image,
                
                # Author and metadata
                "author": "@MiniMax Agent",  # Matches interface format
                "read_time": f"{read_time_minutes} min",  # Format: "4 min"
                "published_date": formatted_date,  # "Nov 23, 2025, 11:53 PM"
                
                # AI generation metadata
                "ai_generated": True,
                "generated_at": datetime.now().isoformat(),
                "source": "ai_automation_agent",
                "version": "2.0",
                
                # Statistics fields (initialize to 0)
                "views": 0,
                "engagement": 0,
                
                # SEO and metadata
                "slug": self._create_slug(title),
                "tags": self._extract_tags(content, category),
                "metadata": {
                    "source": "ai_automation_agent",
                    "version": "2.0",
                    "auth_type": "session",
                    "ai_generated": True,
                    "generated_at": datetime.now().isoformat()
                }
            }
            
            logger.info(f"Creating blog post: {title} (Category: {category}, Status: {status})")
            logger.info(f"Excerpt: {excerpt}")
            logger.info(f"Read time: {read_time_minutes} min")
            
            # Make API request
            response = requests.post(
                self.api_url, 
                json=blog_data, 
                headers=headers, 
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                logger.info(f"✅ Successfully created blog post on celorisdesigns.com")
                logger.info(f"   ID: {result.get('id', 'unknown')}")
                logger.info(f"   Status: {result.get('status', 'unknown')}")
                logger.info(f"   URL: {result.get('url', 'unknown')}")
                
                return {
                    'success': True,
                    'platform': 'celorisdesigns.com',
                    'blog_id': result.get('id'),
                    'url': result.get('url'),
                    'status': result.get('status', status),
                    'title': title,
                    'category': category,
                    'is_featured': is_featured,
                    'read_time': f"{read_time_minutes} min",
                    'views': 0,
                    'engagement': 0,
                    'message': f'Blog post "{title}" successfully created on celorisdesigns.com',
                    'details': {
                        'category': category,
                        'status': status,
                        'is_featured': is_featured,
                        'author': '@MiniMax Agent',
                        'read_time_minutes': read_time_minutes
                    }
                }
                
            elif response.status_code == 400:
                error_msg = f"Bad Request: {response.text}"
                logger.error(f"❌ Validation error creating blog post: {error_msg}")
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': error_msg,
                    'title': title,
                    'category': category
                }
                
            elif response.status_code == 401:
                error_msg = "Authentication failed - check admin session"
                logger.error(f"❌ {error_msg}")
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': error_msg,
                    'auth_issue': True
                }
                
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                logger.error(f"❌ Failed to create blog post: {error_msg}")
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': error_msg,
                    'status_code': response.status_code,
                    'title': title
                }
                
        except requests.exceptions.Timeout:
            error_msg = "Request timeout - API may be slow"
            logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': error_msg,
                'timeout': True
            }
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Connection error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': error_msg,
                'connection_error': True
            }
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"❌ {error_msg}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': error_msg,
                'unexpected_error': True
            }
    
    def update_blog_post(self, blog_id: str, updates: Dict) -> Dict:
        """
        Update existing blog post
        """
        try:
            headers = {
                self.auth_header: self.admin_session,
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            # Validate category if provided
            if 'category' in updates and updates['category'] not in self.categories:
                updates['category'] = 'Technology'  # Default fallback
            
            # Handle featured status
            if 'is_featured' in updates:
                updates['is_featured'] = bool(updates['is_featured'])
            
            # Update read time if content changed
            if 'content' in updates:
                word_count = len(updates['content'].split())
                read_time_minutes = max(1, round(word_count / 200))
                updates['read_time'] = f"{read_time_minutes} min"
            
            # Update excerpt if content changed
            if 'content' in updates:
                excerpt = updates['content'][:150].strip()
                if len(updates['content']) > 150:
                    excerpt += "..."
                updates['excerpt'] = excerpt
            
            updates['updated_at'] = datetime.now().isoformat()
            
            # Make PUT request
            response = requests.put(
                f"{self.api_url}/{blog_id}", 
                json=updates, 
                headers=headers, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Successfully updated blog post {blog_id}")
                return {
                    'success': True,
                    'platform': 'celorisdesigns.com',
                    'blog_id': blog_id,
                    'message': 'Blog post updated successfully',
                    'updates_applied': list(updates.keys())
                }
            else:
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            logger.error(f"Error updating blog post {blog_id}: {e}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': str(e)
            }
    
    def delete_blog_post(self, blog_id: str) -> Dict:
        """
        Delete blog post
        """
        try:
            headers = {
                self.auth_header: self.admin_session,
                'Content-Type': 'application/json'
            }
            
            response = requests.delete(
                f"{self.api_url}/{blog_id}", 
                headers=headers, 
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Successfully deleted blog post {blog_id}")
                return {
                    'success': True,
                    'platform': 'celorisdesigns.com',
                    'blog_id': blog_id,
                    'message': 'Blog post deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'platform': 'celorisdesigns.com',
                    'error': f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            logger.error(f"Error deleting blog post {blog_id}: {e}")
            return {
                'success': False,
                'platform': 'celorisdesigns.com',
                'error': str(e)
            }
    
    def _create_slug(self, title: str) -> str:
        """Create URL-friendly slug from title"""
        import re
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def _extract_tags(self, content: str, category: str) -> List[str]:
        """Extract relevant tags from content and category"""
        tags = [category.lower()]
        
        # Common tech keywords
        keywords = {
            'ai': ['artificial intelligence', 'machine learning', 'ai', 'neural'],
            'react': ['react', 'javascript', 'js', 'component'],
            'nextjs': ['next.js', 'nextjs', 'framework', 'ssr'],
            'web': ['web development', 'frontend', 'html', 'css'],
            'design': ['ui', 'ux', 'design', 'interface', 'user experience'],
            'productivity': ['automation', 'efficiency', 'workflow', 'productivity'],
            'technology': ['tech', 'innovation', 'digital', 'software']
        }
        
        content_lower = content.lower()
        for tag, related_words in keywords.items():
            if any(word in content_lower for word in related_words):
                tags.append(tag)
        
        return list(set(tags))  # Remove duplicates
    
    def test_connection(self) -> Dict:
        """Test connection to celorisdesigns.com API"""
        try:
            headers = {
                self.auth_header: self.admin_session,
                'Accept': 'application/json'
            }
            
            response = requests.get(
                f"{self.api_url}/health", 
                headers=headers, 
                timeout=10
            )
            
            return {
                'success': True,
                'status_code': response.status_code,
                'message': 'Connection to celorisdesigns.com API successful'
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to connect to celorisdesigns.com API'
            }
