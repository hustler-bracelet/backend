import asyncio

from aiogram import Bot, types
from src.database.models import ActivityTask, User

from .base import BaseTelegramNotificationService


class ActivityTaskNotificationService(BaseTelegramNotificationService):

    async def send_notification(self, task: ActivityTask, users: list[User]) -> bool:
        text = (
            "🔔 У тебя новое задание:\n\n"
            f"{task.name}"
        )
        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Посмотреть задание",
                        callback_data=f"open_activity_task:{task.activity_id}",
                    )
                ]
            ]
        )

        for user in users:
            await self.send_text_notification(
                chat_id=user.telegram_id,
                message=text,
                reply_markup=kb
            )
            await asyncio.sleep(0.3)
