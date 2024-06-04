
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.niches import NichesService

from src.api.schemas import NicheDataResponse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['activity_tasks'],
)


@router.get('/activities/current/niches/{niche_id}/tasks/current')
async def get_current_task(niche_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> NicheDataResponse:
    """Получить текущую задачу для ниши"""
    result = await NichesService(session).get_by_id(niche_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result
