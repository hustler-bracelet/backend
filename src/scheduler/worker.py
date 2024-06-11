import config

from pytz import timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.asyncio import AsyncIOExecutor


DEFAULT_REDIS_SCHEDULER_DB = 1


jobstores = {
    'default': RedisJobStore(
        db=DEFAULT_REDIS_SCHEDULER_DB,
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        password=config.REDIS_PASSWORD,
    )
}

executors = {
    'default': AsyncIOExecutor(),
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = AsyncIOScheduler()

scheduler.configure(
    jobstores=jobstores, 
    executors=executors, 
    job_defaults=job_defaults, 
    timezone=timezone('Europe/Moscow')
)
