import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings

logger = logging.getLogger(__name__)

class MongoDB:
    """
    Manages MongoDB connection and provides access to the database client.
    """
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None

    async def connect(self):
        """
        Establishes connection to MongoDB.
        """
        if self.client is not None:
            logger.warning("MongoDB client already connected. Skipping connection.")
            return

        try:
            self.client = AsyncIOMotorClient(
                settings.mongodb_url,
                maxPoolSize=settings.mongodb_max_pool_size,
                minPoolSize=settings.mongodb_min_pool_size,
            )
            self.database = self.client[settings.DB_NAME]
            await self.database.command("ping")  # Test connection
            logger.info("MongoDB connected successfully.")
        except Exception as e:
            logger.error(f"Could not connect to MongoDB: {e}")
            self.client = None
            self.database = None
            raise

    async def close(self):
        """
        Closes MongoDB connection.
        """
        if self.client:
            self.client.close()
            self.client = None
            self.database = None
            logger.info("MongoDB connection closed.")
        else:
            logger.warning("MongoDB client not connected. Skipping close.")

# Global instance
db = MongoDB()

async def get_database() -> AsyncIOMotorDatabase:
    """
    Dependency to get MongoDB database instance.
    """
    if db.database is None:
        raise ConnectionError("MongoDB database not initialized. Call connect() first.")
    return db.database
