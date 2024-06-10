
from src.database.models import ActivityTask, Niche, Activity, User, ActivityTaskUserEvent, TaskCompletionProof
from src.repos.activity_tasks import ActivityTasksRepository, ActivityTasksEventsRepository
from src.repos import Repository

from src.api.schemas.activities import ActivityTaskData, ActivityTaskStatus
from src.enums import ActivityTaskUserEventType

from src.common.bot import BOT

from .base import BaseDatabaseService
from .notifications.activity_task import ActivityTaskNotificationService


class ActivityTasksService(BaseDatabaseService):
    def post_init(self):
        self._repo = ActivityTasksRepository(self._session)
        self._events_repo = ActivityTasksEventsRepository(self._session)
        self._proofs_repo = Repository(TaskCompletionProof, self._session)
        self._user_repo = Repository(User, self._session)

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

        result = await self._repo.create(model)

        # TODO: сделать задачей нотификацию для всех юзеров
        users = await self._user_repo.filter_by(selected_niche_id=niche.id)

        await ActivityTaskNotificationService(BOT).send_notification(result, users)

        return result

    async def get_current(
        self, 
        niche_id: str,
        user_id: str,
    ) -> ActivityTask | None:
        """Получить текущую задачу активности для ниши"""
        return await self._repo.get_current_by_niche(niche_id, user_id)

    async def get_status(self, task_id: int, telegram_id: int) -> ActivityTaskStatus:
        """Получить статус выполнения задачи"""

        proofs = await self._proofs_repo.filter_by(telegram_id=telegram_id, activity_task_id=task_id)

        if proofs.all():
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

    async def cancel_task(self, task_id: int, telegram_id: int):
        """Отменить выполнение задачи"""
        event = ActivityTaskUserEvent(
            telegram_id=telegram_id,
            activity_task_id=task_id,
            type=ActivityTaskUserEventType.LEAVE,
        )

        await self._events_repo.create(event)
