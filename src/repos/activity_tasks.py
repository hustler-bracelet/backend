
from typing import override
from sqlalchemy import select

from src.database.models import ActivityTask

from .generic import Repository


class ActivityTasksRepository(Repository):
    @override
    def __init__(self, session):
        super().__init__(ActivityTask, session)

    async def get_current_by_niche(self, niche_id: int) -> ActivityTask | None:
        query = (
            select(ActivityTask)
            .filter_by(niche_id=niche_id, is_active=True)
            .order_by(ActivityTask.deadline.desc())
        )

        return (await self._session.execute(query)).scalars().first()
