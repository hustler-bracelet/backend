import logging

from aiogram import Bot, types
from typing import Any


logger = logging.getLogger(__name__)


class BaseTelegramNotificationService:
    def __init__(self, bot: Bot):
        self._bot = bot

    async def send_text_notification(
        self, 
        chat_id: int, 
        message: str, 
        reply_markup: types.ReplyKeyboardMarkup | Any | None = None,
    ) -> bool:
        try:
            await self._bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=reply_markup
            )
        # TODO: handle exceptions
        except Exception as e:
            logger.error(e)
            return False
        return True
