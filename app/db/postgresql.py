import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
import asyncpg


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("user-service")


# Convert synchronous postgres URL to async
DATABASE_URL_CGP = str(settings.DATABASE_URL)
DATABASE_URL = str(settings.DATABASE_URL)
if DATABASE_URL_CGP.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL_CGP.replace("postgresql://", "postgresql+asyncpg://", 1)

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)


# Create async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Create base class for declarative models
Base = declarative_base()


# Asyncpg connection pool
async def get_asyncpg_pool():
    print("Creating asyncpg pool..., DATABASE_URL_CGP=", DATABASE_URL_CGP)
    return await asyncpg.create_pool(dsn=DATABASE_URL_CGP)


async def initialize_db():
    """Initialize database with required tables."""
    async with engine.begin() as conn:
        # Create tables if they don't exist
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized")


async def close_db_connection():
    """Close database connection."""
    await engine.dispose()
    logger.info("Database connection closed")


# Dependency for getting a database session
async def get_db():
    """Dependency for getting an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


# Dependency for asyncpg pool
async def get_pool():
    pool = await get_asyncpg_pool()
    async with pool.acquire() as conn:
        yield conn
