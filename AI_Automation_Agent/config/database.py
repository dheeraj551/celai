"""
Database configuration and connection management
"""
import pymongo
import mysql.connector
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger
from .settings import settings

class DatabaseManager:
    """Manages database connections for both MongoDB and MySQL"""
    
    def __init__(self):
        self.mongo_client = None
        self.mongo_db = None
        self.mysql_engine = None
        self.mysql_session = None
        
    def connect_mongodb(self):
        """Connect to MongoDB"""
        try:
            self.mongo_client = pymongo.MongoClient(settings.MONGODB_URI)
            # Test connection
            self.mongo_client.admin.command('ping')
            logger.info("MongoDB connected successfully")
            
            # Get database name from URI or use default
            db_name = "ai_automation"
            if "/" in settings.MONGODB_URI:
                # Extract database name from URI if present
                db_name = settings.MONGODB_URI.split("/")[-1]
                if not db_name:
                    db_name = "ai_automation"
            
            self.mongo_db = self.mongo_client[db_name]
            
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            return False
        
        return True
    
    def connect_mysql(self):
        """Connect to MySQL"""
        try:
            # Create SQLAlchemy engine for MySQL
            mysql_url = f"mysql+mysqlconnector://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"
            self.mysql_engine = create_engine(mysql_url)
            
            # Test connection
            with self.mysql_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            # Create session factory
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.mysql_engine)
            self.mysql_session = SessionLocal
            
            logger.info("MySQL connected successfully")
            
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            return False
        
        return True
    
    def connect(self):
        """Connect to the configured database"""
        if settings.DATABASE_TYPE.lower() == "mongodb":
            return self.connect_mongodb()
        elif settings.DATABASE_TYPE.lower() == "mysql":
            return self.connect_mysql()
        else:
            logger.error(f"Unsupported database type: {settings.DATABASE_TYPE}")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB disconnected")
        
        if self.mysql_engine:
            self.mysql_engine.dispose()
            logger.info("MySQL disconnected")
    
    def get_mongodb_collection(self, collection_name):
        """Get MongoDB collection"""
        if not self.mongo_db:
            raise Exception("MongoDB not connected")
        return self.mongo_db[collection_name]
    
    def get_mysql_session(self):
        """Get MySQL session"""
        if not self.mysql_session:
            raise Exception("MySQL not connected")
        return self.mysql_session

# Global database manager instance
db_manager = DatabaseManager()

# SQLAlchemy base for MySQL models
Base = declarative_base()

# MySQL Models for Blog Module
class BlogPost:
    """SQLAlchemy model for blog posts"""
    from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
    from sqlalchemy.ext.declarative import declarative_base
    import datetime
    
    __tablename__ = "blog_posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    topic = Column(String(100))
    status = Column(String(50), default="draft")  # draft, published, scheduled
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    published_at = Column(DateTime)
    word_count = Column(Integer)
    tags = Column(Text)  # JSON string of tags
    is_auto_generated = Column(Boolean, default=True)
    source_url = Column(String(500))  # For reference
    
    def __repr__(self):
        return f"<BlogPost(id={self.id}, title='{self.title}')>"

# Initialize database connection
def init_database():
    """Initialize database connection"""
    success = db_manager.connect()
    
    if success and settings.DATABASE_TYPE.lower() == "mysql":
        # Create tables for MySQL
        Base.metadata.create_all(bind=db_manager.mysql_engine)
        logger.info("MySQL tables created/verified")
    
    return success

# Get database collection for MongoDB or MySQL
def get_collection(collection_name):
    """Get database collection (MongoDB) or table reference (MySQL)"""
    if settings.DATABASE_TYPE.lower() == "mongodb":
        return db_manager.get_mongodb_collection(collection_name)
    else:
        return db_manager.get_mysql_session()
