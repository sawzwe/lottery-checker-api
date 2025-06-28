#!/usr/bin/env python3
"""
Setup verification script to test your Supabase configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_variables():
    """Test if all required environment variables are present"""
    
    print("🔍 Checking your environment variables...")
    print("="*50)
    
    # Check your existing variables
    api_service_role = os.getenv("API_SERVICE_ROLE_SUPERBASE")
    api_jwt_key = os.getenv("API_JWT_KEY")
    api_keys = os.getenv("API_KEYS_SUPERBASE")
    openai_key = os.getenv("OPEN_AI_KEY")
    db_password = os.getenv("DB_PASSWORD")
    superbase_url = os.getenv("SUPERBASE_PROJECT_URL")
    supabase_url = os.getenv("SUPABASE_URL")
    
    print(f"API_SERVICE_ROLE_SUPERBASE: {'✓ Found' if api_service_role else '✗ Not found'}")
    print(f"API_JWT_KEY: {'✓ Found' if api_jwt_key else '✗ Not found'}")
    print(f"API_KEYS_SUPERBASE: {'✓ Found' if api_keys else '✗ Not found'}")
    print(f"OPEN_AI_KEY: {'✓ Found' if openai_key else '✗ Not found'}")
    print(f"DB_PASSWORD: {'✓ Found' if db_password else '✗ Not found'}")
    print(f"SUPERBASE_PROJECT_URL: {'✓ Found' if superbase_url else '✗ Not found'}")
    print(f"SUPABASE_URL: {'✓ Found' if supabase_url else '✗ Not found'}")
    
    print("\n📋 For lottery uploader, you need:")
    
    # Check API keys
    has_api_key = api_service_role or api_jwt_key or api_keys
    print(f"- {'✓' if has_api_key else '✗'} API Key (Service Role, JWT, or regular)")
    
    # Check URL
    has_url = superbase_url or supabase_url
    print(f"- {'✓' if has_url else '✗'} Project URL")
    
    if not has_url:
        print("\n⚠️  No Supabase URL found!")
        if not superbase_url:
            print("SUPERBASE_PROJECT_URL is preferred (you already have this variable name)")
        print("\nTo find your URL:")
        print("1. Go to your Supabase dashboard")
        print("2. Select your project")
        print("3. Go to Settings → API")
        print("4. Copy the 'Project URL'")
        return False
    
    if not has_api_key:
        print("\n⚠️  No API keys found!")
        print("You need at least one of:")
        print("- API_SERVICE_ROLE_SUPERBASE (best for data operations)")
        print("- API_JWT_KEY")
        print("- API_KEYS_SUPERBASE")
        return False
    
    return True

def test_supabase_connection():
    """Test connection to Supabase"""
    try:
        from config.config import get_supabase_config
        from supabase import create_client
        
        print("\n🔗 Testing Supabase connection...")
        
        url, key = get_supabase_config()
        try:
            supabase = create_client(url, key)
        except TypeError as e:
            if "proxy" in str(e):
                print("⚠️  Detected version compatibility issue, trying basic client...")
                # Fallback to basic client creation
                supabase = create_client(url, key)
            else:
                raise
        
        # Try a simple query to test connection
        try:
            result = supabase.table('lottery_draws').select('count').execute()
            print("✓ Successfully connected to Supabase!")
            print("✓ Table 'lottery_draws' exists and is accessible")
        except Exception as e:
            if "relation \"lottery_draws\" does not exist" in str(e):
                print("✓ Successfully connected to Supabase!")
                print("⚠️  Table 'lottery_draws' doesn't exist yet - you'll need to create it")
                print("  Run the SQL from the README in your Supabase SQL editor")
            else:
                print(f"✗ Connection successful but query failed: {e}")
        
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

def main():
    print("🎲 Lottery Uploader - Setup Verification")
    print("="*50)
    
    # Test environment variables
    env_ok = test_environment_variables()
    
    if env_ok:
        # Test Supabase connection
        conn_ok = test_supabase_connection()
        
        if conn_ok:
            print("\n🎉 Setup looks good! You can now run:")
            print("python upload_lottery_data.py sample_lottery_data.csv")
        else:
            print("\n❌ Setup issues found. Please check your configuration.")
    else:
        print("\n❌ Missing required environment variables.")

if __name__ == "__main__":
    main() 