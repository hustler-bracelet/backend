import os
import dramatiq
import config

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

from dotenv import load_dotenv

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


POSTGRES_URI = f'postgresql+asyncpg://{config.DB_USER}:{config.DB_PASS}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}'
REDIS_URI = f'redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}'
BOT_TOKEN: str = config.BOT_TOKEN

load_dotenv()


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))

engine = create_async_engine(POSTGRES_URI)
SessionMaker = sessionmaker(engine, autoflush=False, class_=AsyncSession, expire_on_commit=False)


redis_broker = RedisBroker(url=REDIS_URI)
redis_broker.add_middleware(AsyncIO())

dramatiq.set_broker(redis_broker)
