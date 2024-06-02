
from datetime import datetime

from src.repos import Repository
from src.database.models import Niche, Activity
from src.common.emoji import EmojiParser, EmojiName
from src.common.exceptions import InvalidNameError

from src.api.schemas.activities import NicheData

from .base import BaseDatabaseService


class NichesService(BaseDatabaseService):
    def post_init(self):
        self._repo = Repository(Niche, self._session)

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
