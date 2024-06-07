import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import (
    activities_router,
    activity_tasks_router,
    niches_router,
)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

origins = [
    'nsdkin.ru',
    'webapp.c.nsdkin.ru',
    'https://webapp.c.nsdkin.ru',
    'https://nsdkin.ru',
    '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(activities_router)
app.include_router(activity_tasks_router)
app.include_router(niches_router)
