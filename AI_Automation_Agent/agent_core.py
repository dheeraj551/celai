"""
AI Automation Agent - Core Module
Main controller for the AI automation agent system
"""
import os
import sys
import time
import signal
import threading
from datetime import datetime
from typing import Dict, List, Optional
from loguru import logger

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from config.database import init_database, db_manager


class AIAutomationAgent:
    """
    Main AI Automation Agent controller
    Manages all automation modules and provides a unified interface
    """
    
    def __init__(self):
        """Initialize the AI automation agent"""
        self.name = "AI Automation Agent"
        self.version = "1.0.0"
        self.is_running = False
        self.modules = {}
        self.start_time = None
        
        # Setup logging
        self._setup_logging()
        
        # Initialize components
        self._initialize_components()
        
        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        logger.remove()  # Remove default handler
        
        # Add file logging
        os.makedirs("logs", exist_ok=True)
        logger.add(
            "logs/agent.log",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
            level=settings.LOG_LEVEL,
            rotation=f"{settings.LOG_MAX_SIZE // 1024 // 1024} MB",
            retention=f"{settings.LOG_BACKUP_COUNT} files",
            compression="zip"
        )
        
        # Add console logging
        logger.add(
            sys.stdout,
            format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | {message}",
            level="INFO"
        )
    
    def _initialize_components(self):
        """Initialize core components"""
        try:
            # Initialize database
            logger.info("Initializing database connection...")
            if not init_database():
                raise Exception("Failed to initialize database")
            
            logger.info("Database connection established")
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def load_module(self, module_name: str) -> bool:
        """
        Load a specific automation module
        
        Args:
            module_name: Name of the module to load
            
        Returns:
            Success status
        """
        try:
            if module_name in self.modules:
                logger.warning(f"Module {module_name} already loaded")
                return True
            
            logger.info(f"Loading module: {module_name}")
            
            if module_name == "blog_automation":
                from modules.blog_automation.blog_scheduler import BlogScheduler
                self.modules[module_name] = BlogScheduler()
                
            elif module_name == "course_creation":
                # Module 2 - Course Creation (to be implemented)
                logger.info("Course creation module coming in Module 2")
                return False
                
            elif module_name == "job_aggregation":
                # Module 3 - Job Aggregation (to be implemented)
                logger.info("Job aggregation module coming in Module 3")
                return False
                
            elif module_name == "user_management":
                # Module 4 - User Management (to be implemented)
                logger.info("User management module coming in Module 4")
                return False
                
            elif module_name == "chatbot":
                # Module 5 - Chatbot (to be implemented)
                logger.info("Chatbot module coming in Module 5")
                return False
                
            else:
                logger.error(f"Unknown module: {module_name}")
                return False
            
            logger.info(f"Successfully loaded module: {module_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load module {module_name}: {e}")
            return False
    
    def start_agent(self):
        """Start the AI automation agent"""
        if self.is_running:
            logger.warning("Agent is already running")
            return
        
        try:
            logger.info(f"Starting {self.name} v{self.version}")
            self.start_time = datetime.now()
            self.is_running = True
            
            # Load and start enabled modules
            if settings.ENABLE_SCHEDULER:
                if self.load_module("blog_automation"):
                    blog_scheduler = self.modules["blog_automation"]
                    blog_scheduler.start()
                    logger.info("Blog automation scheduler started")
            
            # Keep the agent running
            self._main_loop()
            
        except Exception as e:
            logger.error(f"Failed to start agent: {e}")
            self.shutdown()
            raise
    
    def _main_loop(self):
        """Main agent loop"""
        logger.info("Agent main loop started")
        
        try:
            while self.is_running:
                # Monitor module health
                self._monitor_modules()
                
                # Update statistics
                self._update_statistics()
                
                # Sleep for a short interval
                time.sleep(10)
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            self.shutdown()
    
    def _monitor_modules(self):
        """Monitor module health and performance"""
        for module_name, module in self.modules.items():
            try:
                if hasattr(module, 'get_statistics'):
                    stats = module.get_statistics()
                    logger.debug(f"{module_name} stats: {stats}")
                    
            except Exception as e:
                logger.error(f"Error monitoring module {module_name}: {e}")
    
    def _update_statistics(self):
        """Update overall agent statistics"""
        try:
            uptime = datetime.now() - self.start_time if self.start_time else None
            
            stats = {
                'agent_name': self.name,
                'version': self.version,
                'is_running': self.is_running,
                'uptime_seconds': uptime.total_seconds() if uptime else 0,
                'modules_loaded': list(self.modules.keys()),
                'total_modules': len(self.modules),
                'database_connected': db_manager.mongo_db is not None or db_manager.mysql_session is not None,
                'last_updated': datetime.now().isoformat()
            }
            
            # Log summary every hour
            current_minute = datetime.now().minute
            if current_minute == 0:  # Top of each hour
                logger.info(f"Agent Status - Uptime: {uptime}, Modules: {len(self.modules)}")
                
        except Exception as e:
            logger.error(f"Error updating statistics: {e}")
    
    def stop_agent(self):
        """Stop the AI automation agent"""
        self.shutdown()
    
    def shutdown(self):
        """Shutdown the agent gracefully"""
        if not self.is_running:
            return
        
        logger.info("Shutting down AI Automation Agent...")
        self.is_running = False
        
        # Stop all modules
        for module_name, module in self.modules.items():
            try:
                if hasattr(module, 'stop'):
                    module.stop()
                    logger.info(f"Stopped module: {module_name}")
            except Exception as e:
                logger.error(f"Error stopping module {module_name}: {e}")
        
        # Disconnect from database
        try:
            db_manager.disconnect()
            logger.info("Database disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting from database: {e}")
        
        logger.info("Agent shutdown complete")
    
    def get_agent_status(self) -> Dict:
        """Get comprehensive agent status"""
        uptime = datetime.now() - self.start_time if self.start_time else None
        
        return {
            'agent': {
                'name': self.name,
                'version': self.version,
                'is_running': self.is_running,
                'start_time': self.start_time.isoformat() if self.start_time else None,
                'uptime_seconds': uptime.total_seconds() if uptime else 0
            },
            'modules': {
                name: module.get_statistics() if hasattr(module, 'get_statistics') else {'status': 'running'}
                for name, module in self.modules.items()
            },
            'database': {
                'type': settings.DATABASE_TYPE,
                'connected': db_manager.mongo_db is not None or db_manager.mysql_session is not None
            },
            'configuration': {
                'scheduler_enabled': settings.ENABLE_SCHEDULER,
                'nextjs_enabled': bool(settings.NEXTJS_BLOG_API and settings.NEXTJS_API_KEY),
                'log_level': settings.LOG_LEVEL
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def execute_manual_task(self, task_type: str, **kwargs) -> Dict:
        """
        Execute a manual task
        
        Args:
            task_type: Type of task to execute
            **kwargs: Task-specific parameters
            
        Returns:
            Task execution results
        """
        try:
            logger.info(f"Executing manual task: {task_type}")
            
            if task_type == "generate_blog":
                if "blog_automation" not in self.modules:
                    if not self.load_module("blog_automation"):
                        return {'success': False, 'error': 'Failed to load blog automation module'}
                
                blog_scheduler = self.modules["blog_automation"]
                result = blog_scheduler.manual_blog_generation(
                    topic=kwargs.get('topic', 'AI technology'),
                    max_words=kwargs.get('max_words', 800),
                    publish_immediately=kwargs.get('publish_immediately', False)
                )
                
                return {
                    'success': True,
                    'task_type': task_type,
                    'result': result
                }
            
            elif task_type == "get_blog_series":
                if "blog_automation" not in self.modules:
                    if not self.load_module("blog_automation"):
                        return {'success': False, 'error': 'Failed to load blog automation module'}
                
                blog_scheduler = self.modules["blog_automation"]
                result = blog_scheduler.manual_blog_series(
                    main_topic=kwargs.get('main_topic', 'AI Programming'),
                    num_posts=kwargs.get('num_posts', 3)
                )
                
                return {
                    'success': True,
                    'task_type': task_type,
                    'result': result
                }
            
            elif task_type == "get_agent_status":
                status = self.get_agent_status()
                return {
                    'success': True,
                    'task_type': task_type,
                    'result': status
                }
            
            else:
                return {
                    'success': False,
                    'error': f'Unknown task type: {task_type}',
                    'available_tasks': ['generate_blog', 'get_blog_series', 'get_agent_status']
                }
                
        except Exception as e:
            logger.error(f"Error executing manual task {task_type}: {e}")
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Main entry point for the AI Automation Agent"""
    try:
        print("=" * 60)
        print("AI AUTOMATION AGENT")
        print("=" * 60)
        print("Starting AI automation agent...")
        
        # Create and start the agent
        agent = AIAutomationAgent()
        
        # Start the agent
        agent.start_agent()
        
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, shutting down...")
    except Exception as e:
        print(f"Agent failed to start: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    # Run the agent
    exit_code = main()
    sys.exit(exit_code)
