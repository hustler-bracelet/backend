
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import TaskCompletionProof, ActivityTask
from src.enums import TaskCompletionStatus

from .generic import Repository


class ProofsRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(TaskCompletionProof, session)

    async def get_all_by_activity(self, activity_id: int) -> list[TaskCompletionProof]:
        query = (
            select(TaskCompletionProof)
            .where(
                TaskCompletionProof.activity_task_id.in_(
                    select(ActivityTask.id).where(ActivityTask.activity_id == activity_id)
                ),
                TaskCompletionProof.status == TaskCompletionStatus.PENDING,
            )
            .options(selectinload(TaskCompletionProof.user), selectinload(TaskCompletionProof.task))
            .order_by(TaskCompletionProof.sent_on.desc())
        )
        return (await self._session.execute(query)).scalars().all()

    async def get_all_by_user(self, user_id: int, task_id: int) -> list[TaskCompletionProof]:
        return (await self._session.execute(
            select(TaskCompletionProof).where(
                TaskCompletionProof.telegram_id == user_id,
                TaskCompletionProof.activity_task_id == task_id,
                or_(
                    TaskCompletionProof.status == TaskCompletionStatus.PENDING,
                    TaskCompletionProof.status == TaskCompletionStatus.VERIFIED,
                )
            )
        )).scalars()
