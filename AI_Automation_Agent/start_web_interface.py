#!/usr/bin/env python3
"""
AI Automation Agent - Web Interface Startup Script
Starts the web interface for monitoring and configuring the AI agent
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from web_interface.app import main as web_main
    from config.settings import settings
    from loguru import logger
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def setup_logging():
    """Setup logging for the web interface"""
    # Remove default logger
    logger.remove()
    
    # Add console logging
    logger.add(
        sys.stdout,
        format="<green>{time:HH:mm:ss}</green> | <level>{level:8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> | {message}",
        level="INFO"
    )
    
    # Add file logging
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logger.add(
        log_dir / "web_interface.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:8} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )


def check_dependencies():
    """Check if required dependencies are available"""
    required_modules = [
        'fastapi',
        'uvicorn',
        'jinja2',
        'python-multipart'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        logger.error(f"Missing required modules: {', '.join(missing_modules)}")
        logger.info("Please install them using: pip install -r requirements.txt")
        return False
    
    return True


def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "web_interface/static/css",
        "web_interface/static/js",
        "web_interface/static/images",
        "web_interface/templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Created directory: {directory}")


def main():
    """Main startup function"""
    print("=" * 60)
    print("AI AUTOMATION AGENT - WEB INTERFACE")
    print("=" * 60)
    
    # Setup logging
    setup_logging()
    
    logger.info("Starting AI Automation Agent Web Interface...")
    
    # Create directories
    create_directories()
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Missing dependencies. Please install requirements.")
        return 1
    
    # Check if web interface port is available
    port = settings.CHATBOT_PORT
    logger.info(f"Web interface will be available at: http://localhost:{port}")
    
    try:
        # Import and run the web interface
        logger.info("Initializing web interface...")
        
        # Run the FastAPI application
        web_main()
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Failed to start web interface: {e}")
        return 1
    
    logger.info("Web interface shutdown complete")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
