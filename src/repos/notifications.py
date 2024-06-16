import pytz

from datetime import datetime, timedelta
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import NotificationType, NotificationRecords

from .generic import Repository


class NotificationRepository(Repository[NotificationRecords]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(NotificationRecords, session)

    async def already_sent(self, user_id: int, type: NotificationType, period_days: int = 7) -> bool:
        now, period = datetime.now(tz=pytz.utc), datetime.now(tz=pytz.utc) - timedelta(days=period_days)
        query = (
            select(NotificationRecords)
            .where(
                NotificationRecords.telegram_id == user_id,
                NotificationRecords.type == type,
                NotificationRecords.created_at >= period,
                NotificationRecords.created_at < now,
            )
        )

        return bool((await self._session.execute(query)).scalars().all())
