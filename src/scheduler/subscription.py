import logging

from datetime import datetime

from src.services.subscription import SubscriptionJobService
from src.database.engine import SessionMaker

from .worker import scheduler


async def check_sub_job():
    async with SessionMaker() as session:
        await SubscriptionJobService(session).expire_subscriptions_job()


async def check_sub_noti_job():
    async with SessionMaker() as session:
        await SubscriptionJobService(session).expire_subscriptions_notifications_job()
