"""Database connection management."""

import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.logging import get_logger
from pymongo.server_api import ServerApi


from app.core.config import settings
logger = get_logger(__name__)


# MongoDB client (will be initialized in lifespan)
mongo_client: AsyncIOMotorClient | None = None

async def connect_to_mongo():
    global db_client, db   
    
    print(f"📊 Connecting to MongoDB with:")
    print(f"  - DB Name: {settings.DB_NAME}")
    
    # MongoDB connection string
    connection_string = settings.mongodb_url
    
    try:
        db_client = AsyncIOMotorClient(connection_string, server_api=ServerApi('1'))
        db = db_client[settings.DB_NAME]
        
        # Test connection
        await db_client.admin.command('ping')
        print(f"✅ Successfully connected to MongoDB database: {settings.DB_NAME}")
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        raise
    
async def close_mongo_connection():
    global db_client
    if db_client:
        db_client.close()
        print("MongoDB connection closed")

def get_database() -> AsyncIOMotorDatabase:
    if db_client is None:
        raise RuntimeError("Database not initialized")
    return db_client[settings.DB_NAME]
