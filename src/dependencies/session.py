
from src.database.engine import SessionMaker


async def get_session():
    """Get session for working with database"""
    async with SessionMaker() as session:
        yield session
