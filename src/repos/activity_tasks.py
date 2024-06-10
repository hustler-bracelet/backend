from pytz import timezone

from sqlalchemy import select, or_
from datetime import datetime

from src.database.models import ActivityTask, ActivityTaskUserEvent, TaskCompletionProof, ActivityTaskCompletion
from src.enums import ActivityTaskUserEventType, TaskCompletionStatus

from .generic import Repository


class ActivityTasksRepository(Repository):
    def __init__(self, session):
        super().__init__(ActivityTask, session)

    async def get_current_by_niche(self, niche_id: int, user_id: int) -> ActivityTask | None:
        query = (
            select(ActivityTask)
            .where(
                ActivityTask.niche_id == niche_id,
                ActivityTask.deadline >= datetime.now().astimezone(timezone('Europe/Moscow')),

                # NOTE: проверяем что пользователю доступна задача
                ActivityTask.id.not_in(
                    select(ActivityTaskUserEvent.activity_task_id)
                    .where(
                        ActivityTaskUserEvent.telegram_id == user_id, 
                        ActivityTaskUserEvent.type == ActivityTaskUserEventType.LEAVE,
                    )
                ),

                # NOTE: проверяем что пользователь еще не выполнил задачу
                ActivityTask.id.not_in(
                    select(TaskCompletionProof.activity_task_id)
                    .where(
                        TaskCompletionProof.telegram_id == user_id,
                        TaskCompletionProof.status == TaskCompletionStatus.PENDING,
                    )
                ),

                # NOTE: проверяем что пользователь выполнил задачу
                ActivityTask.id.not_in(
                    select(ActivityTaskCompletion.activity_task_id)
                    .where(
                        ActivityTaskCompletion.telegram_id == user_id,
                    )
                )

            )
            .order_by(ActivityTask.deadline.asc())
        )

        return (await self._session.execute(query)).scalars().first()


class ActivityTasksEventsRepository(Repository):
    def __init__(self, session):
        super().__init__(ActivityTaskUserEvent, session)

    async def is_user_cancel_task(self, user_id: int, task_id: int) -> list[ActivityTaskUserEvent]:
        return (await self._session.execute(
            select(ActivityTaskUserEvent).where(
                ActivityTaskUserEvent.telegram_id == user_id,
                ActivityTaskUserEvent.type == ActivityTaskUserEventType.LEAVE,
                ActivityTaskUserEvent.activity_task_id == task_id,
            )
        )).scalars().all()
