
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional


from .leaderboard import LeaderBoardItem
from .user import TelegramUserID


class ActivityTaskData(BaseModel):
    name: str
    description: str
    deadline: datetime
    points: int

    @field_validator('description')
    def validate_description(cls, value: str):
        new_value = value.replace('<p>', '').replace('</p>', '')
        return new_value


class ActivityTaskCreateData(BaseModel):
    name: str
    description: str
    deadline: datetime
    points: int

    @field_validator('description')
    def validate_description(cls, value: str):
        new_value = value.replace('<p>', '').replace('</p>', '')
        return new_value


class NicheData(BaseModel):
    name: str
    description: str
    task: ActivityTaskData

    @field_validator('description')
    def validate_description(cls, value: str):
        new_value = value.replace('<p>', '').replace('</p>', '')
        return new_value


class ActivityDataCreate(BaseModel):
    name: str
    description: str
    fund: int
    total_places: int
    deadline: datetime

    @field_validator('description')
    def validate_description(cls, value: str):
        new_value = value.replace('<p>', '').replace('</p>', '')
        return new_value


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


class UserNicheResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str

    task: Optional['ActivityTaskDataResponse']

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


class ActivitySummaryResponse(BaseModel):
    id: int
    emoji: str
    name: str
    description: str
    fund: int
    total_places: int
    started_on: datetime
    deadline: datetime

    leaderboard_data: list[LeaderBoardItem] | None
    user_leaderboard_data: LeaderBoardItem | None
    niche: UserNicheResponse

    class Config:
        orm_mode = True


class ActivityStartRequestData(BaseModel):
    activity: ActivityDataCreate
    user: TelegramUserID
    niches: list[NicheData]


class ActivityStartResponseData(BaseModel):
    did_start_activity: bool
    description: str


class ActivityUserStatusResponse(BaseModel):
    is_running: bool
    occupied_places: int
    total_places: int
    can_join: bool
    already_joined: bool


class ActivityTaskStatus(BaseModel):
    can_do_task: bool
    already_done: bool
