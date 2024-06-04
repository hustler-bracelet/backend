
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.activity_tasks import ActivityTasksService

from src.api.schemas import ActivityTaskDataResponse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['activity_tasks'],
)


@router.get('/activities/current/niches/{niche_id}/tasks/current')
async def get_current_task(niche_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivityTaskDataResponse:
    """Получить текущую задачу для ниши"""
    result = await ActivityTasksService(session).get_current(niche_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result
