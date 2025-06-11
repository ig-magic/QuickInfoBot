"""
Author: Bisnu Ray
Telegram: https://t.me/SmartBisnuBio
"""

from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    RequestPeerTypeChat,
    RequestPeerTypeUser,
    RequestPeerTypeChannel
)

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN
)

bot = Client(
    "quickinfo",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.HTML
)

menu_buttons = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(
                "👤 Users",
                request_user=RequestPeerTypeUser(
                    button_id=1,
                    is_bot=False,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            ),
            KeyboardButton(
                "🤖 Bots",
                request_user=RequestPeerTypeUser(
                    button_id=2,
                    is_bot=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            ),
            KeyboardButton(
                "🔒 Private Channel",
                request_chat=RequestPeerTypeChannel(
                    button_id=4,
                    is_username=False,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                " 🌐Public Channel",
                request_chat=RequestPeerTypeChannel(
                    button_id=5,
                    is_username=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            ),
            KeyboardButton(
                "🔒 Private Group",
                request_chat=RequestPeerTypeChat(
                    button_id=6,
                    is_username=False,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            ),
            KeyboardButton(
                "🌐 Public Group",
                request_chat=RequestPeerTypeChat(
                    button_id=7,
                    is_username=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                "👥 Your Groups",
                request_chat=RequestPeerTypeChat(
                    button_id=8,
                    is_creator=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            ),
            KeyboardButton(
                "🌟 Your Channels",
                request_chat=RequestPeerTypeChannel(
                    button_id=9,
                    is_creator=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            )
        ]
    ],
    resize_keyboard=True
)

@bot.on_message(filters.command("start"))
async def start(bot, message):
    await message.reply_text(
        "👋 <b>Welcome to Chat ID Finder Bot!</b> 🆔\n\n"
        "✅ <b>Fetch Any Chat ID Instantly!</b>\n\n"
        "🔧 <b>How to Use?</b>\n"
        "1️⃣ Click the buttons below to share a chat or user.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "💎 <b>Features:</b>\n"
        "✅ Supports users, bots, private/public groups & channels\n"
        "⚡ Fast and reliable\n\n"
        "<blockquote>🛠 Made with ❤️ By @ItsSmartDev</blockquote>",
        reply_markup=menu_buttons
    )

@bot.on_message(filters.command("help"))
async def help_command(bot, message):
    await message.reply_text(
        "🚀 <b>Chat ID Finder Bot Help Center</b> 🌟\n\n"
        "🔍 <b>Need to grab a chat ID? We've got you covered!</b>\n\n"
        "📋 <b>Commands & Features:</b>\n"
        "👉 <code>/start</code> - Launch the bot and see the magic buttons! 🎮\n"
        "👉 <code>/help</code> - Show this awesome help message 📖\n"
        "👉 <b>Forward Messages</b> - Send any forwarded message to reveal its source ID! 🔎\n"
        "👉 <b>Buttons</b> - Pick from users, bots, groups, or channels to get IDs instantly ⚡\n\n"
        "💡 <b>Pro Tip:</b> Forward a message from any chat, and I'll dig up the details! 🕵️\n\n"
        "📩 <b>Got questions?</b> Ping @ItsSmartDev for support! 😎\n"
        "<blockquote>🛠 Crafted with ❤️ By @ItsSmartDev</blockquote>"
    )

@bot.on_message(filters.private & filters.forwarded)
async def handle_forwarded_message(bot, message):
    try:
        if hasattr(message, "forward_origin") and message.forward_origin:
            origin = message.forward_origin
            if hasattr(origin, "sender_user") and origin.sender_user:
                # Forwarded from a user or bot
                user = origin.sender_user
                user_id = user.id
                first_name = user.first_name
                last_name = user.last_name or ""
                username = f"@{user.username}" if user.username else "No username"
                user_type = "Bot" if user.username and user.username.lower().endswith("bot") else "User"
                await message.reply_text(
                    f"<b>Forwarded {user_type} Info</b>\n"
                    f"Type: <code>{user_type}</code>\n"
                    f"ID: <code>{user_id}</code>\n"
                    f"Name: <code>{first_name} {last_name}</code>\n"
                    f"Username: <code>{username}</code>"
                )
            elif hasattr(origin, "chat") and origin.chat:
                # Forwarded from a group or channel
                chat = origin.chat
                chat_id = chat.id
                chat_name = chat.title or "Unnamed Chat"
                chat_type = str(chat.type).replace("ChatType.", "").capitalize()
                username = f"@{chat.username}" if chat.username else "No username"
                await message.reply_text(
                    f"<b>Forwarded Chat Info</b>\n"
                    f"Type: <code>{chat_type}</code>\n"
                    f"ID: <code>{chat_id}</code>\n"
                    f"Name: <code>{chat_name}</code>\n"
                    f"Username: <code>{username}</code>"
                )
            elif hasattr(origin, "sender_user_name") and origin.sender_user_name:
                # Forwarded from a user with hidden profile
                await message.reply_text(
                    f"<b>Looks Like I Don't Have Control Over The User</b>\n"
                    f"Forwarded from: <code>{origin.sender_user_name}</code>"
                )
            else:
                # No forward info available
                await message.reply_text(
                    "<b>Looks Like I Don't Have Control Over The User</b>"
                )
        else:
            # No forward info available
            await message.reply_text(
                "<b>Looks Like I Don't Have Control Over The User</b>"
            )
    except Exception:
        # Catch any unexpected errors (e.g., API restrictions)
        await message.reply_text(
            "<b>Looks Like I Don't Have Control Over The User</b>"
        )

@bot.on_message(filters.private)
async def handle_message(bot, message):
    if getattr(message, "chats_shared", None):
        if hasattr(message.chats_shared, "chats") and message.chats_shared.chats:
            for chat in message.chats_shared.chats:
                chat_id = chat.chat_id
                chat_name = chat.name
                chat_type = str(chat.chat_type).replace("ChatType.", "").capitalize()
                await message.reply_text(
                    f"<b>Shared Chat Info</b>\n"
                    f"Type: <code>{chat_type}</code>\n"
                    f"ID: <code>{chat_id}</code>\n"
                    f"Name: <code>{chat_name}</code>"
                )
        elif hasattr(message.chats_shared, "users") and message.chats_shared.users:
            for user in message.chats_shared.users:
                user_id = user.user_id
                first_name = user.first_name
                last_name = user.last_name or ""
                username = f"@{user.username}" if user.username else "No username"
                if user.username and user.username.lower().endswith("bot"):
                    user_type = "Bot"
                else:
                    user_type = "User"
                await message.reply_text(
                    f"<b>Shared {user_type} Info</b>\n"
                    f"ID: <code>{user_id}</code>\n"
                    f"Name: <code>{first_name} {last_name}</code>\n"
                    f"Username: <code>{username}</code>"
                )
    else:
        await message.reply_text("<b>Please use the provided buttons to share a group, bot, channel, or user.</b>")

if __name__ == "__main__":
    bot.run()
