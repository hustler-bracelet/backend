from datetime import datetime

from src.repos import Repository
from src.database.models import User

from .base import BaseDatabaseService


class UsersService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(User, self._session)

    async def get_by_id(self, _id: int) -> User | None:
        """Получить текущую нишу"""
        return await self._repo.get_by_pk(_id)
