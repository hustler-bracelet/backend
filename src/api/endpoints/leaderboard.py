
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.activity_leaderboard import ActivityLeaderboardService
from src.services.activities import ActivitiesService
from src.database.models import Activity

from src.api.schemas.leaderboard import LeaderBoardItem
from src.dependencies.session import get_session


router = APIRouter(
    tags=['activity_tasks'],
)


@router.get('/activities/{activity_id}/leaderboard')
async def get_current_leaderboard(activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> list[LeaderBoardItem]:
    """Получить лидерборд для активности"""
    result: Activity | None = await ActivitiesService(session).get_by_id(activity_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return await ActivityLeaderboardService(session).get_leaderboard(result)
