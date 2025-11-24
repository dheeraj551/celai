#!/usr/bin/env python3
"""
AI Automation Agent - Background Service Script
Starts the web interface as a background service with proper logging
"""

import os
import sys
import signal
import subprocess
import time
import logging
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def setup_logging():
    """Setup logging for the background service"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / "background_service.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def check_mongodb():
    """Check if MongoDB is running"""
    import pymongo
    
    try:
        # Try to connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        logger.info("✓ MongoDB connection successful")
        return True
    except Exception as e:
        logger.error(f"✗ MongoDB connection failed: {e}")
        logger.info("Starting MongoDB...")
        try:
            # Try to start MongoDB
            subprocess.run(['sudo', 'systemctl', 'start', 'mongod'], check=False)
            time.sleep(5)  # Wait for MongoDB to start
            return check_mongodb()  # Recursively check again
        except Exception as start_error:
            logger.error(f"Failed to start MongoDB: {start_error}")
            return False

def check_dependencies():
    """Check if all required dependencies are installed"""
    import importlib.util
    
    required_modules = [
        'fastapi',
        'uvicorn', 
        'pymongo',
        'loguru',
        'python-dotenv',
        'jinja2'
    ]
    
    missing = []
    for module in required_modules:
        if importlib.util.find_spec(module) is None:
            missing.append(module)
    
    if missing:
        logger.error(f"Missing required modules: {', '.join(missing)}")
        logger.info("Installing missing modules...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
            logger.info("Missing modules installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install modules: {e}")
            return False
    
    return True

def start_web_interface():
    """Start the web interface"""
    try:
        logger.info("Starting AI Automation Agent Web Interface...")
        
        # Use nohup to run in background and redirect output
        process = subprocess.Popen([
            sys.executable, 
            str(project_root / 'start_web_interface.py')
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        logger.info(f"Web interface started with PID: {process.pid}")
        
        # Wait a moment to ensure it starts successfully
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            logger.info("✓ Web interface is running successfully")
            
            # Save PID for later management
            with open(project_root / 'web_interface.pid', 'w') as f:
                f.write(str(process.pid))
                
            return process
        else:
            stdout, stderr = process.communicate()
            logger.error(f"Web interface failed to start")
            logger.error(f"STDOUT: {stdout.decode()}")
            logger.error(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        logger.error(f"Failed to start web interface: {e}")
        return None

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    
    # Stop the web interface if it's running
    try:
        with open(project_root / 'web_interface.pid', 'r') as f:
            pid = int(f.read().strip())
        logger.info(f"Stopping web interface (PID: {pid})...")
        os.kill(pid, signal.SIGTERM)
    except (FileNotFoundError, ValueError, ProcessLookupError):
        pass
    
    # Clean up PID file
    try:
        os.remove(project_root / 'web_interface.pid')
    except FileNotFoundError:
        pass
    
    logger.info("Background service stopped")
    sys.exit(0)

def main():
    """Main function"""
    global logger
    logger = setup_logging()
    
    logger.info("=" * 60)
    logger.info("AI AUTOMATION AGENT - BACKGROUND SERVICE")
    logger.info("=" * 60)
    logger.info(f"Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Dependency check failed")
        return 1
    
    # Check MongoDB
    if not check_mongodb():
        logger.warning("MongoDB check failed, but continuing...")
    
    # Start web interface
    process = start_web_interface()
    
    if process:
        logger.info("=" * 60)
        logger.info("BACKGROUND SERVICE RUNNING")
        logger.info("=" * 60)
        logger.info(f"Web interface: http://localhost:8000")
        logger.info(f"PID file: {project_root}/web_interface.pid")
        logger.info(f"Logs: {project_root}/logs/background_service.log")
        logger.info("=" * 60)
        logger.info("To stop: send SIGTERM or Ctrl+C")
        logger.info("To view logs: tail -f logs/background_service.log")
        
        # Keep running and monitor the process
        try:
            while True:
                if process.poll() is not None:
                    logger.error("Web interface process died unexpectedly")
                    logger.info("Attempting to restart...")
                    process = start_web_interface()
                    if not process:
                        logger.error("Failed to restart web interface")
                        break
                
                time.sleep(30)  # Check every 30 seconds
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            signal_handler(signal.SIGTERM, None)
    else:
        logger.error("Failed to start web interface")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)