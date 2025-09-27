# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import LOGGER
from bot import bot
from config import COMMAND_PREFIX,ADMIN_ID

HELP_TEXT = (
    "**Here Are QuickInfo Bot Options 👇:**\n\n"
)

FORWARD_TEXT = (
    "**Forward Message Tutorial 📬**\n\n"
    "🔎 Want to grab the ID of a user or chat? Just forward a message to me! Here’s how:\n\n"
    "1️⃣ Find a message in any chat (user, group, channel, or bot).\n"
    "2️⃣ Forward it to me privately.\n"
    "3️⃣ I’ll instantly reveal the ID, name, and more! ⚡\n\n"
    "💡 **Pro Tip:** Works with any forwarded message, even from private chats! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)

GETME_TEXT = (
    "**Get Me Tutorial 🙋‍♂️**\n\n"
    "🔍 Want to know your own Telegram ID? It’s super easy!\n\n"
    "1️⃣ Just type `/me` in the chat with me.\n"
    "2️⃣ I’ll send your user ID, name, and username instantly! ⚡\n"
    "3️⃣ If you have a profile photo, I’ll show it too! 📸\n\n"
    "💡 **Pro Tip:** Use the button in the reply to copy your ID! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)

SHAREDCHAT_TEXT = (
    "**Shared Chat Tutorial 🌐**\n\n"
    "🔎 Need the ID of a user, group, or channel? Share it with me!\n\n"
    "1️⃣ Type `/start` to see the sharing buttons.\n"
    "2️⃣ Pick a user, bot, group, or channel to share.\n"
    "3️⃣ I’ll fetch the ID, name, and username instantly! ⚡\n\n"
    "💡 **Pro Tip:** Works for public and private chats, plus bots and premium users! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)

ADMINS_TEXT = (
    "**Admins Tutorial 🛡️**\n\n"
    "🔍 Want to see where you’re an admin? I’ve got you!\n\n"
    "1️⃣ Type `/admin` in the chat with me.\n"
    "2️⃣ Use the buttons to share a channel or group where you have admin rights.\n"
    "3️⃣ I’ll reveal the ID and details instantly! ⚡\n\n"
    "💡 **Pro Tip:** Perfect for managing your admin roles! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)

OWNCHATS_TEXT = (
    "**Own Chats Tutorial 📚**\n\n"
    "🔎 Curious about your own channels or groups? Let’s find them!\n\n"
    "1️⃣ Type `/my` in the chat with me.\n"
    "2️⃣ Use the buttons to share a channel or group you own.\n"
    "3️⃣ I’ll send the ID and details in a snap! ⚡\n\n"
    "💡 **Pro Tip:** Great for keeping track of your own chats! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)

USERNAME_TEXT = (
    "**Username Tutorial 👤**\n\n"
    "🔎 Want info about a specific user? Just send me their username!\n\n"
    "1️⃣ Type a username (e.g., `@username`) in the chat with me.\n"
    "2️⃣ I’ll fetch their ID, name, and other details instantly! ⚡\n"
    "3️⃣ If they have a profile photo, I’ll show it too! 📸\n\n"
    "💡 **Pro Tip:** Works for any public username, even bots! 😎\n\n"
    "> 🛠 Crafted with ❤️ By @itsSmartDev"
)

MAIN_MENU_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📬 Forward", callback_data="help_forward"),
            InlineKeyboardButton("🙋‍♂️ Get Me", callback_data="help_getme")
        ],
        [
            InlineKeyboardButton("🌐 Shared Chat", callback_data="help_sharedchat"),
            InlineKeyboardButton("🛡️ Admins", callback_data="help_admins")
        ],
        [
            InlineKeyboardButton("📚 Own Chats", callback_data="help_ownchats"),
            InlineKeyboardButton("Close ❌", callback_data="help_close")
        ],
        [
            InlineKeyboardButton("👤 Username", callback_data="help_username"),
            InlineKeyboardButton("🔧 Dev", user_id=ADMIN_ID)
        ],
        [
            InlineKeyboardButton("🔔 Join For Updates", url="https://t.me/itsSmartDev")
        ]
    ]
)

BACK_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Back", callback_data="main_menu")
        ]
    ]
)

CALLBACK_TEXTS = {
    "help_forward": FORWARD_TEXT,
    "help_getme": GETME_TEXT,
    "help_sharedchat": SHAREDCHAT_TEXT,
    "help_admins": ADMINS_TEXT,
    "help_ownchats": OWNCHATS_TEXT,
    "help_username": USERNAME_TEXT
}

@bot.on_message(filters.command("help", prefixes=COMMAND_PREFIX.split("|")))
async def help_command(bot: Client, message):
    LOGGER.info(f"Help command received for user {message.from_user.id}")
    await message.reply_text(HELP_TEXT, reply_markup=MAIN_MENU_BUTTONS)

@bot.on_callback_query(filters.regex(r"^(help_forward|help_getme|help_sharedchat|help_admins|help_ownchats|help_username|help_close|main_menu)$"))
async def handle_help_callback(bot: Client, callback_query):
    callback_data = callback_query.data
    user_id = callback_query.from_user.id
    LOGGER.info(f"Callback {callback_data} received from user {user_id}")
    if callback_data == "help_close":
        try:
            await callback_query.message.delete()
            LOGGER.info(f"Help message deleted for user {user_id}")
        except Exception as e:
            LOGGER.error(f"Failed to delete help message for user {user_id}: {e}")
            await callback_query.message.edit_text(
                f"{HELP_TEXT}\n\n**Oops!** Couldn’t close the menu, but you can still pick an option! 😅",
                reply_markup=MAIN_MENU_BUTTONS
            )
    elif callback_data == "main_menu":
        await callback_query.message.edit_text(HELP_TEXT, reply_markup=MAIN_MENU_BUTTONS)
    else:
        await callback_query.message.edit_text(CALLBACK_TEXTS[callback_data], reply_markup=BACK_BUTTON)
