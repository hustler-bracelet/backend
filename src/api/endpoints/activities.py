
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.activities import ActivitySummaryResponse
from src.database.models import Activity, User
from src.services.user import UsersService
from src.services.activities import ActivityEventsService, ActivitiesService
from src.scheduler.activity import schedule_activity_deadline
from src.services.activities_status import ActivityStatusService

from src.api.schemas import ActivityStartResponseData, ActivityDataResponse, ActivityStartRequestData, ActivityUserStatusResponse
from src.api.schemas.user import TelegramUserID
from src.api.schemas.default import DefaultResponse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['activities'],
)


@router.post('/send_data', status_code=status.HTTP_201_CREATED)
async def send_data_handler(
    data: ActivityStartRequestData, 
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ActivityStartResponseData:

    activity: Activity = await ActivityEventsService(session).create_event(data)

    return ActivityStartResponseData(
        did_start_activity=True,
        description=f'Активность {activity.name} успешно запущена!'
    )


@router.get('/activities')
async def get_current_activities(
    session: Annotated[AsyncSession, Depends(get_session)],
    is_active: bool = False,
) -> list[ActivityDataResponse]:
    """Получить текущую активность"""
    result = await ActivitiesService(session).filter(is_active)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result


@router.get('/activities/{activity_id}')
async def get_current_activity(activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivityDataResponse:
    """Получить текущую активность"""
    result = await ActivitiesService(session).get_by_id(activity_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result


@router.post('/activities/{activity_id}/stop')
async def stop_activity(activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    """Остановить активность"""
    activity = await ActivityEventsService(session).stop_event(activity_id)

    return DefaultResponse(
        success=True,
        message=f'Активность {activity.name} успешно остановлена!',
    )


@router.get('/activities/{activity_id}/run')
async def run_activity(activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    """Запустить активность"""
    activity = await ActivityEventsService(session).start_event(activity_id)

    schedule_activity_deadline(activity.id, activity.deadline)

    return DefaultResponse(
        success=True,
        message=f'Активность {activity.name} успешно запущена!',
    )


@router.get('/users/{user_id}/activities/{activity_id}/summary')
async def get_user_activity_summary(user_id: int, activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivitySummaryResponse:
    """Получить активность пользователя"""
    user: User = await UsersService(session).get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    result = await ActivityEventsService(session).get_user_event_summary_by_user(user, activity_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result


@router.post('/activities/{activity_id}/leave')
async def leave_activity(activity_id: int, user_data: TelegramUserID, session: Annotated[AsyncSession, Depends(get_session)]):
    """Покинуть активность"""

    user: User = await UsersService(session).get_by_id(user_data.telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    await ActivityEventsService(session).leave_event(user, activity_id)

    return DefaultResponse(
        success=True,
        message=f'Вы покинули активность!',
    )


@router.get('/activities/{activity_id}/status')
async def get_activity_status(activity_id: int, user_data: TelegramUserID, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivityUserStatusResponse:
    """Получить статус активности для пользователя"""
    user = await UsersService(session).get_by_id(user_data.telegram_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    activity = await ActivitiesService(session).get_by_id(activity_id)

    if not activity:
        raise HTTPException(status_code=404, detail='Activity not found')

    return await ActivityStatusService(session).get_user_activity_status(user, activity)
