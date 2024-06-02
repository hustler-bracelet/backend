
from datetime import datetime
from pydantic import BaseModel, Field


class ActivityTaskData(BaseModel):
    name: str
    description: str
    deadline: datetime
    points: int


class NicheData(BaseModel):
    name: str
    description: str
    task: ActivityTaskData


class ActivityData(BaseModel):
    name: str
    description: str
    fund: int
    total_places: int = Field(alias='places')
    deadline: datetime


class ActivityStartRequestData(BaseModel):
    activity: ActivityData
    niches: list[NicheData]


class ActivityStartResponseData(BaseModel):
    did_start_activity: bool
    description: str
