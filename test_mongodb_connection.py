#!/usr/bin/env python3
"""
Test script to verify MongoDB connection and basic functionality
Run this on your VPS to ensure MongoDB is working properly
"""

import sys
import os
from datetime import datetime

# Add the AI_Automation_Agent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AI_Automation_Agent'))

try:
    from config.settings import settings
    from config.database import init_database, db_manager, get_collection
    from loguru import logger
    
    print("=" * 60)
    print("🧪 MONGODB CONNECTION TEST")
    print("=" * 60)
    
    print(f"\n📋 Configuration:")
    print(f"   Database Type: {settings.DATABASE_TYPE}")
    print(f"   MongoDB URI: {settings.MONGODB_URI}")
    
    # Test database initialization
    print(f"\n🔌 Testing database connection...")
    success = init_database()
    
    if success:
        print(f"   ✅ Database connected successfully!")
        
        # Test collection access
        print(f"\n📦 Testing collection access...")
        try:
            collection = get_collection("test_collection")
            
            # Insert test document
            test_doc = {
                "test": "MongoDB connection test",
                "timestamp": datetime.now(),
                "status": "success"
            }
            
            result = collection.insert_one(test_doc)
            print(f"   ✅ Document inserted with ID: {result.inserted_id}")
            
            # Retrieve document
            retrieved_doc = collection.find_one({"_id": result.inserted_id})
            if retrieved_doc:
                print(f"   ✅ Document retrieved successfully")
                print(f"   📄 Retrieved data: {retrieved_doc.get('test', 'N/A')}")
            
            # Clean up test document
            collection.delete_one({"_id": result.inserted_id})
            print(f"   ✅ Test document cleaned up")
            
            print(f"\n🎉 All MongoDB tests passed!")
            print(f"   Your MongoDB setup is working correctly.")
            
        except Exception as e:
            print(f"   ❌ Collection access failed: {e}")
            sys.exit(1)
            
    else:
        print(f"   ❌ Database connection failed!")
        print(f"   Please check:")
        print(f"   1. MongoDB is installed: sudo apt install mongodb")
        print(f"   2. MongoDB service is running: sudo systemctl start mongodb")
        print(f"   3. MongoDB is accessible: mongosh")
        sys.exit(1)
    
    print(f"\n📝 Next Steps:")
    print(f"   1. Run: python service_manager.py start")
    print(f"   2. Open browser to: http://YOUR_VPS_IP:8000")
    print(f"   3. Close terminal and verify service continues running")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"   Please ensure all dependencies are installed:")
    print(f"   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)

print("=" * 60)