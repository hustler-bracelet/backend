
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


class ActivityDataCreate(BaseModel):
    name: str
    description: str
    fund: int
    total_places: int = Field(alias='places')
    deadline: datetime


class ActivityDataResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str
    fund: int
    total_places: int
    started_on: datetime
    deadline: datetime

    niches: list['NicheDataResponse']

    class Config:
        orm_mode = True


class NicheDataResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str

    tasks: list['ActivityTaskDataResponse']

    class Config:
        orm_mode = True

class ActivityTaskDataResponse(BaseModel):
    id: int
    name: str
    description: str
    points: int
    added_on: datetime
    deadline: datetime

    class Config:
        orm_mode = True


class ActivityStartRequestData(BaseModel):
    activity: ActivityDataCreate
    niches: list[NicheData]


class ActivityStartResponseData(BaseModel):
    did_start_activity: bool
    description: str
