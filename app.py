# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

origins = [
    'nsdkin.ru'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST'],
    allow_headers=['*']
)


class ActivityTask(BaseModel):
    name: str
    description: str
    deadline: datetime
    points: int


class Niche(BaseModel):
    name: str
    description: str
    task: ActivityTask


class Activity(BaseModel):
    name: str
    description: str
    fund: int
    places: int
    deadline: datetime


class ActivityStartRequestData(BaseModel):
    activity: Activity
    niches: list[Niche]


class ActivityStartResponseData(BaseModel):
    did_start_activity: bool
    description: str


@app.post('/send_data')
async def send_data_handler(data: ActivityStartRequestData) -> ActivityStartResponseData:
    print(data.model_dump_json(indent=4))
    return ActivityStartResponseData(
        did_start_activity=True,
        description='Активность успешно запущена'
    )
