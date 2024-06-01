
from fastapi import APIRouter, Depends
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import Activity
from src.services.activities import ActivityEventsService

from src.api.schemas import ActivityStartRequestData, ActivityStartResponseData
from src.dependencies.session import get_session


router = APIRouter()


@router.post('/send_data')
async def send_data_handler(
    data: ActivityStartRequestData, 
    session: Annotated[AsyncSession, Depends(get_session)]
) -> ActivityStartResponseData:

    activity: Activity = await ActivityEventsService(session).create_event(data)

    return ActivityStartResponseData(
        did_start_activity=True,
        description=f'Активность {activity.name} успешно запущена!'
    )
