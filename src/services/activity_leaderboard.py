import logging
import pandas as pd

from datetime import datetime
from typing import TypedDict
from sqlalchemy.orm import selectinload

from src.database.models import ActivityTaskCompletion, Activity, User
from src.api.schemas.leaderboard import LeaderBoardItem, EarnData
from src.api.schemas.user import User as UserSchema
from src.repos.activity_task_completion import ActivityTasksCompletionRepository

from src.common.activity import distribute_funds

from .base import BaseDatabaseService


class ActivityLeaderboardData(TypedDict):
    telegram_id: int
    name: str
    sum: int


class ActivityLeaderboardService(BaseDatabaseService):
    def post_init(self):
        self._repo = ActivityTasksCompletionRepository(self._session)

    def _convert_to_leaderboard(self, data: list[ActivityTaskCompletion]) -> list[ActivityLeaderboardData]:
        """Преобразовать данные в лидерборд, получить сумму для уникальных пользователей"""
        df = pd.DataFrame([
            {
                'telegram_id': item.user.telegram_id,
                'name': item.user.telegram_name,
                'sum': item.points,
                'created_at': item.sent_on,
            }
            for item in data
        ])

        grouped_df: pd.DataFrame = df.groupby(['telegram_id', 'name', 'created_at'], as_index=False)['sum'].sum()

        sorted_df = grouped_df.sort_values(by=['created_at'], ascending=True)

        return sorted_df.to_dict(orient='records')

    async def get_leaderboard(self, activity: Activity) -> list[LeaderBoardItem]:
        """Получить лидерборд активности"""
        completed_tasks = await self._repo.get_tasks_completed_by_activity(activity.id)

        if not completed_tasks:
            return []

        leaderboard = []
        converted_data: list[ActivityLeaderboardData] = self._convert_to_leaderboard(completed_tasks)
        current_places: int = len(converted_data)

        total_places: int = activity.total_places if activity.total_places <= current_places else current_places

        for ctr, (sum, data) in enumerate(zip(distribute_funds(activity.fund, total_places), converted_data), start=1):
            leaderboard.append(
                LeaderBoardItem(
                    user=UserSchema(
                        telegram_id=data['telegram_id'],
                        telegram_name=data['name'],
                    ),
                    points=data['sum'],
                    position=ctr,
                    earn=EarnData(
                        sum=sum,
                    )
                )
            )

        return leaderboard

    async def get_leaderboard_item_by_user(self, user: User, activity: Activity) -> LeaderBoardItem | None:
        """Получить лидерборд пользователя"""
        leaderbord_items: list[LeaderBoardItem] = await self.get_leaderboard(activity)

        for item in leaderbord_items:
            if item.user.telegram_id == user.telegram_id:
                return item

        return None
