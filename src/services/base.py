
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import Bot


class BaseDatabaseService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.post_init()

    def post_init(self):
        pass


class BotService:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot
