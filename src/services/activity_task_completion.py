
from src.database.models import Activity, User
from src.repos.activity_task_completion import ActivityTasksCompletionRepository

from .base import BaseDatabaseService


class ActivityTasksCompletionService(BaseDatabaseService):
    def post_init(self):
        self._repo = ActivityTasksCompletionRepository(self._session)

    async def hide_user_tasks(self, user: User, activity: Activity):
        """Hide all tasks completed by user"""
        await self._repo.hide_all_user_completed_tasks(user.telegram_id, activity_id=activity.id)
