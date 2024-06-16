import pytz

from datetime import datetime

from src.repos import Repository
from src.database.models import BraceletSubscription, User, NotificationRecords, NotificationType

from src.common.bot import BOT
from src.services.channel import HustlerChannelsService
from src.repos.subsctiption import SubscriptionRepository
from src.repos.notifications import NotificationRepository

from config import CHANNEL_ID

from .base import BaseDatabaseService
from .notifications.subscription import SubscriptionNotificationService


class SubscriptionService(BaseDatabaseService):
    def post_init(self):
        self._repo = SubscriptionRepository(self._session)
        self._user_repo = Repository(User, self._session)

    async def check_subscription(self, user_id: int) -> bool:
        subscription = await self._repo.get_last_subscription(user_id)

        if not subscription:
            return False

        if subscription.will_end_on < datetime.now(tz=pytz.timezone('Europe/Moscow')):
            return False

        return True


class SubscriptionJobService(SubscriptionService):
    def post_init(self):
        super().post_init()
        self._channel = HustlerChannelsService(BOT, CHANNEL_ID)
        self._notifications = SubscriptionNotificationService(BOT)
        self._notifications_repo = NotificationRepository(self._session)

    async def expire_subscriptions_job(self):
        users: list[User] = await self._user_repo.get_all()

        for user in users:
            result = await self.check_subscription(user.telegram_id)

            # NOTE: все ок, подписка не истекла
            if result:
                continue

            # NOTE: подписка истекла
            if await self._channel.is_user_in_channel(user.telegram_id):
                await self._channel.kick_user(user.telegram_id)

            else:
                continue

            await self._notifications.send_notification(user.telegram_id, already_expired=True)

    async def expire_subscriptions_notifications_job(self):
        users: list[User] = await self._user_repo.get_all()

        for user in users:
            subscription: BraceletSubscription = await self._repo.get_last_subscription(user.telegram_id)

            # NOTE: нет подписки
            if not subscription:
                continue

            # NOTE: уведы только за 3 дня
            if (subscription.will_end_on - datetime.now(tz=pytz.timezone('Europe/Moscow'))).days != 3:
                continue

            already_sent = await self._notifications_repo.already_sent(
                user_id=user.telegram_id, type=NotificationType.SUB_END_IN_3_DAYS, period_days=5
            )

            if already_sent:
                continue

            await self._notifications.send_notification(user.telegram_id)
            noti = NotificationRecords(
                telegram_id=user.telegram_id,
                type=NotificationType.SUB_END_IN_3_DAYS,
            )
            await self._notifications_repo.create(noti)
