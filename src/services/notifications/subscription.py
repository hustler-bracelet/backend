
from aiogram import Bot
from .base import BaseTelegramNotificationService


class SubscriptionNotificationService(BaseTelegramNotificationService):
    async def send_notification(self, user_id: int, already_expired: bool = False):
        text = (
            f"❗️ У тебя {'заканчивается' if not already_expired else 'закончилась'} подписка!\n\n"
            "Зайди в главное меню и продли ее - /start"
        )
        await self.send_text_notification(user_id, text)
