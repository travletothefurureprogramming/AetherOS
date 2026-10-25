import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pathlib import Path
import secrets
import json 

CONFIG_PATH = Path("cfg/api_key.json")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_or_create_api_key() -> str:
    if env_key := os.getenv("AETHEROS_API_KEY"):
        return env_key

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("api_key")
        except Exception:
            pass

    new_key =  f"aether_{secrets.token_hex(16)}"
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump({"api_key": new_key}, f, indent=4)

    print(f"[AetherOS Security] Generated new API Key: {new_key}")

    return new_key

MASTER_API_KEY = get_or_create_api_key

async def verify_api_key(api_key: str = Security(api_key_header)):

    if api_key == MASTER_API_KEY:
        return api_key
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Unauthorized access: Invalid or missing API Key"
    )