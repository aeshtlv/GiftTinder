from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    gifts = relationship("Gift", back_populates="user")
    swipes = relationship("Swipe", back_populates="user")
    matches = relationship("Match", back_populates="user1", foreign_keys="Match.user1_id")
    matches2 = relationship("Match", back_populates="user2", foreign_keys="Match.user2_id")

class Gift(Base):
    __tablename__ = "gifts"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, ForeignKey("users.telegram_id"))
    gift_id = Column(String, index=True)  # Telegram gift ID
    gift_name = Column(String)
    gift_description = Column(Text, nullable=True)
    gift_image_url = Column(String, nullable=True)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="gifts")
    swipes = relationship("Swipe", back_populates="gift")

class Swipe(Base):
    __tablename__ = "swipes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.telegram_id"))
    gift_id = Column(Integer, ForeignKey("gifts.id"))
    is_like = Column(Boolean)  # True for like, False for dislike
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="swipes")
    gift = relationship("Gift", back_populates="swipes")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    user1_id = Column(Integer, ForeignKey("users.telegram_id"))
    user2_id = Column(Integer, ForeignKey("users.telegram_id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user1 = relationship("User", back_populates="matches", foreign_keys=[user1_id])
    user2 = relationship("User", back_populates="matches2", foreign_keys=[user2_id]) 