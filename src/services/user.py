from datetime import datetime

from src.repos import Repository
from src.database.models import User, ActivityUserEvent, ActivityUserEventType, Activity

from .base import BaseDatabaseService


class UsersService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(User, self._session)
        self._record_repo = Repository(User, self._session)

    async def get_by_id(self, _id: int) -> User | None:
        """Получить текущую нишу"""
        return await self._repo.get_by_pk(_id)

    async def leave_current_activity(self, user: User, activity: Activity):
        """Покинуть текущую активность"""
        user.selected_niche_id = None
        await self._repo.update(user)

        event = ActivityUserEvent(
            telegram_id=user.telegram_id,
            type=ActivityUserEventType.LEAVE,
            activity_id=activity.id,
        )
        await self._record_repo.create(event)
