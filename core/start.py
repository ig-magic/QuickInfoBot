# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from utils import LOGGER
from miscs.startbtn import menu_buttons
from bot import bot
from config import COMMAND_PREFIX

@bot.on_message(filters.command("start", prefixes=COMMAND_PREFIX.split("|")))
async def start(bot: Client, message):
    LOGGER.info("Start command received")
    await message.reply_text(
        "**👋 Welcome to Quick Info Bot!** 🆔\n\n"
        "**✅ Fetch Any Chat ID Instantly!**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a chat or user.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "💎 **Features:**\n"
        "- Supports users, bots, private/public groups & channels\n"
        "- Fast and reliable\n\n"
        "> 🛠 Made with ❤️ By @itsSmartDev",
        reply_markup=menu_buttons
    )
