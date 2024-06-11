import dramatiq
import config

from dotenv import load_dotenv

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO


REDIS_URI = f'redis://:{config.REDIS_PASSWORD}@{config.REDIS_HOST}:{config.REDIS_PORT}'

load_dotenv()


redis_broker = RedisBroker(url=REDIS_URI)
redis_broker.add_middleware(AsyncIO())

dramatiq.set_broker(redis_broker)
