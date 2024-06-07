
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime

from src.database.models import ActivityTaskCompletion, ActivityTask

from .generic import Repository


class ActivityTasksCompletionRepository(Repository):
    def __init__(self, session):
        super().__init__(ActivityTaskCompletion, session)

    async def get_tasks_completed_by_activity(self, activity_id: int) -> list[ActivityTaskCompletion]:
        """Get all tasks completed for an activity"""
        query = (
            select(ActivityTaskCompletion)
            .join(ActivityTaskCompletion.activity_task.and_(ActivityTask.activity_id == activity_id))
            .where(ActivityTaskCompletion.checked_on.isnot(None))
            .options(selectinload(ActivityTaskCompletion.user))
            .order_by(ActivityTaskCompletion.checked_on.desc())
        )

        return (await self._session.execute(query)).scalars().all()
