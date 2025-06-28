"""
Configuration for Lottery Uploader

If you can't create a .env file, you can modify this file directly with your credentials.
However, it's recommended to use environment variables for security.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_supabase_config():
    """Get Supabase configuration from environment variables or config file"""
    
    # Try to get URL from your environment variables
    supabase_url = os.getenv("SUPERBASE_PROJECT_URL") or os.getenv("SUPABASE_URL")
    
    # Use your existing API keys - try in order of preference
    supabase_key = (os.getenv("API_SERVICE_ROLE_SUPERBASE") or 
                   os.getenv("API_JWT_KEY") or 
                   os.getenv("API_KEYS_SUPERBASE"))
    
    # Fallback to direct configuration if environment variables not found
    if not supabase_url:
        supabase_url = "https://zfkszzzpkuniomghhmyo.supabase.co"
    
    if not supabase_key:
        supabase_key = "eyJhbGciOiI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJX0.hYEuRPsPR4YNyCOMHJZ_zlLi_Gd7y7Y20PLYVLeeeQo"
    
    # If URL not found, use direct config
    if not supabase_url:
        # Uncomment and set your Supabase project URL:
        # supabase_url = "https://your-project.supabase.co"
        pass
    
    # If no keys found, use direct config
    if not supabase_key:
        # Uncomment and use one of your keys directly:
        # supabase_key = "your-service-role-key-or-anon-key"
        pass
    
    if not supabase_url:
        raise ValueError(
            "Supabase URL not found. Your environment variables:\n"
            f"SUPERBASE_PROJECT_URL: {'Found' if os.getenv('SUPERBASE_PROJECT_URL') else 'Not found'}\n"
            f"SUPABASE_URL: {'Found' if os.getenv('SUPABASE_URL') else 'Not found'}\n"
            "Please check your environment variables are loaded correctly."
        )
    
    if not supabase_key:
        raise ValueError(
            "Supabase API key not found. Your environment variables:\n"
            f"API_SERVICE_ROLE_SUPERBASE: {'Found' if os.getenv('API_SERVICE_ROLE_SUPERBASE') else 'Not found'}\n"
            f"API_JWT_KEY: {'Found' if os.getenv('API_JWT_KEY') else 'Not found'}\n"
            f"API_KEYS_SUPERBASE: {'Found' if os.getenv('API_KEYS_SUPERBASE') else 'Not found'}\n"
            "Please check your environment variables are loaded correctly."
        )
    
    # Log which credentials are being used (without exposing the actual values)
    if os.getenv("SUPERBASE_PROJECT_URL"):
        print("✓ Using SUPERBASE_PROJECT_URL for project URL")
    else:
        print("✓ Using SUPABASE_URL for project URL")
    
    if os.getenv("API_SERVICE_ROLE_SUPERBASE"):
        print("✓ Using API_SERVICE_ROLE_SUPERBASE (recommended for data operations)")
    elif os.getenv("API_JWT_KEY"):
        print("✓ Using API_JWT_KEY")
    else:
        print("✓ Using API_KEYS_SUPERBASE")
    
    return supabase_url, supabase_key 