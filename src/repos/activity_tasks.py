
from sqlalchemy import select
from datetime import datetime

from src.database.models import ActivityTask

from .generic import Repository


class ActivityTasksRepository(Repository):
    def __init__(self, session):
        super().__init__(ActivityTask, session)

    async def get_current_by_niche(self, niche_id: int) -> ActivityTask | None:
        query = (
            select(ActivityTask)
            .where(
                ActivityTask.niche_id == niche_id,
                ActivityTask.deadline >= datetime.utcnow(),
            )
            .order_by(ActivityTask.deadline.desc())
        )

        return (await self._session.execute(query)).scalars().first()
