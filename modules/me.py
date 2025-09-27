# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMediaAnimation
from pyrogram.enums import ChatType, UserStatus
from utils import LOGGER
from bot import bot
from config import COMMAND_PREFIX
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def calculate_account_age(creation_date):
    today = datetime.now()
    delta = relativedelta(today, creation_date)
    years = delta.years
    months = delta.months
    days = delta.days
    return f"{years} years, {months} months, {days} days"

def estimate_account_creation_date(user_id):
    reference_points = [
        (100000000, datetime(2013, 8, 1)),
        (1273841502, datetime(2020, 8, 13)),
        (1500000000, datetime(2021, 5, 1)),
        (2000000000, datetime(2022, 12, 1)),
    ]
    closest_point = min(reference_points, key=lambda x: abs(x[0] - user_id))
    closest_user_id, closest_date = closest_point
    id_difference = user_id - closest_user_id
    days_difference = id_difference / 20000000
    creation_date = closest_date + timedelta(days=days_difference)
    return creation_date

def get_status_display(status):
    if not status:
        return "Unknown"
    status_map = {
        UserStatus.ONLINE: "Online",
        UserStatus.OFFLINE: "Offline",
        UserStatus.RECENTLY: "Recently",
        UserStatus.LAST_WEEK: "Last Week",
        UserStatus.LAST_MONTH: "Last Month",
        UserStatus.LONG_AGO: "Long Ago"
    }
    return status_map.get(status, "Unknown")

def get_dc_location(dc_id):
    dc_locations = {
        1: "MIA, Miami, USA, US",
        2: "AMS, Amsterdam, Netherlands, NL",
        3: "MBA, Mumbai, India, IN",
        4: "STO, Stockholm, Sweden, SE",
        5: "SIN, Singapore, SG",
        6: "LHR, London, United Kingdom, GB",
        7: "FRA, Frankfurt, Germany, DE",
        8: "JFK, New York, USA, US",
        9: "HKG, Hong Kong, HK",
        10: "TYO, Tokyo, Japan, JP",
        11: "SYD, Sydney, Australia, AU",
        12: "GRU, São Paulo, Brazil, BR",
        13: "DXB, Dubai, UAE, AE",
        14: "CDG, Paris, France, FR",
        15: "ICN, Seoul, South Korea, KR",
    }
    return dc_locations.get(dc_id, "Unknown")

async def get_profile_photo_file_id(client, entity_id):
    try:
        async for photo in client.get_chat_photos(entity_id, limit=1):
            if hasattr(photo, 'video_sizes') and photo.video_sizes:
                return photo.file_id, True
            return photo.file_id, False
    except Exception as e:
        LOGGER.error(f"Error getting chat photos: {str(e)}")
    return None, False

def format_user_response(user):
    premium_status = "Yes" if user.is_premium else "No"
    dc_id = getattr(user, 'dc_id', 0)
    dc_location = get_dc_location(dc_id)
    account_created = estimate_account_creation_date(user.id)
    account_created_str = account_created.strftime("%B %d, %Y")
    account_age = calculate_account_age(account_created)
    first_name = getattr(user, 'first_name', 'Unknown')
    last_name = getattr(user, 'last_name', None)
    full_name = first_name if last_name is None else f"{first_name} {last_name}".strip()
    profile_type = "Bot's Profile Info" if user.is_bot else "User's Profile Info"
    response = (
        f"**🔍 Showing {profile_type} 📋**\n"
        "━━━━━━━━━━━━━━━━\n"
        f"**Full Name:** {full_name}\n"
    )
    if user.username:
        response += f"**Username:** @{user.username}\n"
    response += f"**User ID:** `{user.id}`\n"
    if not user.is_bot:
        response += f"**Premium User:** {premium_status}\n"
    response += f"**Data Center:** {dc_location}\n"
    if not user.is_bot:
        response += (
            f"**Created On:** {account_created_str}\n"
            f"**Account Age:** {account_age}\n"
        )
    if hasattr(user, 'usernames') and user.usernames:
        fragment_usernames = ", ".join([f"@{username.username}" for username in user.usernames])
        response += f"**Fragment Usernames:** {fragment_usernames}\n"
    restricted = getattr(user, 'is_restricted', False)
    response += f"**Account Frozen:** {'Yes' if restricted else 'No'}\n"
    if not user.is_bot and hasattr(user, 'status'):
        status_display = get_status_display(user.status)
        response += f"**Last Seen:** {status_display}\n"
    if getattr(user, 'is_support', False):
        response += f"**Telegram Staff:** Yes\n"
    response += (
        f"**Permanent Link:** [Click Here](tg://user?id={user.id})\n"
        "━━━━━━━━━━━━━━━━\n"
        "**👁 Thank You for Using Our Tool ✅**"
    )
    return response, full_name

@bot.on_message(filters.command("me", prefixes=COMMAND_PREFIX.split("|")))
async def me_command(bot: Client, message):
    LOGGER.info(f"Me command received for user {message.from_user.id}")
    loading_message = await message.reply_text("`Processing Your Info...`")
    try:
        user = message.from_user
        response, full_name = format_user_response(user)
        buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text=full_name, copy_text=str(user.id))]]
        )
        try:
            photo_file_id, is_animated = await get_profile_photo_file_id(bot, user.id)
            if photo_file_id:
                if is_animated:
                    await loading_message.edit_media(
                        media=InputMediaAnimation(
                            media=photo_file_id,
                            caption=response
                        ),
                        reply_markup=buttons
                    )
                else:
                    await loading_message.edit_media(
                        media=InputMediaPhoto(
                            media=photo_file_id,
                            caption=response
                        ),
                        reply_markup=buttons
                    )
                LOGGER.info(f"Sent user info with photo for user {user.id}")
            else:
                await loading_message.edit_text(response, reply_markup=buttons)
                LOGGER.info(f"Sent user info without photo for user {user.id}")
        except Exception as e:
            LOGGER.error(f"Error sending user info with photo for user {user.id}: {e}")
            await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")
    except Exception as e:
        LOGGER.error(f"Error processing me command for user {message.from_user.id}: {e}")
        await loading_message.edit_text("**Looks Like I Don't Have Control Over The User**")