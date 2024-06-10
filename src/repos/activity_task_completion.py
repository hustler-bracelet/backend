
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
            .where(
                ActivityTaskCompletion.is_hidden == False,
            )
            .options(selectinload(ActivityTaskCompletion.user))
        )

        return (await self._session.execute(query)).scalars().all()

    async def hide_all_user_completed_tasks(self, user_id: int, activity_id: int):
        """Hide all tasks completed by user"""
        query = (
            select(ActivityTaskCompletion)
            .where(
                ActivityTaskCompletion.telegram_id == user_id,
                ActivityTaskCompletion.activity_task_id == activity_id,
            )
        )

        tasks = (await self._session.execute(query)).scalars().all()

        for task in tasks:
            task.is_hidden = True
            await self._session.flush()

        await self._session.commit()
