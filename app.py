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
from src.scheduler.worker import scheduler, default_job_store
from src.scheduler.subscription import check_sub_job, check_sub_noti_job


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


async def startup():
    scheduler.remove_all_jobs(default_job_store)

    scheduler.add_job(check_sub_job, id='check_sub_job', trigger='interval', hours=1, max_instances=1, replace_existing=True)
    scheduler.add_job(check_sub_noti_job, id='check_sub_noti_job', trigger='interval', hours=1, max_instances=1, replace_existing=True)

    scheduler.start()

app.add_event_handler('startup', startup)


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
