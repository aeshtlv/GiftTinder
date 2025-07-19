import asyncio
import logging
from pyrogram import Client
from config import API_ID, API_HASH
from tasks import sync_gifts_task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Pyrogram client
app = Client(
    "gift_tinder_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    workdir="./userbot"
)

async def main():
    """Main function to run the userbot"""
    logger.info("Starting Gift Tinder Userbot...")
    
    async with app:
        logger.info("Userbot started successfully!")
        
        # Start the gift sync task
        await sync_gifts_task(app)
        
        # Keep the userbot running
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Userbot stopped by user")
    except Exception as e:
        logger.error(f"Userbot error: {e}") 