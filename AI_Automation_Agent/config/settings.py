"""
Configuration settings for AI Automation Agent
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # Database Configuration
    DATABASE_TYPE = os.getenv("DATABASE_TYPE", "mongodb")  # "mongodb" or "mysql"
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "ai_automation")
    
    # AI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Next.js Integration (Primary Publishing Method)
    NEXTJS_BLOG_API = os.getenv("NEXTJS_BLOG_API")
    # Session-based Authentication (RECOMMENDED)
    NEXTJS_ADMIN_SESSION = os.getenv("NEXTJS_ADMIN_SESSION")
    NEXTJS_AUTH_HEADER = os.getenv("NEXTJS_AUTH_HEADER", "x-admin-session")
    NEXTJS_API_TIMEOUT = int(os.getenv("NEXTJS_API_TIMEOUT", "30"))
    NEXTJS_RATE_LIMIT_AWARE = os.getenv("NEXTJS_RATE_LIMIT_AWARE", "true").lower() == "true"
    # Legacy API Key Authentication (DEPRECATED)
    NEXTJS_API_KEY = os.getenv("NEXTJS_API_KEY")
    
    # Legacy Platform Support (Optional)
    WORDPRESS_URL = os.getenv("WORDPRESS_URL")
    WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
    WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
    MEDIUM_ACCESS_TOKEN = os.getenv("MEDIUM_ACCESS_TOKEN")
    
    # Scheduling
    ENABLE_SCHEDULER = os.getenv("ENABLE_SCHEDULER", "true").lower() == "true"
    SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "UTC")
    BLOG_GENERATION_TIME = os.getenv("BLOG_GENERATION_TIME", "09:00")
    BLOG_GENERATION_DAYS = os.getenv("BLOG_GENERATION_DAYS", "mon,tue,wed,thu,fri").split(",")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/agent.log")
    LOG_MAX_SIZE = int(os.getenv("LOG_MAX_SIZE", "10485760"))  # 10MB
    LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    DETAILED_API_LOGGING = os.getenv("DETAILED_API_LOGGING", "true").lower() == "true"
    
    # Blog Settings
    BLOG_FREQUENCY = os.getenv("BLOG_FREQUENCY", "daily")  # daily, weekly
    BLOG_TOPICS = os.getenv("BLOG_TOPICS", "technology,ai,programming").split(",")
    BLOG_MAX_LENGTH = int(os.getenv("BLOG_MAX_LENGTH", "1000"))
    BLOG_DEFAULT_STATUS = os.getenv("BLOG_DEFAULT_STATUS", "draft")  # draft, published
    SEO_OPTIMIZATION = os.getenv("SEO_OPTIMIZATION", "true").lower() == "true"
    
    # Security & Performance
    API_RETRY_ATTEMPTS = int(os.getenv("API_RETRY_ATTEMPTS", "3"))
    API_RETRY_DELAY = int(os.getenv("API_RETRY_DELAY", "5"))
    MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "5"))
    
    # Course Settings
    COURSE_MAX_MODULES = int(os.getenv("COURSE_MAX_MODULES", "10"))
    COURSE_MAX_LESSONS = int(os.getenv("COURSE_MAX_LESSONS", "5"))
    
    # Job Aggregation (Future Module)
    JOB_SOURCES = os.getenv("JOB_SOURCES", "linkedin,indeed,glassdoor").split(",")
    JOB_UPDATE_FREQUENCY = os.getenv("JOB_UPDATE_FREQUENCY", "6h")
    
    # Course Settings (Future Module)
    COURSE_MAX_MODULES = int(os.getenv("COURSE_MAX_MODULES", "10"))
    COURSE_MAX_LESSONS = int(os.getenv("COURSE_MAX_LESSONS", "5"))
    
    # Chatbot & Web Interface
    CHATBOT_ENABLED = os.getenv("CHATBOT_ENABLED", "true").lower() == "true"
    CHATBOT_PORT = int(os.getenv("CHATBOT_PORT", "8000"))
    SESSION_SECRET = os.getenv("SESSION_SECRET", "default-secret-change-in-production")

# Create settings instance
settings = Settings()
