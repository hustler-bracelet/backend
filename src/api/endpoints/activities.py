
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Activity
from src.services.activities import ActivityEventsService, ActivitiesService

from src.api.schemas import ActivityStartRequestData, ActivityStartResponseData, ActivityDataResponse
from src.dependencies.session import get_session


router = APIRouter(
    tags=['activities'],
)


@router.post('/send_data', status_code=status.HTTP_201_CREATED)
async def send_data_handler(
    data: ActivityStartRequestData, 
    session: Annotated[AsyncSession, Depends(get_session)]
) -> ActivityStartResponseData:

    activity: Activity = await ActivityEventsService(session).create_event(data)

    return ActivityStartResponseData(
        did_start_activity=True,
        description=f'Активность {activity.name} успешно запущена!'
    )


@router.get('/activities/current')
async def get_current_activities(session: Annotated[AsyncSession, Depends(get_session)]) -> ActivityDataResponse:
    """Получить текущую активность"""
    result = await ActivitiesService(session).get_current()

    if not result:
        raise HTTPException(status_code=404, detail='No active activity found')

    return result
