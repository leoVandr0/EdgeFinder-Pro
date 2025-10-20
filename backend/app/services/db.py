from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
import os
from datetime import datetime

# MongoDB setup
mongo_client = None
mongo_db = None

# PostgreSQL setup
Base = declarative_base()

class InsightDB(Base):
    """PostgreSQL table for insights"""
    __tablename__ = "insights"

    id = Column(Integer, primary_key=True, index=True)
    pair = Column(String(10), index=True)
    signal_type = Column(String(10))
    confidence = Column(Float)
    entry_price = Column(Float)
    stop_loss = Column(Float)
    take_profit = Column(Float)
    reasoning = Column(String(500))
    timeframe = Column(String(5))
    created_at = Column(DateTime, default=datetime.utcnow)

class StrengthDB(Base):
    """PostgreSQL table for currency strengths"""
    __tablename__ = "strengths"

    id = Column(Integer, primary_key=True, index=True)
    currency = Column(String(3), unique=True, index=True)
    strength_score = Column(Float)
    momentum = Column(Float)
    trend = Column(String(10))
    rank = Column(Integer)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Database connection functions
async def connect_mongodb():
    """Connect to MongoDB"""
    global mongo_client, mongo_db
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        print("Warning: MONGODB_URI not set, using in-memory fallback")
        return None

    mongo_client = AsyncIOMotorClient(mongodb_uri)
    mongo_db = mongo_client.edgefinder
    print("Connected to MongoDB")
    return mongo_db

async def close_mongodb():
    """Close MongoDB connection"""
    global mongo_client
    if mongo_client:
        mongo_client.close()

def get_postgres_engine():
    """Get PostgreSQL async engine"""
    postgres_url = os.getenv("POSTGRES_URL", "").replace("postgresql://", "postgresql+asyncpg://")
    if not postgres_url:
        print("Warning: POSTGRES_URL not set, using SQLite fallback")
        postgres_url = "sqlite+aiosqlite:///./edgefinder.db"

    return create_async_engine(postgres_url, echo=False)

async def init_postgres():
    """Initialize PostgreSQL tables"""
    engine = get_postgres_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("PostgreSQL tables initialized")
    return engine

def get_session_maker(engine):
    """Get async session maker"""
    return sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

# In-memory fallback for events if MongoDB not available
_fallback_events = []

def get_fallback_events():
    """Get fallback events storage"""
    return _fallback_events
