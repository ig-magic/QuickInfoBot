"""
Author: Bisnu Ray
Telegram: https://t.me/SmartBisnuBio
"""

import logging
from telethon import TelegramClient, events, utils
from telethon.tl.types import (
    KeyboardButtonRequestPeer, ReplyKeyboardMarkup, KeyboardButtonRow,
    RequestPeerTypeUser, RequestPeerTypeChat, RequestPeerTypeBroadcast,
    UpdateNewMessage, MessageService,
    RequestedPeerUser, RequestedPeerChat, RequestedPeerChannel,
    PeerUser, PeerChat, PeerChannel, User, Chat, Channel,
    ChatAdminRights
)
from config import API_ID, API_HASH, BOT_TOKEN

TYPES = {
    1: {'name': '👤 User'},
    2: {'name': '🔒 Private Channel'},
    3: {'name': '🌐 Public Channel'},
    4: {'name': '🔒 Private Group'},
    5: {'name': '🌐 Public Group'},
    6: {'name': '🤖 Bot'},
    7: {'name': '🌟 Premium User'},
    8: {'name': '📢 Your Channel'},
    9: {'name': '👥 Your Group'},
    10: {'name': '📢 Channels You Admin'},
    11: {'name': '👥 Groups You Admin'}
}

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('error.log'),
        logging.StreamHandler()
    ]
)

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage)
async def handle_new_message(event):
    message = event.message
    chat_id = event.chat_id
    text = message.text
    sender = await event.get_sender()

    # Log every incoming message
    logging.info(f"Received NewMessage: text='{text}', chat_id={chat_id}, message={message}")

    if text == '/start':
        logging.info("Processing /start command")
        welcome_text = (
            "👋 <b>Welcome to Chat ID Finder Bot!</b> 🆔\n\n"
            "✅ <b>Fetch Any Chat ID Instantly!</b>\n\n"
            "🔧 <b>How to Use?</b>\n"
            "1️⃣ Click the buttons below to share a chat or user.\n"
            "2️⃣ Receive the unique ID instantly.\n\n"
            "💎 <b>Features:</b>\n"
            "✅ Supports users, bots, groups & channels\n"
            "⚡ Fast and reliable\n\n"
            "<blockquote>🛠 Made with ❤️ by @ItsSmartDev</blockquote>"
        )

        keyboard = [
            [
                KeyboardButtonRequestPeer(
                    text='👤 User',
                    button_id=1,
                    peer_type=RequestPeerTypeUser(bot=False),
                    max_quantity=1
                ),
                KeyboardButtonRequestPeer(
                    text='🤖 Bot',
                    button_id=6,
                    peer_type=RequestPeerTypeUser(bot=True),
                    max_quantity=1
                )
            ],
            [
                KeyboardButtonRequestPeer(
                    text='🔒 Private Channel',
                    button_id=2,
                    peer_type=RequestPeerTypeBroadcast(has_username=False),
                    max_quantity=1
                ),
                KeyboardButtonRequestPeer(
                    text='🌐 Public Channel',
                    button_id=3,
                    peer_type=RequestPeerTypeBroadcast(has_username=True),
                    max_quantity=1
                )
            ],
            [
                KeyboardButtonRequestPeer(
                    text='🔒 Private Group',
                    button_id=4,
                    peer_type=RequestPeerTypeChat(has_username=False),
                    max_quantity=1
                ),
                KeyboardButtonRequestPeer(
                    text='🌐 Public Group',
                    button_id=5,
                    peer_type=RequestPeerTypeChat(has_username=True),
                    max_quantity=1
                )
            ],
            [
                KeyboardButtonRequestPeer(
                    text='🌟 Premium User',
                    button_id=7,
                    peer_type=RequestPeerTypeUser(premium=True),
                    max_quantity=1
                )
            ]
        ]

        reply_markup = ReplyKeyboardMarkup(
            rows=[KeyboardButtonRow(buttons=row) for row in keyboard],
            resize=True,
            single_use=False
        )

        try:
            await client.send_message(
                chat_id,
                welcome_text,
                parse_mode='html',
                link_preview=False,
                buttons=reply_markup
            )
            logging.info("Sent welcome message with keyboard")
        except Exception as e:
            logging.error(f"Failed to send welcome message: {str(e)}")
            await client.send_message(
                chat_id,
                welcome_text,
                parse_mode='html',
                link_preview=False,
                buttons=reply_markup
            )
            logging.info("Retried welcome message")

    elif text == '/me':
        logging.info("Processing /me command")
        response = f"👤 <b>Your Info</b>\n🆔 ID: <code>{sender.id}</code>"
        try:
            await client.send_message(
                chat_id,
                response,
                parse_mode='html'
            )
            logging.info(f"Sent /me response: {response}")
        except Exception as e:
            logging.error(f"Failed to send /me response: {str(e)}")

    elif text == '/my':
        logging.info("Processing /my command")
        keyboard = [
            [
                KeyboardButtonRequestPeer(
                    text='📢 Your Channel',
                    button_id=8,
                    peer_type=RequestPeerTypeBroadcast(creator=True),
                    max_quantity=1
                ),
                KeyboardButtonRequestPeer(
                    text='👥 Your Group',
                    button_id=9,
                    peer_type=RequestPeerTypeChat(creator=True),
                    max_quantity=1
                )
            ]
        ]

        reply_markup = ReplyKeyboardMarkup(
            rows=[KeyboardButtonRow(buttons=row) for row in keyboard],
            resize=True,
            single_use=False
        )

        try:
            await client.send_message(
                chat_id,
                "Please select a channel or group where you are the owner:",
                parse_mode='html',
                link_preview=False,
                buttons=reply_markup
            )
            logging.info("Sent /my message with keyboard")
        except Exception as e:
            logging.error(f"Failed to send /my message: {str(e)}")

    elif text == '/admins':
        logging.info("Processing /admins command")
        keyboard = [
            [
                KeyboardButtonRequestPeer(
                    text='📢 Channels You Admin',
                    button_id=10,
                    peer_type=RequestPeerTypeBroadcast(user_admin_rights=ChatAdminRights(change_info=True)),
                    max_quantity=1
                ),
                KeyboardButtonRequestPeer(
                    text='👥 Groups You Admin',
                    button_id=11,
                    peer_type=RequestPeerTypeChat(user_admin_rights=ChatAdminRights(change_info=True)),
                    max_quantity=1
                )
            ]
        ]

        reply_markup = ReplyKeyboardMarkup(
            rows=[KeyboardButtonRow(buttons=row) for row in keyboard],
            resize=True,
            single_use=False
        )

        try:
            await client.send_message(
                chat_id,
                "Please select a channel or group where you are an admin:",
                parse_mode='html',
                link_preview=False,
                buttons=reply_markup
            )
            logging.info("Sent /admins message with keyboard")
        except Exception as e:
            logging.error(f"Failed to send /admins message: {str(e)}")

    elif text == '/help':
        logging.info("Processing /help command")
        help_text = (
            "<b>Available Commands:</b>\n\n"
            "<b>/start</b> - Start the bot and get the main menu with options to fetch IDs.\n"
            "<b>/me</b> - Get your own Telegram user ID.\n"
            "<b>/my</b> - View your owned channels and groups.\n"
            "<b>/admins</b> - View channels and groups where you are an admin.\n"
            "<b>/help</b> - Show this help message with command explanations."
        )
        try:
            await client.send_message(
                chat_id,
                help_text,
                parse_mode='html'
            )
            logging.info("Sent /help message")
        except Exception as e:
            logging.error(f"Failed to send /help message: {str(e)}")

    elif message.forward is not None:
        peer = message.forward.saved_from_peer or message.forward.from_id
        if peer:
            chat_id_forwarded = utils.get_peer_id(peer)
            try:
                entity = await client.get_entity(peer)
                if isinstance(entity, User):
                    chat_name = entity.first_name or "User"
                elif isinstance(entity, (Chat, Channel)):
                    chat_name = entity.title
                else:
                    chat_name = "Unknown"
                response = (
                    f"<b>Forward Message Detected</b>\n"
                    f"<b>Chat Name {chat_name}</b>\n"
                    f"<b>ChatID {chat_id_forwarded}</b>"
                )
                try:
                    await client.send_message(
                        chat_id,
                        response,
                        parse_mode='html'
                    )
                    logging.info(f"Sent forwarded message response: {response}")
                except Exception as e:
                    logging.error(f"Failed to send forwarded message response: {str(e)}")
                    await client.send_message(
                        chat_id,
                        response,
                        parse_mode='html'
                    )
                    logging.info("Retried forwarded message response")
            except ValueError:
                response = "❌ <b>Sorry, Forward Method Not Supported For Private Chats</b>"
                await client.send_message(chat_id, response, parse_mode='html')
                logging.info(f"Sent response: {response}")
        else:
            logging.info("Forwarded message but no peer found")

@client.on(events.Raw)
async def handle_raw_update(update):
    logging.info(f"Received raw update: {update}")

    if isinstance(update, UpdateNewMessage) and isinstance(update.message, MessageService):
        message = update.message
        chat_id = message.peer_id.user_id if hasattr(message.peer_id, 'user_id') else message.peer_id.chat_id
        logging.info(f"Service message detected: {message}")

        if hasattr(message.action, 'button_id') and hasattr(message.action, 'peers'):
            logging.info("Detected peer sharing action")
            button_id = message.action.button_id
            peers = message.action.peers

            type_info = TYPES.get(button_id, {'name': 'Unknown'})
            type_ = type_info['name']

            if peers:
                for peer in peers:
                    logging.info(f"Processing shared peer: {peer}")
                    try:
                        if isinstance(peer, RequestedPeerUser):
                            user_id = peer.user_id
                            response = f"👤 <b>Shared {type_} Info</b>\n🆔 ID: <code>{user_id}</code>"
                        elif isinstance(peer, RequestedPeerChat):
                            chat_id_shared = -peer.chat_id
                            response = f"💬 <b>Shared {type_} Info</b>\n🆔 ID: <code>{chat_id_shared}</code>"
                        elif isinstance(peer, RequestedPeerChannel):
                            channel_id = -1000000000000 - peer.channel_id
                            response = f"💬 <b>Shared {type_} Info</b>\n🆔 ID: <code>{channel_id}</code>"
                        else:
                            response = "Looks Like I Don't Have Control Over The User"
                            logging.warning("Unknown peer type encountered")

                        try:
                            await client.send_message(
                                chat_id,
                                response,
                                parse_mode='html'
                            )
                            logging.info(f"Sent response: {response}")
                        except Exception as e:
                            logging.error(f"Failed to send peer sharing response: {str(e)}")
                            await client.send_message(
                                chat_id,
                                response,
                                parse_mode='html'
                            )
                            logging.info("Retried peer sharing response: {response}")
                    except Exception as e:
                        logging.error(f"Error processing peer: {str(e)}")
                        response = "❌ Error fetching entity"
                        await client.send_message(chat_id, response, parse_mode='html')
            else:
                logging.warning("No peers found in the action")
        else:
            logging.info("Service message is not a peer sharing event")

print("✅ Bot Is Up And Running On Telethon")
client.run_until_disconnected()
