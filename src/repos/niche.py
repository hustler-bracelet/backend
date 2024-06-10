
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Niche

from .generic import Repository


class NichesRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(Niche, session)

    async def get_all_by_activity(self, activity_id: int) -> list[Niche]:
        return (await self._session.execute(
            select(Niche).where(Niche.activity_id == activity_id)
        )).scalars().all()
