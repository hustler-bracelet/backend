import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.common.exceptions import CustomException
from src.api import (
    activities_router,
    activity_tasks_router,
    niches_router,
    leaderboard_router,
    proofs_router,
)
from src.api.schemas.default import DefaultResponse


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
app.include_router(leaderboard_router)
app.include_router(proofs_router)


app.add_event_handler('startup', lambda: logging.info('Application started'))


def handle_exception(request, exc):
    logging.error(exc)
    return JSONResponse(
        status_code=400,
        content=DefaultResponse(
            message='Internal server error',
            success=False
        ).model_dump()
    )


app.add_exception_handler(
    CustomException,
    handle_exception,
)
