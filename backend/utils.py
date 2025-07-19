import hashlib
import hmac
import json
from typing import Dict, Any, Optional
from config import SECRET_KEY

def validate_telegram_webapp_data(init_data: str) -> bool:
    """
    Validate Telegram WebApp initData
    """
    try:
        # Parse init_data
        data_dict = {}
        for item in init_data.split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                data_dict[key] = value
        
        # Check if hash exists
        if 'hash' not in data_dict:
            return False
        
        # Get hash and remove it from data
        data_hash = data_dict.pop('hash')
        
        # Sort data alphabetically
        data_check_string = '\n'.join([
            f"{k}={v}" for k, v in sorted(data_dict.items())
        ])
        
        # Create secret key
        secret_key = hmac.new(
            b"WebAppData",
            SECRET_KEY.encode(),
            hashlib.sha256
        ).digest()
        
        # Calculate hash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return calculated_hash == data_hash
        
    except Exception:
        return False

def extract_user_from_init_data(init_data: str) -> Optional[Dict[str, Any]]:
    """
    Extract user data from Telegram WebApp initData
    """
    try:
        data_dict = {}
        for item in init_data.split('&'):
            if '=' in item:
                key, value = item.split('=', 1)
                data_dict[key] = value
        
        if 'user' in data_dict:
            user_data = json.loads(data_dict['user'])
            return user_data
        
        return None
        
    except Exception:
        return None

def format_gift_data(gift: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format gift data for frontend
    """
    return {
        "id": gift.get("id"),
        "name": gift.get("gift_name", "Unknown Gift"),
        "description": gift.get("gift_description", ""),
        "image_url": gift.get("gift_image_url", ""),
        "user_id": gift.get("telegram_id"),
        "created_at": gift.get("created_at")
    }

def format_match_data(match: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format match data for frontend
    """
    return {
        "id": match.get("id"),
        "user1_id": match.get("user1_id"),
        "user2_id": match.get("user2_id"),
        "created_at": match.get("created_at"),
        "is_active": match.get("is_active", True)
    } 