from supabase import create_client, Client
from config.config import get_supabase_config

_supabase_client: Client = None

def get_supabase_client() -> Client:
    """Get Supabase client instance (singleton)"""
    global _supabase_client
    
    if _supabase_client is None:
        url, key = get_supabase_config()
        _supabase_client = create_client(url, key)
    
    return _supabase_client 