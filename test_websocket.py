#!/usr/bin/env python3
"""
WebSocket Test and Debug Tool
"""
import asyncio
import websockets
import json
import sys
import time

async def test_websocket():
    """Test WebSocket connection"""
    uri = "ws://localhost:8000/ws"
    
    print(f"🔌 Testing WebSocket connection to: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket connection established!")
            
            # Test connection by sending a message
            test_message = {
                "type": "ping",
                "data": {"timestamp": time.time()}
            }
            await websocket.send(json.dumps(test_message))
            print("📤 Sent ping message")
            
            # Listen for response
            try:
                response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                print(f"📥 Received response: {response}")
                
                # Parse response
                try:
                    data = json.loads(response)
                    print(f"📊 Parsed data: {json.dumps(data, indent=2)}")
                except json.JSONDecodeError:
                    print(f"❌ Could not parse response as JSON: {response}")
                    
            except asyncio.TimeoutError:
                print("⏰ No response received within 5 seconds")
            
            # Keep connection alive for testing
            print("🔄 Keeping connection alive for 10 seconds...")
            await asyncio.sleep(10)
            
    except ConnectionRefusedError:
        print("❌ Connection refused - server might not be running")
        return False
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        return False
    
    return True

def test_api_endpoints():
    """Test REST API endpoints"""
    import requests
    
    base_url = "http://localhost:8000"
    endpoints = [
        "/",
        "/api/health", 
        "/api/status",
        "/api/blog/posts",
        "/api/analytics/summary"
    ]
    
    print("🌐 Testing REST API endpoints...")
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint}: {response.status_code}")
            
            if endpoint == "/api/health":
                try:
                    health_data = response.json()
                    print(f"   Health Status: {health_data.get('status', 'unknown')}")
                    if 'checks' in health_data:
                        for check_name, check_data in health_data['checks'].items():
                            status = check_data.get('status', 'unknown')
                            print(f"   {check_name}: {status}")
                except:
                    print(f"   Response: {response.text[:100]}...")
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: Connection error - {e}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

async def main():
    """Main test function"""
    print("🧪 WebSocket and API Testing Tool")
    print("=" * 40)
    
    # Test REST API first
    print("\n1️⃣ Testing REST API...")
    test_api_endpoints()
    
    # Test WebSocket
    print("\n2️⃣ Testing WebSocket...")
    ws_success = await test_websocket()
    
    print("\n" + "=" * 40)
    if ws_success:
        print("🎉 WebSocket test completed successfully!")
        print("💡 If frontend still has issues, check browser console for specific errors")
    else:
        print("❌ WebSocket test failed!")
        print("💡 Check server logs for WebSocket implementation issues")
    
    print("\n📋 Next Steps:")
    print("1. If API works but WebSocket fails, WebSocket implementation needs fixing")
    print("2. If both work, frontend JavaScript might have loading issues")
    print("3. Check browser developer tools console for specific error messages")

if __name__ == "__main__":
    asyncio.run(main())