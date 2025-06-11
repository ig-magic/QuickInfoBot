from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    RequestPeerTypeUser,
    RequestPeerTypeChannel,
    RequestPeerTypeChat
)
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "quickinfo",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode=ParseMode.MARKDOWN
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
                "👤 Premium Users",
                request_user=RequestPeerTypeUser(
                    button_id=3,
                    is_bot=False,
                    is_premium=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                "🌐 Public Channel",
                request_chat=RequestPeerTypeChannel(
                    button_id=5,
                    is_username=True,
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
                "🔒 Private Channel",
                request_chat=RequestPeerTypeChannel(
                    button_id=4,
                    is_username=False,
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
        "**👋 Welcome to Chat ID Finder Bot!** 🆔\n\n"
        "**✅ Fetch Any Chat ID Instantly!**\n\n"
        "🔧 **How to Use?**\n"
        "1️⃣ Click the buttons below to share a chat or user.\n"
        "2️⃣ Receive the unique ID instantly.\n\n"
        "💎 **Features:**\n"
        "- Supports users, bots, private/public groups & channels\n"
        "- Fast and reliable\n\n"
        "> 🛠 Made with ❤️ By @ItsSmartDev",
        reply_markup=menu_buttons
    )

@bot.on_message(filters.command("help"))
async def help_command(bot, message):
    await message.reply_text(
        "**🚀 Chat ID Finder Bot Help Center** 🌟\n\n"
        "🔍 **Need to grab a chat ID? We've got you covered!**\n\n"
        "📋 **Commands & Features:**\n"
        "👉 `/start` - Launch the bot and see the magic buttons! 🎮\n"
        "👉 `/help` - Show this awesome help message 📖\n"
        "👉 **Forward Messages** - Send any forwarded message to reveal its source ID! 🔎\n"
        "👉 **Buttons** - Pick from users, bots, groups, or channels to get IDs instantly ⚡\n\n"
        "💡 **Pro Tip:** Forward a message from any chat, and I'll dig up the details! 🕵️\n\n"
        "📩 **Got questions?** Ping @ItsSmartDev for support! 😎\n"
        "> 🛠 Crafted with ❤️ By @ItsSmartDev"
    )

@bot.on_message(filters.private & filters.forwarded)
async def handle_forwarded_message(bot, message):
    try:
        if hasattr(message, "forward_origin") and message.forward_origin:
            origin = message.forward_origin
            if hasattr(origin, "sender_user") and origin.sender_user:
                user = origin.sender_user
                user_id = user.id
                first_name = user.first_name
                last_name = user.last_name or ""
                username = f"@{user.username}" if user.username else "No username"
                user_type = "Bot" if user.username and user.username.lower().endswith("bot") else "User"
                await message.reply_text(
                    f"**Forwarded {user_type} Info**\n"
                    f"Type: `{user_type}`\n"
                    f"ID: `{user_id}`\n"
                    f"Name: `{first_name} {last_name}`\n"
                    f"Username: `{username}`"
                )
            elif hasattr(origin, "chat") and origin.chat:
                chat = origin.chat
                chat_id = chat.id
                chat_name = chat.title or "Unnamed Chat"
                chat_type = str(chat.type).replace("ChatType.", "").capitalize()
                username = f"@{chat.username}" if chat.username else "No username"
                await message.reply_text(
                    "**Forwarded Chat Info**\n"
                    f"Type: `{chat_type}`\n"
                    f"ID: `{chat_id}`\n"
                    f"Name: `{chat_name}`\n"
                    f"Username: `{username}`"
                )
            elif hasattr(origin, "sender_user_name") and origin.sender_user_name:
                await message.reply_text(
                    "**Looks Like I Don't Have Control Over The User**\n"
                    f"Forwarded from: `{origin.sender_user_name}`"
                )
            else:
                await message.reply_text(
                    "**Looks Like I Don't Have Control Over The User**"
                )
        else:
            await message.reply_text(
                "**Looks Like I Don't Have Control Over The User**"
            )
    except Exception:
        await message.reply_text(
            "**Looks Like I Don't Have Control Over The User**"
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
                    "**Shared Chat Info**\n"
                    f"Type: `{chat_type}`\n"
                    f"ID: `{chat_id}`\n"
                    f"Name: `{chat_name}`"
                )
        elif hasattr(message.chats_shared, "users") and message.chats_shared.users:
            for user in message.chats_shared.users:
                user_id = user.user_id
                first_name = user.first_name
                last_name = user.last_name or ""
                username = f"@{user.username}" if user.username else "No username"
                user_type = "Bot" if user.username and user.username.lower().endswith("bot") else "User"
                await message.reply_text(
                    f"**Shared {user_type} Info**\n"
                    f"ID: `{user_id}`\n"
                    f"Name: `{first_name} {last_name}`\n"
                    f"Username: `{username}`"
                )
    else:
        await message.reply_text(
            "**Please use the provided buttons to share a group, bot, channel, or user.**"
        )

if __name__ == "__main__":
    bot.run()
