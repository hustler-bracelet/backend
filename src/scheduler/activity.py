import logging

from datetime import datetime

from src.services.activities import ActivityEventsService
from src.database.engine import SessionMaker

from .worker import scheduler


logger = logging.getLogger(__name__)


def schedule_activity_deadline(activity_id: int, deadline: datetime):
    """Запланированно завершить активность по истечению дедлайна"""
    job = scheduler.add_job(
        _process_finish_activity,
        trigger='date',
        run_date=deadline,
        args=[activity_id],
    )

    logger.info(f'Scheduled activity deadline -- id={activity_id}, job_id={job.id}, job_name={job.name}')


async def _process_finish_activity(activity_id: int):
    async with SessionMaker() as session:
        await ActivityEventsService(session).stop_event(activity_id)
