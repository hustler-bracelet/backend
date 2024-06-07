
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from src.repos import Repository
from src.database.models import Niche, Activity, User
from src.common.emoji import EmojiParser, EmojiName
from src.common.exceptions import InvalidNameError

from src.api.schemas.activities import UserNicheResponse, NicheData

from .base import BaseDatabaseService


class NichesService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(Niche, self._session)

        self._user_repo = Repository(User, self._session)

    async def create_new(self, niche: NicheData, activity: Activity) -> Niche:
        """
        Create new niche

        :param niche: niche data
        :param activity: activity
        """

        parser = EmojiParser(niche.name)

        if not parser.contains_emoji:
            raise InvalidNameError(f'Invalid niche name: {niche.name} - must contain emoji')

        parsed_name: EmojiName = parser.parse()

        model = Niche(
            **niche.model_dump(include=['description']),
            **parsed_name.model_dump(),
            activity_id=activity.id
        )

        return await self._repo.create(model)

    async def get_by_id(self, _id: int) -> Niche | None:
        """Получить текущую нишу"""
        return await self._repo.get_by_pk(_id, options=[selectinload(Niche.tasks)])

    async def select_niche(self, niche_id: int, user_id: int):
        """Выбрать нишу"""
        user = await self._user_repo.get_by_pk(user_id)
        niche = await self.get_by_id(niche_id)

        if not niche:
            raise HTTPException(status_code=404, detail='Niche not found')

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        user.selected_niche_id = niche.id
        await self._user_repo.update(user)

        return niche

    async def get_selected_niche(self, user_id: int) -> Niche | None:
        """Получить выбранную нишу"""
        user = await self._user_repo.get_by_pk(user_id)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if not user.selected_niche_id:
            return None

        return await self.get_by_id(user.selected_niche_id)
