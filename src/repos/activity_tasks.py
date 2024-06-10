
from sqlalchemy import select
from datetime import datetime

from src.database.models import ActivityTask, ActivityTaskUserEvent
from src.enums import ActivityTaskUserEventType

from .generic import Repository


class ActivityTasksRepository(Repository):
    def __init__(self, session):
        super().__init__(ActivityTask, session)

    async def get_current_by_niche(self, niche_id: int) -> ActivityTask | None:
        query = (
            select(ActivityTask)
            .where(
                ActivityTask.niche_id == niche_id,
                ActivityTask.deadline >= datetime.utcnow(),
            )
            .order_by(ActivityTask.deadline.desc())
        )

        return (await self._session.execute(query)).scalars().first()


class ActivityTasksEventsRepository(Repository):
    def __init__(self, session):
        super().__init__(ActivityTaskUserEvent, session)

    async def is_user_cancel_task(self, user_id: int, task_id: int) -> list[ActivityTaskUserEvent]:
        return (await self._session.execute(
            select(ActivityTaskUserEvent).where(
                ActivityTaskUserEvent.user_id == user_id,
                ActivityTaskUserEvent.type == ActivityTaskUserEventType.LEAVE,
                ActivityTaskUserEvent.task_id == task_id,
            )
        )).scalars().all()
