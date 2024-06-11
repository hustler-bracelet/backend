import asyncio

from aiogram import Bot, types

from src.api.schemas import ActivityStartRequestData

from .base import BaseTelegramNotificationService


"""
⚡️ Запуск активности

Название: 💰 Сезон крипты
Описание:
Ну что, хаслеры, время пампить, дампить, хуямпить, МММ’ить, и регулировать стаканы!
Выбирай свою нишу и вперёд жарить стейкинги!
Мест: 20
Призовой фонд: 100 000₽
Дедлайн: 7 июля 2024 (23:59 МСК)

✈️ TON staker
Этот броуски любит Дурова
Первое задание: Стейкать тон
(описание типа)
5 баллов, до 3 июля 23:59 МСК

💲 USDT enjoyer
За классику
Первое задание: Хз чё-нить сделай
(описание типа)
5 баллов, до 3 июля 23:59 МСК

🍼 MUMBA pusher
Абобус
Первое задание: я кусаю кошек
(описание типа)
5 баллов, до 3 июля 23:59 МСК

Погнали, хуле?

"""


class AdminActivityNotificationService(BaseTelegramNotificationService):

    async def send_notification(self, user_id: int, activity_id: int, data: ActivityStartRequestData) -> bool:
        text = (
            "⚡️ Запуск активности\n\n"
            f"Название: {data.activity.name}\n"
            f"Описание: {data.activity.description}\n"
            f"Мест: {data.activity.total_places}\n"
            f"Призовой фонд: {data.activity.fund} ₽\n"
        )

        for niche in data.niches:
            text += (
                f"{niche.name}\n"
                f"{niche.description}\n"
                f"Первое задание: {niche.task.name}"
                f"{niche.task.description}\n"
                f"{niche.task.points} баллов, до {niche.task.deadline}\n\n"
            )

        kb = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="⚡️ Запустить активность",
                        callback_data=f"admin:activity_run:{activity_id}",
                    )
                ]
            ]
        )

        await self._bot.send_message(user_id, text, reply_markup=kb)
