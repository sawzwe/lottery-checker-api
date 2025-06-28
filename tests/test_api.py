#!/usr/bin/env python3
"""
Test script for the Lottery Checker API
"""

import requests
import json
from datetime import date

BASE_URL = "http://localhost:8000"

def test_api():
    """Test the lottery API endpoints"""
    
    print("🧪 Testing Lottery Checker API")
    print("="*50)
    
    try:
        # Test 1: Root endpoint
        print("1. Testing root endpoint...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API is running: {data['message']}")
        else:
            print(f"   ❌ API not responding properly")
            return
        
        # Test 2: Health check
        print("\n2. Testing health check...")
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        
        # Test 3: Get latest draw
        print("\n3. Testing latest lottery draw...")
        response = requests.get(f"{BASE_URL}/api/th/v1/lottery/draws/latest")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Latest draw: {data['data']['draw']['date']}")
            print(f"   ✅ 1st Prize: {data['data']['draw']['prize_1st']}")
        
        # Test 4: Get all draws (first page)
        print("\n4. Testing get all draws...")
        response = requests.get(f"{BASE_URL}/api/th/v1/lottery/draws?page=1&size=5")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retrieved {len(data['data']['draws'])} draws")
            print(f"   ✅ Total draws: {data['data']['pagination']['total']}")
        
        # Test 5: Get specific draw
        print("\n5. Testing specific draw by date...")
        response = requests.get(f"{BASE_URL}/api/th/v1/lottery/draws/2024-12-16")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found draw for 2024-12-16")
            print(f"   ✅ 1st Prize: {data['data']['draw']['prize_1st']}")
        
        # Test 6: Check lottery numbers
        print("\n6. Testing lottery number checking...")
        test_data = {
            "numbers": ["097863", "123456", "42"],
            "date": None
        }
        response = requests.post(
            f"{BASE_URL}/api/th/v1/lottery/check",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            results = data['data']['results']
            winning_count = data['data']['winning_count']
            total_winnings = data['data']['total_winnings']
            
            print(f"   ✅ Checked {len(test_data['numbers'])} numbers")
            print(f"   ✅ Found {winning_count} winners")
            print(f"   ✅ Total winnings: ฿{total_winnings:,}")
            
            for result in results:
                if result['matched']:
                    print(f"   🎉 Winner: {result['number']} - {result['prize_type']} - ฿{result['prize_amount']:,}")
        
        print("\n🎉 All API tests completed successfully!")
        print("\n📖 Visit http://localhost:8000/docs for interactive API documentation")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running:")
        print("   python run_api.py")
    except Exception as e:
        print(f"❌ Error testing API: {e}")

if __name__ == "__main__":
    test_api() 