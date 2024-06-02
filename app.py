import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import activities_router


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

origins = [
    'nsdkin.ru',
    'webapp.c.nsdkin.ru',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST'],
    allow_headers=['*']
)

app.include_router(activities_router)
