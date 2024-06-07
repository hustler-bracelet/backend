
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.schemas.activities import ActivitySummaryResponse
from src.database.models import Activity, User
from src.services.user import UsersService
from src.services.activities import ActivityEventsService, ActivitiesService

from src.api.schemas import ActivityStartRequestData, ActivityStartResponseData, ActivityDataResponse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['activities'],
)


@router.post('/send_data', status_code=status.HTTP_201_CREATED)
async def send_data_handler(
    data: dict, 
    session: Annotated[AsyncSession, Depends(get_session)]
) -> dict:

    # activity: Activity = await ActivityEventsService(session).create_event(data)

    return ActivityStartResponseData(
        did_start_activity=True,
        #description=f'Активность {activity.name} успешно запущена!'
        description='Активность запущена!'
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


@router.post('/activities/{activity_id}/stop')
async def stop_activity(activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    """Остановить активность"""
    await ActivityEventsService(session).stop_event(activity_id)


@router.get('/users/{user_id}/activities/{activity_id}/summary')
async def get_user_activity_summary(user_id: int, activity_id: int, session: Annotated[AsyncSession, Depends(get_session)]) -> ActivitySummaryResponse:
    """Получить активность пользователя"""
    user: User = await UsersService(session).get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    result = await ActivityEventsService(session).get_user_event_summary(user, activity_id)

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result
