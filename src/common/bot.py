import config

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

BOT_TOKEN: str = config.BOT_TOKEN


BOT = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
