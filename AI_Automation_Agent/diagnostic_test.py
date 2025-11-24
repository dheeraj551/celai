#!/usr/bin/env python3
"""
AI Automation Agent - Diagnostic Test Script
Tests the fixes for loading icon and background service issues
"""

import sys
import os
import requests
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def print_status(message):
    print(f"✅ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_imports():
    """Test if required modules can be imported"""
    print_info("Testing imports...")
    
    try:
        from config.settings import settings
        print_status("Settings import successful")
        
        # Check critical settings
        print_info(f"  Database Type: {settings.DATABASE_TYPE}")
        print_info(f"  Chatbot Port: {settings.CHATBOT_PORT}")
        print_info(f"  OpenAI API Key: {'Set' if settings.OPENAI_API_KEY else 'Not Set'}")
        print_info(f"  NextJS Blog API: {'Set' if settings.NEXTJS_BLOG_API else 'Not Set'}")
        
    except Exception as e:
        print_error(f"Settings import failed: {e}")
        return False
    
    try:
        from config.database import db_manager
        print_status("Database manager import successful")
        
        # Test database connection
        try:
            if db_manager.mongo_db is not None:
                db_manager.mongo_db.admin.command('ping')
                print_status("MongoDB connection successful")
            else:
                print_warning("MongoDB not connected (this may be OK for now)")
        except Exception as db_error:
            print_warning(f"MongoDB connection failed: {db_error}")
            
    except Exception as e:
        print_error(f"Database manager import failed: {e}")
        return False
    
    try:
        from agent_core import AIAutomationAgent
        print_status("Agent core import successful")
    except Exception as e:
        print_warning(f"Agent core import failed: {e} (this may be OK)")
    
    return True

def test_service_manager():
    """Test service manager functionality"""
    print_info("Testing service manager...")
    
    try:
        from service_manager import ServiceManager
        manager = ServiceManager()
        
        print_status("Service manager imported successfully")
        print_info(f"  PID file location: {manager.pid_file}")
        
        # Test if service is running
        if manager.is_running():
            pid = manager.get_pid()
            print_status(f"Service is running (PID: {pid})")
        else:
            print_info("Service is not currently running")
            
        return True
        
    except Exception as e:
        print_error(f"Service manager test failed: {e}")
        return False

def test_web_interface_imports():
    """Test web interface imports"""
    print_info("Testing web interface imports...")
    
    try:
        sys.path.append(str(project_root / "web_interface"))
        from app import WebInterface
        print_status("Web interface imports successful")
        return True
        
    except Exception as e:
        print_warning(f"Web interface import failed: {e}")
        return False

def test_api_endpoints():
    """Test if API endpoints are accessible"""
    print_info("Testing API endpoints...")
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/api/health",
        "/api/status", 
        "/api/blog/posts",
        "/api/analytics/summary"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print_status(f"Endpoint {endpoint} is accessible")
            else:
                print_warning(f"Endpoint {endpoint} returned status {response.status_code}")
        except requests.exceptions.ConnectionError:
            print_warning(f"Endpoint {endpoint} not accessible (service not running)")
        except Exception as e:
            print_error(f"Endpoint {endpoint} error: {e}")

def main():
    print("=" * 60)
    print("AI AUTOMATION AGENT - DIAGNOSTIC TEST")
    print("=" * 60)
    print()
    
    # Change to project directory
    os.chdir(project_root)
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    if test_imports():
        tests_passed += 1
    
    if test_service_manager():
        tests_passed += 1
        
    if test_web_interface_imports():
        tests_passed += 1
    
    # API endpoint test (only if service is running)
    print_info("Checking if web service is running...")
    try:
        response = requests.get("http://localhost:8000/api/health", timeout=2)
        if response.status_code == 200:
            print_status("Web service is running and responding")
            tests_passed += 1
            
            # Test specific endpoints
            test_api_endpoints()
        else:
            print_warning("Web service is running but not responding properly")
    except:
        print_warning("Web service is not running (this is OK if you haven't started it yet)")
    
    print()
    print("=" * 60)
    print(f"TEST RESULTS: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print_status("All tests passed! Your system should be working correctly.")
    elif tests_passed >= total_tests - 1:
        print_status("Most tests passed. System should be functional.")
    else:
        print_warning("Some tests failed. Please check the troubleshooting guide.")
    
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. If service is not running: python service_manager.py start")
    print("2. Check service status: python service_manager.py status")
    print("3. View logs if issues: python service_manager.py logs")
    print("4. Visit web interface: http://localhost:8000")
    print("5. Check health: http://localhost:8000/api/health")

if __name__ == "__main__":
    main()