import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token_here")
BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")

# Telegram API Configuration
API_ID = int(os.getenv("API_ID", "1234567"))
API_HASH = os.getenv("API_HASH", "your_api_hash_here")

# Database Configuration
DB_URL = os.getenv("DB_URL", "sqlite:///./gift_tinder.db")

# App Configuration
APP_NAME = "Gift Tinder"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.com")

# Limits
MAX_GIFTS_PER_USER = 50
MAX_SWIPES_PER_DAY = 100 