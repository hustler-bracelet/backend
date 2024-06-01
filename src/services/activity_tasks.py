
from src.database.models import ActivityTask, Niche
from src.repos import Repository

from src.api.schemas.activities import ActivityTaskData

from .base import BaseDatabaseService


class ActivityTasksService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(ActivityTask, self._session)

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
