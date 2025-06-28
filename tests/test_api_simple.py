#!/usr/bin/env python3

import requests
import sys

def test_api():
    try:
        print("Testing API health endpoint...")
        response = requests.get('http://localhost:8000/health', timeout=5)
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Response: {response.text}")
        
        if response.status_code == 200:
            print("\n🎉 API is running successfully!")
            
            # Test the root endpoint too
            print("\nTesting root endpoint...")
            root_response = requests.get('http://localhost:8000/', timeout=5)
            print(f"✅ Root Status: {root_response.status_code}")
            print(f"✅ Root Response: {root_response.text}")
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: API is not running or not accessible on localhost:8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: API is not responding within 5 seconds")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 API Test Script")
    print("=" * 50)
    success = test_api()
    sys.exit(0 if success else 1) 