
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.niches import NichesService

from src.api.schemas import NicheDataResponse
from src.api.schemas.user import TelegramUserID
from src.api.schemas.default import DefaultResponse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['niches'],
)


@router.get('/niches/{niche_id}')
async def get_niche_by_id(niche_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> NicheDataResponse:
    """Получить нишу по ID"""
    result = await NichesService(session).get_by_id(niche_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result


@router.get('/users/{user_id}/niches')
async def get_user_niche(user_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> NicheDataResponse:
    """Получить нишу пользователя"""
    result = await NichesService(session).get_selected_niche(user_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result


@router.post('/niches/{niche_id}/select')
async def select_niche(niche_id: int, user: TelegramUserID, session: Annotated[AsyncSession, Depends(get_session)]) -> NicheDataResponse:
    """Выбрать нишу"""
    result = await NichesService(session).select_niche(niche_id, user.telegram_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result
