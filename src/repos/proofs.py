
from sqlalchemy import select
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
        )
        return (await self._session.execute(query)).scalars().all()
