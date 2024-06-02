
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDatabaseService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

        self.post_init()

    def post_init(self):
        pass
