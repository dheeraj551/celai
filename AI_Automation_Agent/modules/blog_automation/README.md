# Blog Automation Module

## Overview
The Blog Automation module automatically generates and publishes blog posts using AI. It can create engaging content on various topics and post to multiple platforms.

## Features
- **AI Content Generation**: Creates high-quality blog posts using OpenAI GPT
- **Multiple Topics**: Supports multiple content categories
- **Automated Publishing**: Can post to WordPress, Medium, or custom platforms
- **SEO Optimization**: Includes metadata, tags, and optimization
- **Scheduling**: Posts according to configured frequency
- **Analytics**: Tracks performance and engagement

## Architecture
```
blog_automation/
├── blog_generator.py        # Core AI blog generation logic
├── content_publisher.py     # Platform publishing utilities
├── blog_scheduler.py        # Automated scheduling
├── blog_analytics.py        # Performance tracking
└── README.md               # This file
```

## Setup Requirements

### 1. Environment Variables
Add these to your `.env` file:
```bash
# Blog specific settings
BLOG_FREQUENCY=daily
BLOG_TOPICS=technology,ai,programming
BLOG_MAX_LENGTH=1000
BLOG_PUBLISH_TO=wordpress,medium
WORDPRESS_URL=https://yourblog.com
WORDPRESS_USERNAME=your_username
WORDPRESS_PASSWORD=your_app_password
MEDIUM_TOKEN=your_medium_token
```

### 2. Dependencies
```bash
pip install openai wordpress-xmlrpc medium-sdk requests beautifulsoup4
```

### 3. Database Setup
If using MySQL, create the blog table:
```sql
CREATE TABLE blog_posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    topic VARCHAR(100),
    status VARCHAR(50) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    published_at TIMESTAMP NULL,
    word_count INT,
    tags TEXT,
    is_auto_generated BOOLEAN DEFAULT TRUE,
    source_url VARCHAR(500),
    INDEX idx_status (status),
    INDEX idx_topic (topic),
    INDEX idx_created_at (created_at)
);
```

## Usage Examples

### Basic Blog Generation
```python
from modules.blog_automation.blog_generator import BlogGenerator

# Initialize the generator
blog_gen = BlogGenerator()

# Generate a blog post
blog_post = blog_gen.generate_blog(
    topic="Artificial Intelligence in Healthcare",
    max_words=800,
    target_audience="medical professionals"
)

print(f"Title: {blog_post['title']}")
print(f"Content: {blog_post['content'][:200]}...")
```

### Publishing to WordPress
```python
from modules.blog_automation.content_publisher import WordPressPublisher

# Initialize publisher
wp_publisher = WordPressPublisher(
    url="https://yourblog.com",
    username="your_username", 
    password="your_app_password"
)

# Publish blog post
result = wp_publisher.publish_post(
    title=blog_post['title'],
    content=blog_post['content'],
    tags=blog_post['tags'],
    category="Technology"
)

if result['success']:
    print(f"Published with ID: {result['post_id']}")
```

### Automated Scheduling
```python
from modules.blog_automation.blog_scheduler import BlogScheduler

# Initialize scheduler
scheduler = BlogScheduler()

# Schedule daily blog generation
scheduler.schedule_daily_blog_generation(
    topics=settings.BLOG_TOPICS.split(","),
    max_words=800,
    publish_immediately=True
)

# Start scheduler
scheduler.start()
```

## API Reference

### BlogGenerator Class
```python
class BlogGenerator:
    def generate_blog(self, topic: str, max_words: int = 800, 
                     target_audience: str = "general", 
                     style: str = "informative") -> dict
    def generate_blog_series(self, main_topic: str, num_posts: int) -> list
    def optimize_for_seo(self, blog_content: str, keywords: list) -> dict
```

### ContentPublisher Class
```python
class WordPressPublisher:
    def publish_post(self, title: str, content: str, 
                    tags: list = None, category: str = None) -> dict
    
class MediumPublisher:
    def publish_post(self, title: str, content: str, 
                    tags: list = None, publish_status: str = "draft") -> dict
```

### BlogScheduler Class
```python
class BlogScheduler:
    def schedule_daily_blog_generation(self, topics: list, **kwargs) -> None
    def schedule_weekly_blog_series(self, main_topic: str, **kwargs) -> None
    def start(self) -> None
    def stop(self) -> None
```

## Best Practices

### 1. Content Quality
- Always review AI-generated content before publishing
- Add human touches to make content more engaging
- Include relevant images and multimedia
- Use proper heading structure (H1, H2, H3)

### 2. SEO Optimization
- Include relevant keywords naturally in content
- Use meta descriptions (150-160 characters)
- Add alt text to images
- Create compelling titles with keywords

### 3. Publishing Strategy
- Post at optimal times for your audience
- Vary content length and format
- Use consistent branding
- Monitor performance and adjust

### 4. Error Handling
- Always handle API rate limits
- Implement retry mechanisms
- Log errors for debugging
- Have fallback content ready

## Common Issues & Solutions

### Issue: OpenAI API Rate Limits
**Solution**: Implement exponential backoff and request queuing
```python
import time
from openai.error import RateLimitError

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### Issue: WordPress Connection Failed
**Solution**: Check credentials and enable application passwords
```python
# WordPress requires application-specific passwords
# Go to: Users > Profile > Application Passwords
# Generate a new password and use it
```

### Issue: Content Too Generic
**Solution**: Use more specific prompts and examples
```python
better_prompt = f"""
Create a blog post about {topic} for {target_audience}.
Focus on recent developments in 2025.
Include specific examples and actionable insights.
Use a {style} writing style.
Target {max_words} words.
"""
```

## Next Steps
1. Configure your environment variables
2. Set up database connection
3. Test blog generation locally
4. Configure publishing platforms
5. Set up automated scheduling
6. Monitor and optimize performance

## Module Dependencies
- `config.settings` - Configuration settings
- `config.database` - Database connections
- `openai` - AI content generation
- `selenium/requests` - Web publishing

## Coming Next
- Module 2: Course Creation