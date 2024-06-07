import dramatiq
import logging

from src.repos import Repository

from src.database.models import User, Activity
from src.services.notifications.activity import ActivityNotificationService
from src.services.activity_leaderboard import ActivityLeaderboardService

from .worker import bot, SessionMaker


log = logging.getLogger(__name__)


@dramatiq.actor(max_retries=0)
async def send_start_activity_notification(activity_id: int):
    """Отправить уведомление о начале активности"""

    async with SessionMaker() as session:

        activity = await Repository(Activity, session).get_by_pk(activity_id)
        notification = ActivityNotificationService(bot)

        if not activity:
            log.warning(f'Activity {activity_id} not found')
            return

        users = await Repository(User).get_all()

        for user in users:
            await notification.send_activity_notification(user, activity)

        log.info(f'Sent notification to {len(users)} users')


@dramatiq.actor(max_retries=0)
async def send_finish_activity_notification(activity_id: int):
    """Отправить уведомление о окончании активности"""

    async with SessionMaker() as session:

        activity = await Repository(Activity).get_by_pk(activity_id)
        leader_board = ActivityLeaderboardService()

        notification = ActivityNotificationService(bot)

