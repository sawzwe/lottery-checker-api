# Configuration

This directory contains configuration files for the lottery checker application.

## Files

- `config.py` - Main configuration management
  - Database connection settings
  - Environment variable handling
  - Supabase client configuration

## Usage

```python
from config.config import get_supabase_config

url, key = get_supabase_config()
```

## Environment Variables Required

- `SUPERBASE_PROJECT_URL` or `SUPABASE_URL` - Your Supabase project URL
- `API_SERVICE_ROLE_SUPERBASE` - Service role key (preferred for backend)
- `API_JWT_KEY` - JWT key (alternative)
- `API_KEYS_SUPERBASE` - Regular API key (fallback) 