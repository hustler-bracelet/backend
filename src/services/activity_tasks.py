
from src.database.models import ActivityTask, Niche
from src.repos.activity_tasks import ActivityTasksRepository

from src.api.schemas.activities import ActivityTaskData

from .base import BaseDatabaseService


class ActivityTasksService(BaseDatabaseService):
    def post_init(self):
        self._repo = ActivityTasksRepository(self._session)

    async def create_new(self, activity_task: ActivityTaskData, niche: Niche) -> ActivityTask:
        """
        Create new activity task

        :param activity_task: activity task data
        :return: created activity task
        """

        model = ActivityTask(
            **activity_task.model_dump(),
            niche_id=niche.id,
        )

        return await self._repo.create(model)

    async def get_current(self, niche_id: str) -> ActivityTask | None:
        """Получить текущую задачу активности для ниши"""
        return await self._repo.get_current_by_niche(niche_id)
