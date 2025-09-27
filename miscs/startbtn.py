# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    RequestPeerTypeUser,
    RequestPeerTypeChannel,
    RequestPeerTypeChat,
    ChatPrivileges
)
from utils import LOGGER

menu_buttons = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(
                "👤 User Info",
                request_user=RequestPeerTypeUser(
                    button_id=1,
                    is_bot=False,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                "👥 Public Group",
                request_chat=RequestPeerTypeChat(
                    button_id=7,
                    is_username=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            ),
            KeyboardButton(
                "🔒 Private Group",
                request_chat=RequestPeerTypeChat(
                    button_id=6,
                    is_username=False,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                "📢 Public Channel",
                request_chat=RequestPeerTypeChannel(
                    button_id=5,
                    is_username=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            ),
            KeyboardButton(
                "🔒 Private Channel",
                request_chat=RequestPeerTypeChannel(
                    button_id=4,
                    is_username=False,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                "🤖 Bot",
                request_user=RequestPeerTypeUser(
                    button_id=2,
                    is_bot=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            ),
            KeyboardButton(
                "🌟 Premium Users",
                request_user=RequestPeerTypeUser(
                    button_id=3,
                    is_bot=False,
                    is_premium=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                "👥 Your Group",
                request_chat=RequestPeerTypeChat(
                    button_id=8,
                    is_creator=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            ),
            KeyboardButton(
                "📢 Your Channel",
                request_chat=RequestPeerTypeChannel(
                    button_id=9,
                    is_creator=True,
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            )
        ],
        [
            KeyboardButton(
                "👥 Admin",
                request_chat=RequestPeerTypeChat(
                    button_id=11,
                    user_privileges=ChatPrivileges(
                        can_manage_chat=True,
                        can_delete_messages=True,
                        can_manage_video_chats=True,
                        can_restrict_members=True,
                        can_promote_members=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                        can_manage_topics=True
                    ),
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            ),
            KeyboardButton(
                "📢 Channel Admin",
                request_chat=RequestPeerTypeChannel(
                    button_id=10,
                    user_privileges=ChatPrivileges(
                        can_manage_chat=True,
                        can_delete_messages=True,
                        can_manage_video_chats=True,
                        can_restrict_members=True,
                        can_promote_members=True,
                        can_change_info=True,
                        can_post_messages=True,
                        can_edit_messages=True,
                        can_invite_users=True,
                        can_pin_messages=True,
                        can_manage_topics=True,
                        can_post_stories=True,
                        can_edit_stories=True,
                        can_delete_stories=True
                    ),
                    max=1,
                    is_name_requested=True,
                    is_username_requested=True,
                    is_photo_requested=True
                )
            )
        ]
    ],
    resize_keyboard=True,
    placeholder="Choose a chat type"
)

LOGGER.info("Menu buttons initialized")
