
from src.database.models import Activity, User
from src.common.format import format_number

from .base import BaseTelegramNotificationService


class ActivityNotificationService(BaseTelegramNotificationService):

    async def send_activity_notification(self, user: User, activity: Activity) -> bool:
        """Отправить уведомление об активности"""

        text = (
            f"🔔 Началась активность <b>«{activity.name}»</b>!\n\n"
            f"⚡️ Скорее успей залететь и побороться за <b>{format_number(activity.fund)}₽</b>, пока есть свободные места!"
        )

        await self._bot.send_message(user.telegram_id, text)

    async def send_activity_finished_notification(self, user: User, earn_str: str, activity: Activity) -> bool:
        """Отправить уведомление об окончании активности"""

        text = (
            f"🔔 Активность <b>«{activity.name}»</b> закрыта!\n"
            f"{earn_str}"
            "➡️ Чтобы получить деньги, напиши @ambienthugg\n"
            "❗ Для удобства ты можешь получить деньги в TON-ах\n"
        )

        await self._bot.send_message(user.telegram_id, text)
