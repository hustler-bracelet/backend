
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from src.services.activity_tasks import ActivityTasksService
from src.services.niches import NichesService
from src.database.models import Niche

from src.api.schemas.activities import ActivityTaskDataResponse, ActivityTaskStatus, ActivityTaskCreateData
from src.api.schemas.user import TelegramUserID
from src.dependencies.session import get_session


router = APIRouter(
    tags=['activity_tasks'],
)


@router.get('/niches/{niche_id}/tasks/current')
async def get_current_task(niche_id: int, user: TelegramUserID, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivityTaskDataResponse:
    """Получить текущую задачу для ниши"""
    result = await ActivityTasksService(session).get_current(niche_id, user.telegram_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result


@router.post('/niches/{niche_id}/tasks', status_code=status.HTTP_201_CREATED)
async def create_new_task(niche_id: int, activity_task: ActivityTaskCreateData, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivityTaskDataResponse:
    """Создать новую задачу для ниши"""
    niche: Niche = await NichesService(session).get_by_id(niche_id)

    if not niche:
        raise HTTPException(status_code=404, detail='Niche not found')

    return await ActivityTasksService(session).create_new(activity_task, niche, activity_id=niche.activity_id)


@router.get('/tasks/{task_id}/status')
async def get_task_status_for_user(task_id: int, user_id: TelegramUserID, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivityTaskStatus:
    """Получить статус выполнения задачи"""
    return await ActivityTasksService(session).get_status(task_id, user_id.telegram_id)


@router.post('/tasks/{task_id}/cancel')
async def cancel_task(task_id: int, user: TelegramUserID, session: Annotated[AsyncSession, Depends(get_session)]):
    """Отменить выполнение задачи"""
    return await ActivityTasksService(session).cancel_task(task_id, user.telegram_id)
