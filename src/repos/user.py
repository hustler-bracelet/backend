
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import User

from .generic import Repository


class UserRepository(Repository):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_all_with_niche_id(self, niches_ids: list[int]) -> list[User]:
        return (await self._session.execute(
            select(User).where(User.selected_niche_id.in_(niches_ids))
        )).scalars().all()
