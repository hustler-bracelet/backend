import pytz

from datetime import datetime

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import BraceletSubscription

from .generic import Repository


class SubscriptionRepository(Repository[BraceletSubscription]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(BraceletSubscription, session)

    async def get_all_expired(self) -> list[BraceletSubscription]:
        query = (
            select(BraceletSubscription)
            .where(
                BraceletSubscription.will_end_on < datetime.now(tz=pytz.timezone('Europe/Moscow')),
            )
            .order_by(BraceletSubscription.will_end_on)
        )
        return await self._session.execute(query)

    async def get_last_subscription(self, telegram_id: int) -> BraceletSubscription | None:
        query = (
            select(BraceletSubscription)
            .where(
                BraceletSubscription.telegram_id == telegram_id,
            )
            .order_by(BraceletSubscription.will_end_on.desc())
            .limit(1)
        )

        return (await self._session.execute(query)).scalar()
