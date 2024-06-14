
from aiogram import types

from src.database.models import ActivityTask
from src.common.texts import plural_form

from .base import BaseTelegramNotificationService


class ProofsNotificationService(BaseTelegramNotificationService):
    async def send_decline_notification(self, telegram_id: int, task: ActivityTask) -> None:
        text = (
            f"❗️ Твой пруф на задание {task.name} <b>отклонён</b>!\n\n"
            "Если это ошибка - напиши @ambienthugg"
        )

        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="👀 Посмотреть задание",
                        callback_data=f"open_activity_task:{task.activity_id}",
                    )
                ]
            ]
        )

        await self.send_text_notification(telegram_id, text, reply_markup=kb)


    async def send_accept_notification(self, telegram_id: int, task: ActivityTask, extra_points: int = 0) -> None:
        main_points_str = plural_form(
            task.points,
            [
                "балл",
                "балла",
                "баллов",
            ]
        )

        extra_points_str = plural_form(
            extra_points,
            [
                "дополнительный балл",
                "дополнительных балла",
                "дополнительных баллов",
            ]
        )

        text = (
            f"✅ Твой пруф на задание {task.name} <b>принят</b>!\n\n"
            f"Ты заработал за это задание <b>{main_points_str} + {extra_points_str}</b>!\n\n"
        )

        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🏆 Открыть ТОП",
                        callback_data=f"open_leaderboard:{task.activity_id}",
                    )
                ]
            ]
        )

        await self.send_text_notification(telegram_id, text, reply_markup=kb)
