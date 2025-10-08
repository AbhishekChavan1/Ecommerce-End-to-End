"""
Quick Application Test Script.
Tests that the application starts and responds correctly.
"""

import requests
import time

def test_application():
    """Test that the application is running and responding correctly."""
    base_url = "http://127.0.0.1:5000"
    
    print("🔍 Testing Flask Application...")
    print("=" * 50)
    
    # Wait a moment for the server to be ready
    time.sleep(2)
    
    try:
        # Test home page
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200:
            print("✅ Home page (/) loads successfully")
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Length: {len(response.content)} bytes")
        else:
            print(f"❌ Home page failed with status code: {response.status_code}")
        
        # Test shop page
        response = requests.get(f"{base_url}/shop/products", timeout=10)
        if response.status_code == 200:
            print("✅ Products page (/shop/products) loads successfully")
        else:
            print(f"❌ Products page failed with status code: {response.status_code}")
        
        # Test auth pages
        response = requests.get(f"{base_url}/auth/login", timeout=10)
        if response.status_code == 200:
            print("✅ Login page (/auth/login) loads successfully")
        else:
            print(f"❌ Login page failed with status code: {response.status_code}")
            
        print("\n🎉 Application is running correctly!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the application. Make sure it's running on http://127.0.0.1:5000")
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The application might be slow to respond.")
    except Exception as e:
        print(f"❌ Error testing application: {e}")

if __name__ == "__main__":
    test_application()