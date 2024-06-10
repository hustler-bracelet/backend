
from src.database.models import ActivityTask, Niche, Activity, User, ActivityTaskUserEvent, TaskCompletionProof
from src.repos.activity_tasks import ActivityTasksRepository, ActivityTasksEventsRepository
from src.repos import Repository

from src.api.schemas.activities import ActivityTaskData, ActivityTaskStatus

from .base import BaseDatabaseService


class ActivityTasksService(BaseDatabaseService):
    def post_init(self):
        self._repo = ActivityTasksRepository(self._session)
        self._events_repo = ActivityTasksEventsRepository(self._session)
        self._proofs_repo = Repository(TaskCompletionProof, self._session)

    async def create_new(self, activity_task: ActivityTaskData, niche: Niche, activity_id: int) -> ActivityTask:
        """
        Create new activity task

        :param activity_task: activity task data
        :return: created activity task
        """

        model = ActivityTask(
            **activity_task.model_dump(),
            niche_id=niche.id,
            activity_id=activity_id,
        )

        return await self._repo.create(model)

    async def get_current(self, niche_id: str) -> ActivityTask | None:
        """Получить текущую задачу активности для ниши"""
        return await self._repo.get_current_by_niche(niche_id)

    async def get_status(self, task_id: int, telegram_id: int) -> ActivityTaskStatus:
        """Получить статус выполнения задачи"""

        proofs = await self._proofs_repo.filter_by(telegram_id=telegram_id, activity_task_id=task_id)

        if proofs:
            return ActivityTaskStatus(
                can_do_task=False,
                already_done=True,
            )

        leaves = await self._events_repo.is_user_cancel_task(telegram_id, task_id)

        if leaves:
            return ActivityTaskStatus(
                can_do_task=False,
                already_done=False,
            )

        return ActivityTaskStatus(
            can_do_task=True,
            already_done=False,
        )
