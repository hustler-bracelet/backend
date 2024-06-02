
import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

postgres_uri = f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'

engine = create_async_engine(postgres_uri, pool_pre_ping=True)
SessionMaker = sessionmaker(engine, autoflush=False, class_=AsyncSession, expire_on_commit=False)
