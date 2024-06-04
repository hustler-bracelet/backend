
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.niches import NichesService

from src.api.schemas import NicheDataResponse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['niches'],
)


@router.get('/niches/{niche_id}')
async def get_niche_by_id(niche_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> NicheDataResponse:
    """Получить текущую задачу для ниши"""
    result = await NichesService(session).get_by_id(niche_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result
