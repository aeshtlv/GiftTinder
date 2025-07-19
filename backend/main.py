from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import json

from database import get_db, create_tables
from models import User, Gift, Swipe, Match
from utils import validate_telegram_webapp_data, extract_user_from_init_data, format_gift_data, format_match_data
from config import APP_NAME, APP_VERSION

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Gift Tinder API - Telegram Mini App Backend"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.get("/")
async def root():
    return {"message": "Gift Tinder API", "version": APP_VERSION}

@app.get("/api/user/{telegram_id}")
async def get_user(telegram_id: int, db: Session = Depends(get_db)):
    """Get user by Telegram ID"""
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_at": user.created_at,
        "is_active": user.is_active
    }

@app.post("/api/user")
async def create_user(request: Request, db: Session = Depends(get_db)):
    """Create or update user"""
    # Validate Telegram WebApp data
    init_data = request.headers.get("X-Telegram-Init-Data", "")
    if not validate_telegram_webapp_data(init_data):
        raise HTTPException(status_code=401, detail="Invalid Telegram data")
    
    # Extract user data
    user_data = extract_user_from_init_data(init_data)
    if not user_data:
        raise HTTPException(status_code=400, detail="Invalid user data")
    
    telegram_id = user_data.get("id")
    if not telegram_id:
        raise HTTPException(status_code=400, detail="Missing user ID")
    
    # Check if user exists
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if user:
        # Update existing user
        user.username = user_data.get("username")
        user.first_name = user_data.get("first_name")
        user.last_name = user_data.get("last_name")
    else:
        # Create new user
        user = User(
            telegram_id=telegram_id,
            username=user_data.get("username"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name")
        )
        db.add(user)
    
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "created_at": user.created_at,
        "is_active": user.is_active
    }

@app.get("/api/gifts/{telegram_id}")
async def get_user_gifts(telegram_id: int, db: Session = Depends(get_db)):
    """Get all gifts for a user"""
    gifts = db.query(Gift).filter(
        Gift.telegram_id == telegram_id,
        Gift.is_visible == True
    ).all()
    
    return [format_gift_data(gift.__dict__) for gift in gifts]

@app.post("/api/sync_gifts/{telegram_id}")
async def sync_gifts(telegram_id: int, gifts_data: List[dict], db: Session = Depends(get_db)):
    """Sync gifts for a user (called by userbot)"""
    # Clear existing gifts for this user
    db.query(Gift).filter(Gift.telegram_id == telegram_id).delete()
    
    # Add new gifts
    for gift_data in gifts_data:
        gift = Gift(
            telegram_id=telegram_id,
            gift_id=gift_data.get("id"),
            gift_name=gift_data.get("name", "Unknown Gift"),
            gift_description=gift_data.get("description", ""),
            gift_image_url=gift_data.get("image_url", "")
        )
        db.add(gift)
    
    db.commit()
    return {"message": f"Synced {len(gifts_data)} gifts"}

@app.get("/api/next_gift/{telegram_id}")
async def get_next_gift(telegram_id: int, db: Session = Depends(get_db)):
    """Get next gift to swipe for a user"""
    # Get gifts that user hasn't swiped on yet
    swiped_gift_ids = db.query(Swipe.gift_id).filter(Swipe.user_id == telegram_id).subquery()
    
    next_gift = db.query(Gift).filter(
        Gift.telegram_id != telegram_id,  # Not user's own gifts
        Gift.is_visible == True,
        ~Gift.id.in_(swiped_gift_ids)
    ).first()
    
    if not next_gift:
        return {"message": "No more gifts to swipe"}
    
    return format_gift_data(next_gift.__dict__)

@app.post("/api/swipe")
async def swipe_gift(telegram_id: int, gift_id: int, is_like: bool, db: Session = Depends(get_db)):
    """Record a swipe (like/dislike)"""
    # Check if user exists
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if gift exists
    gift = db.query(Gift).filter(Gift.id == gift_id).first()
    if not gift:
        raise HTTPException(status_code=404, detail="Gift not found")
    
    # Check if already swiped
    existing_swipe = db.query(Swipe).filter(
        Swipe.user_id == telegram_id,
        Swipe.gift_id == gift_id
    ).first()
    
    if existing_swipe:
        raise HTTPException(status_code=400, detail="Already swiped on this gift")
    
    # Create swipe
    swipe = Swipe(
        user_id=telegram_id,
        gift_id=gift_id,
        is_like=is_like
    )
    db.add(swipe)
    
    # Check for match if it's a like
    if is_like:
        # Check if the gift owner also liked this user's gift
        gift_owner_swipe = db.query(Swipe).filter(
            Swipe.user_id == gift.telegram_id,
            Swipe.gift_id.in_(
                db.query(Gift.id).filter(Gift.telegram_id == telegram_id)
            ),
            Swipe.is_like == True
        ).first()
        
        if gift_owner_swipe:
            # Create match
            match = Match(
                user1_id=telegram_id,
                user2_id=gift.telegram_id
            )
            db.add(match)
    
    db.commit()
    
    return {"message": "Swipe recorded", "is_like": is_like}

@app.get("/api/matches/{telegram_id}")
async def get_matches(telegram_id: int, db: Session = Depends(get_db)):
    """Get all matches for a user"""
    matches = db.query(Match).filter(
        (Match.user1_id == telegram_id) | (Match.user2_id == telegram_id),
        Match.is_active == True
    ).all()
    
    result = []
    for match in matches:
        # Get the other user's info
        other_user_id = match.user2_id if match.user1_id == telegram_id else match.user1_id
        other_user = db.query(User).filter(User.telegram_id == other_user_id).first()
        
        if other_user:
            result.append({
                "match_id": match.id,
                "other_user": {
                    "telegram_id": other_user.telegram_id,
                    "username": other_user.username,
                    "first_name": other_user.first_name,
                    "last_name": other_user.last_name
                },
                "created_at": match.created_at
            })
    
    return result 