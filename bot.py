# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client
from pyrogram.enums import ParseMode
from utils import LOGGER
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN
)

LOGGER.info("Creating Bot Client From BOT_TOKEN")

bot = Client(
    "QuickInfoBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=1000,
    parse_mode=ParseMode.MARKDOWN
)

LOGGER.info("Bot Client Created Successfully!")
