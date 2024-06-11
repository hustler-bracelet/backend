
from src.repos import Repository
from src.database.models import Activity, ActivityUserEvent, Niche, User, ActivityUserEventType

from src.repos.niche import NichesRepository
from src.repos.user import UserRepository

from src.api.schemas.activities import ActivityUserStatusResponse

from .activities import ActivitiesService
from .base import BaseDatabaseService


class ActivityStatusService(BaseDatabaseService):
    def post_init(self):
        self._event_repo = Repository(ActivityUserEvent, self._session)
        self._user_repo = UserRepository(self._session)
        self._niche_repo = NichesRepository(self._session)

    async def get_user_activity_status(self, user: User, activity: Activity) -> ActivityUserEvent:
        niches = await self._niche_repo.get_all_by_activity(activity.id)
        niche_ids = [niche.id for niche in niches]
        users = await self._user_repo.get_all_with_niche_id(niche_ids)

        result = await self._event_repo.filter_by(
            telegram_id=user.telegram_id,
            activity_id=activity.id,
            type=ActivityUserEventType.LEAVE,
        )

        return ActivityUserStatusResponse(
            is_running=activity.is_running,
            occupied_places=len(users),
            total_places=activity.total_places,
            can_join=not bool(len(result.all())),
            already_joined=user.selected_niche_id in niche_ids,
        )
