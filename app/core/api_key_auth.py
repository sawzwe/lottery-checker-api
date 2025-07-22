from fastapi import Header, HTTPException
from supabase import Client
from .database import get_supabase_client


def validate_api_key(x_api_key: str = Header(...)) -> str:
    """
    Validate x-api-key live from Supabase on every request.

    Returns:
        client_name (str) if key is valid and active.

    Raises HTTPException 401 if invalid or inactive.
    """
    client: Client = get_supabase_client()

    # Query Supabase for the exact key
    response = client.table("api_keys").select("api_key, client_name, active") \
        .eq("api_key", x_api_key).limit(1).execute()

    if not response.data or len(response.data) == 0:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    api_key_record = response.data[0]

    if not api_key_record.get("active", False):
        raise HTTPException(
            status_code=403, detail="You don't have access to the api")

    return api_key_record["client_name"]
