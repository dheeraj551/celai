#!/bin/bash
"""
AI Automation Agent - Background Service Management Script
Provides commands to start, stop, restart, and check status of the web interface
"""

import sys
import os
import subprocess
import signal
from pathlib import Path
import json

class ServiceManager:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.pid_file = self.project_root / "web_interface.pid"
        self.service_name = "ai-automation-agent"
    
    def start(self):
        """Start the service in background"""
        if self.is_running():
            print(f"✓ {self.service_name} is already running (PID: {self.get_pid()})")
            return
        
        print(f"Starting {self.service_name}...")
        
        try:
            # Start the background service
            process = subprocess.Popen([
                sys.executable, 
                str(self.project_root / 'start_background_service.py')
            ], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=str(self.project_root)
            )
            
            print(f"✓ {self.service_name} started with PID: {process.pid}")
            
            # Wait a moment and check if it's running
            import time
            time.sleep(3)
            
            if self.is_running():
                print(f"✓ Service is running successfully")
                print(f"🌐 Web Interface: http://localhost:8000")
                print(f"📊 Status: http://localhost:8000/api/status")
            else:
                print("✗ Service failed to start properly")
                # Get error output
                stdout, stderr = process.communicate()
                if stderr:
                    print(f"Error: {stderr.decode()}")
                    
        except Exception as e:
            print(f"✗ Failed to start service: {e}")
    
    def stop(self):
        """Stop the service"""
        if not self.is_running():
            print(f"✓ {self.service_name} is not running")
            return
        
        pid = self.get_pid()
        print(f"Stopping {self.service_name} (PID: {pid})...")
        
        try:
            os.kill(pid, signal.SIGTERM)
            print("✓ Service stopped gracefully")
            
            # Wait and verify it's stopped
            import time
            time.sleep(2)
            if not self.is_running():
                print("✓ Service stopped successfully")
            else:
                print("⚠ Service didn't stop gracefully, forcing...")
                os.kill(pid, signal.SIGKILL)
                print("✓ Service stopped by force")
                
        except ProcessLookupError:
            print("✓ Service was already stopped")
        except Exception as e:
            print(f"✗ Failed to stop service: {e}")
    
    def restart(self):
        """Restart the service"""
        print(f"Restarting {self.service_name}...")
        self.stop()
        import time
        time.sleep(2)
        self.start()
    
    def status(self):
        """Check service status"""
        if self.is_running():
            pid = self.get_pid()
            print(f"✓ {self.service_name} is RUNNING")
            print(f"   PID: {pid}")
            print(f"   Web Interface: http://localhost:8000")
            print(f"   Status API: http://localhost:8000/api/status")
            
            # Test the API
            try:
                import requests
                response = requests.get("http://localhost:8000/api/status", timeout=5)
                if response.status_code == 200:
                    print("✓ Web interface is responding to requests")
                else:
                    print(f"⚠ Web interface returned status: {response.status_code}")
            except Exception:
                print("⚠ Could not connect to web interface")
                
        else:
            print(f"✗ {self.service_name} is NOT RUNNING")
    
    def is_running(self):
        """Check if service is running"""
        try:
            if not self.pid_file.exists():
                return False
            
            with open(self.pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process is actually running
            os.kill(pid, 0)  # This will raise an exception if process doesn't exist
            return True
            
        except (FileNotFoundError, ValueError, ProcessLookupError, OSError):
            # Clean up stale PID file
            if self.pid_file.exists():
                self.pid_file.unlink()
            return False
    
    def get_pid(self):
        """Get the PID of the running service"""
        try:
            with open(self.pid_file, 'r') as f:
                return int(f.read().strip())
        except:
            return None
    
    def logs(self, lines=50):
        """Show recent logs"""
        log_file = self.project_root / "logs" / "background_service.log"
        
        if not log_file.exists():
            print("No log file found")
            return
        
        try:
            result = subprocess.run(['tail', '-n', str(lines), str(log_file)], 
                                 capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"Could not display logs: {e}")

def main():
    if len(sys.argv) < 2:
        print("AI Automation Agent - Service Manager")
        print("Usage: python service_manager.py [start|stop|restart|status|logs|help]")
        print("")
        print("Commands:")
        print("  start   - Start the service in background")
        print("  stop    - Stop the running service")
        print("  restart - Restart the service")
        print("  status  - Check if service is running")
        print("  logs    - Show recent logs")
        print("  help    - Show this help message")
        return 1
    
    command = sys.argv[1].lower()
    manager = ServiceManager()
    
    if command == "start":
        manager.start()
    elif command == "stop":
        manager.stop()
    elif command == "restart":
        manager.restart()
    elif command == "status":
        manager.status()
    elif command == "logs":
        lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        manager.logs(lines)
    elif command == "help":
        print("AI Automation Agent - Service Manager")
        print("")
        print("Manages the web interface as a background service.")
        print("")
        print("Features:")
        print("- Runs independently of terminal sessions")
        print("- Automatic restart if service crashes")
        print("- Health monitoring and logging")
        print("- PID management for proper shutdown")
        print("")
        print("Usage:")
        print("  python service_manager.py start   # Start in background")
        print("  python service_manager.py status  # Check if running")
        print("  python service_manager.py stop    # Stop gracefully")
        print("  python service_manager.py restart # Restart service")
        print("  python service_manager.py logs    # View recent logs")
    else:
        print(f"Unknown command: {command}")
        print("Use 'help' for usage information")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())