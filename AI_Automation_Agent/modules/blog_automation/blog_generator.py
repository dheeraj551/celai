"""
Blog Generator Module
Handles AI-powered blog content generation using OpenAI
"""
import openai
import json
import re
from typing import Dict, List, Optional
from loguru import logger
from datetime import datetime
import random

from config.settings import settings


class BlogGenerator:
    """
    AI-powered blog post generator using OpenAI GPT
    """
    
    def __init__(self):
        """Initialize the blog generator with OpenAI configuration"""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.AI_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        
        # Blog templates for different styles
        self.blog_templates = {
            "informative": {
                "structure": "introduction,main_points,conclusion",
                "tone": "professional and educational"
            },
            "casual": {
                "structure": "hook,story,insights,call_to_action",
                "tone": "conversational and friendly"
            },
            "technical": {
                "structure": "overview,technical_details,implementation,conclusion",
                "tone": "detailed and precise"
            },
            "how_to": {
                "structure": "introduction,step_by_step_guide,troubleshooting,tips",
                "tone": "instructional and clear"
            }
        }
    
    def generate_blog(self, topic: str, max_words: int = 800, 
                     target_audience: str = "general", 
                     style: str = "informative") -> Dict:
        """
        Generate a complete blog post on a given topic
        
        Args:
            topic: The main topic for the blog post
            max_words: Maximum word count for the blog
            target_audience: Who the blog is written for
            style: Writing style (informative, casual, technical, how_to)
            
        Returns:
            Dictionary containing blog data
        """
        try:
            # Validate inputs
            if not topic.strip():
                raise ValueError("Topic cannot be empty")
            
            if style not in self.blog_templates:
                logger.warning(f"Unknown style '{style}', using 'informative'")
                style = "informative"
            
            # Generate blog content
            blog_data = self._generate_content(topic, max_words, target_audience, style)
            
            # Process and enhance the content
            processed_data = self._process_blog_content(blog_data, topic)
            
            logger.info(f"Successfully generated blog post: '{processed_data['title']}'")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error generating blog post: {e}")
            raise
    
    def _generate_content(self, topic: str, max_words: int, 
                         target_audience: str, style: str) -> Dict:
        """Generate raw content using OpenAI"""
        
        template = self.blog_templates[style]
        
        prompt = f"""
        Create a high-quality blog post about "{topic}" for {target_audience}.
        
        Requirements:
        - Maximum {max_words} words
        - Writing style: {template['tone']}
        - Structure: {template['structure']}
        - Include an engaging title
        - Add relevant subheadings (H2, H3)
        - Include 3-5 relevant tags
        - Make it SEO-friendly with natural keyword usage
        - Focus on 2025 trends and developments
        - Provide actionable insights or practical value
        
        Format your response as a JSON object with this structure:
        {{
            "title": "Compelling blog post title",
            "content": "Full blog post content with markdown formatting",
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
            "meta_description": "Brief description for SEO (150-160 characters)",
            "word_count": actual_word_count
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert content writer who creates engaging, well-structured blog posts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Parse the response
            content = response.choices[0].message.content
            blog_data = json.loads(content)
            
            return blog_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {e}")
            # Fallback to extract content from non-JSON response
            return self._extract_content_from_text(content, topic)
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    def _extract_content_from_text(self, content: str, topic: str) -> Dict:
        """Extract blog data from non-JSON response"""
        lines = content.split('\n')
        title = lines[0].strip() if lines else f"Understanding {topic}"
        
        # Try to find tags in the content
        tags = []
        tag_pattern = r'#(\w+)'
        tag_matches = re.findall(tag_pattern, content)
        if tag_matches:
            tags = tag_matches[:5]
        else:
            # Generate tags based on topic
            words = topic.lower().split()
            tags = words[:3] + ["blog", "article"]
        
        return {
            "title": title,
            "content": content,
            "tags": tags,
            "meta_description": f"Learn about {topic} and its implications in 2025.",
            "word_count": len(content.split())
        }
    
    def _process_blog_content(self, blog_data: Dict, topic: str) -> Dict:
        """Process and enhance blog content"""
        
        # Clean and format content
        content = blog_data['content'].strip()
        
        # Ensure proper heading structure
        content = self._ensure_heading_structure(content)
        
        # Add metadata
        word_count = len(content.split())
        if word_count > settings.BLOG_MAX_LENGTH:
            content = self._trim_content(content, settings.BLOG_MAX_LENGTH)
            word_count = settings.BLOG_MAX_LENGTH
        
        # Generate slug from title
        slug = self._generate_slug(blog_data['title'])
        
        # Add publishing metadata
        processed_data = {
            **blog_data,
            'content': content,
            'word_count': word_count,
            'slug': slug,
            'created_at': datetime.now().isoformat(),
            'topic': topic,
            'is_auto_generated': True,
            'status': 'draft'
        }
        
        return processed_data
    
    def _ensure_heading_structure(self, content: str) -> str:
        """Ensure proper heading structure in markdown"""
        lines = content.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            
            # If line looks like a heading but doesn't have #, add it
            if (line and 
                len(line) > 10 and 
                len(line) < 100 and 
                not line.startswith('#') and
                not line.startswith('-') and
                not line.startswith('*') and
                line.endswith(':')):
                processed_lines.append(f"## {line}")
            else:
                processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def _trim_content(self, content: str, max_words: int) -> str:
        """Trim content to specified word count"""
        words = content.split()
        if len(words) <= max_words:
            return content
        
        trimmed_words = words[:max_words]
        
        # Try to end at a sentence boundary
        trimmed_text = ' '.join(trimmed_words)
        last_period = trimmed_text.rfind('.')
        last_exclamation = trimmed_text.rfind('!')
        last_question = trimmed_text.rfind('?')
        
        end_pos = max(last_period, last_exclamation, last_question)
        if end_pos > len(trimmed_text) * 0.8:  # Don't cut too much
            return trimmed_text[:end_pos + 1]
        
        return trimmed_text + "..."
    
    def _generate_slug(self, title: str) -> str:
        """Generate URL-friendly slug from title"""
        # Convert to lowercase
        slug = title.lower()
        
        # Replace spaces and special characters with hyphens
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        return slug
    
    def generate_blog_series(self, main_topic: str, num_posts: int = 5) -> List[Dict]:
        """
        Generate a series of related blog posts
        
        Args:
            main_topic: Main topic for the series
            num_posts: Number of posts to generate
            
        Returns:
            List of blog post dictionaries
        """
        try:
            # Generate subtopics for the series
            series_plan = self._generate_series_plan(main_topic, num_posts)
            
            blog_series = []
            for i, subtopic in enumerate(series_plan, 1):
                logger.info(f"Generating blog {i}/{num_posts}: {subtopic}")
                
                blog_post = self.generate_blog(
                    topic=subtopic,
                    max_words=int(settings.BLOG_MAX_LENGTH * 0.8),  # Slightly shorter for series
                    target_audience="general",
                    style="informative"
                )
                
                # Add series metadata
                blog_post['series_position'] = i
                blog_post['series_topic'] = main_topic
                blog_post['series_slug'] = f"{main_topic.lower().replace(' ', '-')}-part-{i}"
                
                blog_series.append(blog_post)
            
            logger.info(f"Successfully generated blog series: {len(blog_series)} posts")
            return blog_series
            
        except Exception as e:
            logger.error(f"Error generating blog series: {e}")
            raise
    
    def _generate_series_plan(self, main_topic: str, num_posts: int) -> List[str]:
        """Generate subtopics for a blog series"""
        
        prompt = f"""
        Create a detailed plan for a blog series about "{main_topic}".
        
        Requirements:
        - Generate {num_posts} related subtopics
        - Each subtopic should be unique and build on the previous one
        - Topics should progress from basic concepts to advanced applications
        - Make topics specific enough to write detailed blog posts about
        - Focus on 2025 developments and trends
        
        Format your response as a JSON array of strings:
        ["Subtopic 1", "Subtopic 2", "Subtopic 3", ...]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert content strategist who creates logical, engaging blog series."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            series_plan = json.loads(content)
            
            if not isinstance(series_plan, list) or len(series_plan) != num_posts:
                # Fallback to simple subtopic generation
                return self._generate_simple_series_plan(main_topic, num_posts)
            
            return series_plan
            
        except Exception as e:
            logger.warning(f"Failed to generate series plan: {e}")
            return self._generate_simple_series_plan(main_topic, num_posts)
    
    def _generate_simple_series_plan(self, main_topic: str, num_posts: int) -> List[str]:
        """Simple fallback series plan generator"""
        base_plan = [
            f"Introduction to {main_topic}",
            f"Getting Started with {main_topic}",
            f"Advanced {main_topic} Techniques",
            f"{main_topic} Best Practices",
            f"Future of {main_topic}",
            f"{main_topic} Case Studies",
            f"Common {main_topic} Mistakes",
            f"{main_topic} Tools and Resources",
            f"{main_topic} vs Alternatives",
            f"Mastering {main_topic}"
        ]
        
        return base_plan[:num_posts]
    
    def optimize_for_seo(self, blog_content: str, keywords: List[str]) -> Dict:
        """
        Optimize blog content for SEO
        
        Args:
            blog_content: The blog post content
            keywords: Target keywords for SEO
            
        Returns:
            Dictionary with SEO optimization data
        """
        try:
            # Analyze keyword density
            content_lower = blog_content.lower()
            keyword_analysis = {}
            
            for keyword in keywords:
                keyword_count = content_lower.count(keyword.lower())
                keyword_density = (keyword_count / len(blog_content.split())) * 100
                
                keyword_analysis[keyword] = {
                    'count': keyword_count,
                    'density': round(keyword_density, 2)
                }
            
            # Generate SEO recommendations
            recommendations = []
            
            if any(data['density'] < 1 for data in keyword_analysis.values()):
                recommendations.append("Consider increasing keyword density for better SEO")
            
            if any(data['density'] > 3 for data in keyword_analysis.values()):
                recommendations.append("Some keywords may be overused - consider reducing density")
            
            # Check for headings with keywords
            heading_count = blog_content.count('#')
            if heading_count < 3:
                recommendations.append("Add more subheadings to improve content structure")
            
            return {
                'keyword_analysis': keyword_analysis,
                'recommendations': recommendations,
                'seo_score': self._calculate_seo_score(blog_content, keyword_analysis),
                'optimized_content': self._add_seo_enhancements(blog_content, keywords)
            }
            
        except Exception as e:
            logger.error(f"Error optimizing for SEO: {e}")
            return {'error': str(e)}
    
    def _calculate_seo_score(self, content: str, keyword_analysis: Dict) -> int:
        """Calculate SEO score (0-100)"""
        score = 50  # Base score
        
        # Word count bonus
        word_count = len(content.split())
        if 300 <= word_count <= 1500:
            score += 20
        elif word_count < 300:
            score -= 10
        
        # Heading structure bonus
        heading_count = content.count('#')
        if heading_count >= 3:
            score += 15
        elif heading_count >= 2:
            score += 10
        
        # Keyword optimization
        avg_density = sum(data['density'] for data in keyword_analysis.values()) / len(keyword_analysis)
        if 1 <= avg_density <= 2.5:
            score += 15
        elif avg_density > 3:
            score -= 10
        
        return min(100, max(0, score))
    
    def _add_seo_enhancements(self, content: str, keywords: List[str]) -> str:
        """Add SEO enhancements to content"""
        enhanced_content = content
        
        # Add keywords to first paragraph if not present
        lines = enhanced_content.split('\n')
        first_paragraph_idx = -1
        
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#') and not line.startswith('-'):
                first_paragraph_idx = i
                break
        
        if first_paragraph_idx != -1 and keywords:
            first_line = lines[first_paragraph_idx]
            if not any(keyword.lower() in first_line.lower() for keyword in keywords[:2]):
                # Add first keyword naturally to first paragraph
                enhanced_lines = lines.copy()
                enhanced_lines[first_paragraph_idx] = f"{first_line} Understanding {keywords[0]} is crucial."
                enhanced_content = '\n'.join(enhanced_lines)
        
        return enhanced_content


# Example usage and testing
if __name__ == "__main__":
    # Initialize the blog generator
    generator = BlogGenerator()
    
    # Test single blog generation
    try:
        blog = generator.generate_blog(
            topic="Artificial Intelligence in Healthcare",
            max_words=500,
            target_audience="medical professionals",
            style="informative"
        )
        
        print("Generated Blog Post:")
        print(f"Title: {blog['title']}")
        print(f"Word Count: {blog['word_count']}")
        print(f"Tags: {', '.join(blog['tags'])}")
        print(f"\nContent Preview:\n{blog['content'][:300]}...")
        
    except Exception as e:
        print(f"Error: {e}")
