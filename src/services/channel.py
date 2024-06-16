
from aiogram import Bot
from .base import BotService


class HustlerChannelsService(BotService):
    def __init__(self, bot: Bot, channel_id: int) -> None:
        super().__init__(bot)
        self._channel_id = channel_id

    async def is_user_in_channel(self, user_id: int) -> bool:
        try:
            res = await self._bot.get_chat_member(
                self._channel_id, 
                user_id,
            )
            return res.status != 'left'
        except Exception:
            return False

    async def kick_user(self, user_id: int):
        try:
            await self._bot.ban_chat_member(
                self._channel_id, 
                user_id,
            )
            await self._bot.unban_chat_member(
                self._channel_id, 
                user_id,
            )
        except Exception:
            pass
