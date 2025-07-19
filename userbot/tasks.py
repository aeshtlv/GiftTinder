import asyncio
import aiohttp
import logging
from typing import List, Dict, Any
from pyrogram import Client
from config import WEBAPP_URL

logger = logging.getLogger(__name__)

async def get_user_gifts(client: Client, user_id: int) -> List[Dict[str, Any]]:
    """
    Get gifts for a specific user using Pyrogram
    """
    try:
        # Get user's gifts using Pyrogram
        gifts = await client.get_gifts(user_id)
        
        formatted_gifts = []
        for gift in gifts:
            formatted_gift = {
                "id": str(gift.id),
                "name": getattr(gift, 'name', 'Unknown Gift'),
                "description": getattr(gift, 'description', ''),
                "image_url": getattr(gift, 'image_url', ''),
                "user_id": user_id
            }
            formatted_gifts.append(formatted_gift)
        
        return formatted_gifts
        
    except Exception as e:
        logger.error(f"Error getting gifts for user {user_id}: {e}")
        return []

async def sync_gifts_to_backend(telegram_id: int, gifts: List[Dict[str, Any]]) -> bool:
    """
    Sync gifts to backend API
    """
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{WEBAPP_URL}/api/sync_gifts/{telegram_id}"
            async with session.post(url, json=gifts) as response:
                if response.status == 200:
                    logger.info(f"Synced {len(gifts)} gifts for user {telegram_id}")
                    return True
                else:
                    logger.error(f"Failed to sync gifts for user {telegram_id}: {response.status}")
                    return False
    except Exception as e:
        logger.error(f"Error syncing gifts to backend: {e}")
        return False

async def sync_gifts_task(client: Client):
    """
    Main task to sync gifts for all users
    """
    logger.info("Starting gift sync task...")
    
    while True:
        try:
            # Get all users from backend
            async with aiohttp.ClientSession() as session:
                url = f"{WEBAPP_URL}/api/users"
                async with session.get(url) as response:
                    if response.status == 200:
                        users = await response.json()
                        
                        for user in users:
                            telegram_id = user.get("telegram_id")
                            if telegram_id:
                                # Get gifts for this user
                                gifts = await get_user_gifts(client, telegram_id)
                                
                                if gifts:
                                    # Sync to backend
                                    await sync_gifts_to_backend(telegram_id, gifts)
                                
                                # Small delay between users
                                await asyncio.sleep(1)
                    
            # Wait before next sync cycle (every 6 hours)
            logger.info("Gift sync completed. Waiting 6 hours before next sync...")
            await asyncio.sleep(6 * 60 * 60)  # 6 hours
            
        except Exception as e:
            logger.error(f"Error in gift sync task: {e}")
            await asyncio.sleep(60)  # Wait 1 minute before retry

async def sync_single_user_gifts(client: Client, telegram_id: int):
    """
    Sync gifts for a single user (can be called manually)
    """
    logger.info(f"Syncing gifts for user {telegram_id}...")
    
    gifts = await get_user_gifts(client, telegram_id)
    if gifts:
        success = await sync_gifts_to_backend(telegram_id, gifts)
        if success:
            logger.info(f"Successfully synced {len(gifts)} gifts for user {telegram_id}")
        else:
            logger.error(f"Failed to sync gifts for user {telegram_id}")
    else:
        logger.info(f"No gifts found for user {telegram_id}") 