# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineKeyboardButtonBuy, LabeledPrice
from pyrogram.enums import ParseMode
from utils import LOGGER
from bot import bot
from config import COMMAND_PREFIX, ADMIN_ID
import uuid
import time
import asyncio

DONATION_OPTIONS_TEXT = """
**Why support Quick Info Bot?**
**━━━━━━━━━━━━━━━━━━**
🌟 **Love the service?**
Your support helps keep **Quick Info Bot** fast, reliable, and free for everyone.
Even a small **Gift or Donation** makes a big difference! 💖

👇 **Choose an amount to contribute:**

**Why contribute?**
More support = more motivation
More motivation = better tools
Better tools = more productivity
More productivity = less wasted time
Less wasted time = more done with **Quick Info Bot** 💡
**More Muhahaha… 🤓🔥**
"""

PAYMENT_SUCCESS_TEXT = """
**✅ Donation Successful!**

🎉 Huge thanks **{0}** for donating **{1}** ⭐️ to support **Quick Info Bot!**
Your contribution helps keep everything running smooth and awesome 🚀

**🧾 Transaction ID:** `{2}`
"""

ADMIN_NOTIFICATION_TEXT = """
**Hey New Donation Received 🤗**
**━━━━━━━━━━━━━━━**
**From: ** {0}
**Username:** {2}
**UserID:** `{1}`
**Amount:** {3} ⭐️
**Transaction ID:** `{4}`
**━━━━━━━━━━━━━━━**
**Click Below Button If Need Refund 💸**
"""

INVOICE_CREATION_TEXT = "Generating invoice for {0} Stars...\nPlease wait ⏳"
INVOICE_CONFIRMATION_TEXT = "**✅ Invoice for {0} Stars has been generated! You can now proceed to pay via the button below.**"
DUPLICATE_INVOICE_TEXT = "**🚫 Wait Bro! Contribution Already in Progress!**"
INVALID_INPUT_TEXT = "**❌ Sorry Bro! Invalid Input! Use a positive number.**"
INVOICE_FAILED_TEXT = "**❌ Invoice Creation Failed, Bruh! Try Again!**"
PAYMENT_FAILED_TEXT = "**❌ Sorry Bro! Payment Declined! Contact Support!**"
REFUND_SUCCESS_TEXT = "**✅ Refund Successfully Completed Bro!**\n\n**{0} Stars** have been refunded to **[{1}](tg://user?id={2})**"
REFUND_FAILED_TEXT = "**❌ Refund Failed!**\n\nFailed to refund **{0} Stars** to **{1}** (ID: `{2}`)\nError: {3}"

active_invoices = {}
payment_data = {}

def get_donation_buttons(amount: int = 5):
    if amount == 5:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{amount} ⭐️", callback_data=f"gift_{amount}"),
             InlineKeyboardButton("+5", callback_data=f"increment_gift_{amount}")]
        ])
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("-5", callback_data=f"decrement_gift_{amount}"),
         InlineKeyboardButton(f"{amount} ⭐️", callback_data=f"gift_{amount}"),
         InlineKeyboardButton("+5", callback_data=f"increment_gift_{amount}")]
    ])

@bot.on_message(filters.command(["donate", "gift"], prefixes=COMMAND_PREFIX.split("|")))
async def donate_command(client: Client, message):
    user_id = message.from_user.id
    LOGGER.info(f"Donation command received: user: {user_id}, chat: {message.chat.id}")
    try:
        command_parts = message.text.split()
        if len(command_parts) == 1:
            reply_markup = get_donation_buttons()
            await message.reply_text(
                text=DONATION_OPTIONS_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            LOGGER.info(f"Successfully sent donation options to chat {message.chat.id}")
        elif len(command_parts) == 2 and command_parts[1].isdigit() and int(command_parts[1]) > 0:
            amount = int(command_parts[1])
            loading_message = await message.reply_text(
                text=INVOICE_CREATION_TEXT.format(amount),
                parse_mode=ParseMode.MARKDOWN
            )
            await generate_invoice(message.chat.id, user_id, amount, client, loading_message.id)
        else:
            await message.reply_text(
                text=INVALID_INPUT_TEXT,
                parse_mode=ParseMode.MARKDOWN
            )
            LOGGER.warning(f"Invalid donation amount provided by user: {user_id}")
    except Exception as e:
        LOGGER.error(f"Error processing /donate command in chat {message.chat.id}: {e}")
        await message.reply_text(
            text="**❌ Sorry Bro! Donation System Error**",
            parse_mode=ParseMode.MARKDOWN
        )

async def generate_invoice(chat_id: int, user_id: int, amount: int, client: Client, message_id: int):
    if active_invoices.get(user_id):
        await client.send_message(chat_id, DUPLICATE_INVOICE_TEXT, parse_mode=ParseMode.MARKDOWN)
        return
    back_button = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="show_donate_options")]])
    try:
        active_invoices[user_id] = True
        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        invoice_payload = f"contribution_{user_id}_{amount}_{timestamp}_{unique_id}"
        title = "Support Quick Info Bot"
        description = f"Contribute {amount} Stars to support ongoing development and keep the tools free, fast, and reliable for everyone 💫 Every star helps us grow!"
        currency = "XTR"
        prices = [LabeledPrice(label=f"⭐️ {amount} Stars", amount=amount)]
        pay_button = InlineKeyboardMarkup([[InlineKeyboardButtonBuy("💫 Donate Via Stars")]])
        await client.send_invoice(
            chat_id=chat_id,
            title=title,
            description=description,
            payload=invoice_payload,
            currency=currency,
            prices=prices,
            start_parameter="donate-stars-to-quickinfobot",
            reply_markup=pay_button
        )
        await client.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=INVOICE_CONFIRMATION_TEXT.format(amount),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=back_button
        )
        LOGGER.info(f"✅ Invoice sent for {amount} stars to user {user_id} with payload {invoice_payload}")
    except Exception as e:
        LOGGER.error(f"❌ Failed to generate invoice for user {user_id}: {str(e)}")
        try:
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=INVOICE_FAILED_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=back_button
            )
        except Exception as edit_e:
            LOGGER.error(f"Failed to edit message in chat {chat_id}: {str(edit_e)}")
            await client.send_message(
                chat_id=chat_id,
                text=INVOICE_FAILED_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=back_button
            )
    finally:
        active_invoices.pop(user_id, None)

@bot.on_callback_query(filters.regex(r"^(gift_\d+|increment_gift_\d+|decrement_gift_\d+|show_donate_options|refund_.+)$"))
async def handle_donate_callback(client: Client, callback_query):
    data = callback_query.data
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    message_id = callback_query.message.id
    LOGGER.info(f"Callback query received: data={data}, user: {user_id}, chat: {chat_id}")
    try:
        if data.startswith("gift_"):
            quantity = int(data.split("_")[1])
            await client.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=INVOICE_CREATION_TEXT.format(quantity),
                parse_mode=ParseMode.MARKDOWN
            )
            await generate_invoice(chat_id, user_id, quantity, client, message_id)
            await callback_query.answer("✅ Invoice Generated! Donate Now! ⭐️")
        elif data.startswith("increment_gift_"):
            current_amount = int(data.split("_")[2])
            new_amount = current_amount + 5
            reply_markup = get_donation_buttons(new_amount)
            await callback_query.message.edit_text(
                text=DONATION_OPTIONS_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            await callback_query.answer(f"Updated to {new_amount} Stars")
            LOGGER.info(f"Incremented donation amount to {new_amount} for user {user_id}")
        elif data.startswith("decrement_gift_"):
            current_amount = int(data.split("_")[2])
            new_amount = max(5, current_amount - 5)
            reply_markup = get_donation_buttons(new_amount)
            await callback_query.message.edit_text(
                text=DONATION_OPTIONS_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            await callback_query.answer(f"Updated to {new_amount} Stars")
            LOGGER.info(f"Decremented donation amount to {new_amount} for user {user_id}")
        elif data == "show_donate_options":
            reply_markup = get_donation_buttons()
            await callback_query.message.edit_text(
                text=DONATION_OPTIONS_TEXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
            await callback_query.answer()
            LOGGER.info(f"Showed donation options to user {user_id}")
        elif data.startswith("refund_"):
            admin_ids = ADMIN_ID if isinstance(ADMIN_ID, (list, tuple)) else [ADMIN_ID]
            if user_id in admin_ids:
                payment_id = data.replace("refund_", "")
                user_info = payment_data.get(payment_id)
                if not user_info:
                    await callback_query.answer("❌ Payment data not found!", show_alert=True)
                    return
                refund_user_id = user_info['user_id']
                refund_amount = user_info['amount']
                full_charge_id = user_info['charge_id']
                full_name = user_info['full_name']
                try:
                    result = await client.refund_star_payment(refund_user_id, full_charge_id)
                    if result:
                        await callback_query.message.edit_text(
                            text=REFUND_SUCCESS_TEXT.format(refund_amount, full_name, refund_user_id),
                            parse_mode=ParseMode.MARKDOWN
                        )
                        await callback_query.answer("✅ Refund processed successfully!")
                        payment_data.pop(payment_id, None)
                        LOGGER.info(f"Successfully refunded {refund_amount} stars to user {refund_user_id}")
                    else:
                        await callback_query.answer("❌ Refund failed!", show_alert=True)
                        LOGGER.error(f"Refund failed for user {refund_user_id}")
                except Exception as e:
                    LOGGER.error(f"❌ Refund failed for user {refund_user_id}: {str(e)}")
                    await callback_query.message.edit_text(
                        text=REFUND_FAILED_TEXT.format(refund_amount, full_name, refund_user_id, str(e)),
                        parse_mode=ParseMode.MARKDOWN
                    )
                    await callback_query.answer("❌ Refund failed!", show_alert=True)
            else:
                await callback_query.answer("❌ You don't have permission to refund!", show_alert=True)
                LOGGER.warning(f"Unauthorized refund attempt by user {user_id}")
    except Exception as e:
        LOGGER.error(f"Error processing donation callback in chat {chat_id}: {e}")
        await callback_query.answer("❌ Sorry Bro! Donation System Error", show_alert=True)

@bot.on_pre_checkout_query()
async def process_pre_checkout_query(client: Client, pre_checkout_query):
    try:
        await client.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
        LOGGER.info(f"✅ Pre-checkout query {pre_checkout_query.id} OK for user {pre_checkout_query.from_user.id}")
    except Exception as e:
        LOGGER.error(f"❌ Pre-checkout query {pre_checkout_query.id} failed: {str(e)}")
        await client.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="Failed to process pre-checkout."
        )

@bot.on_message(filters.successful_payment)
async def process_successful_payment(client: Client, message):
    payment = message.successful_payment
    user_id = message.from_user.id
    chat_id = message.chat.id
    LOGGER.info(f"Processing successful payment for user {user_id} in chat {chat_id}")
    try:
        user = message.from_user
        full_name = f"{user.first_name} {getattr(user, 'last_name', '')}".strip() or "Unknown"
        username = f"@{user.username}" if user.username else "@N/A"
        payment_id = str(uuid.uuid4())[:16]
        payment_data[payment_id] = {
            'user_id': user_id,
            'full_name': full_name,
            'username': username,
            'amount': payment.total_amount,
            'charge_id': payment.telegram_payment_charge_id
        }
        success_buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Transaction ID", copy_text=payment.telegram_payment_charge_id)]]
        )
        await client.send_message(
            chat_id=chat_id,
            text=PAYMENT_SUCCESS_TEXT.format(full_name, payment.total_amount, payment.telegram_payment_charge_id),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=success_buttons
        )
        admin_text = ADMIN_NOTIFICATION_TEXT.format(full_name, user_id, username, payment.total_amount, payment.telegram_payment_charge_id)
        refund_buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton(f"Refund {payment.total_amount} ⭐️", callback_data=f"refund_{payment_id}")]]
        )
        admin_ids = ADMIN_ID if isinstance(ADMIN_ID, (list, tuple)) else [ADMIN_ID]
        for admin_id in admin_ids:
            try:
                await client.send_message(
                    chat_id=admin_id,
                    text=admin_text,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=refund_buttons
                )
            except Exception as e:
                LOGGER.error(f"❌ Failed to notify admin {admin_id}: {str(e)}")
        LOGGER.info(f"Successfully processed payment for user {user_id}: {payment.total_amount} stars")
    except Exception as e:
        LOGGER.error(f"❌ Payment processing failed for user {user_id}: {str(e)}")
        support_buttons = InlineKeyboardMarkup(
            [[InlineKeyboardButton("📞 Contact Support", url=f"tg://user?id={admin_ids[0]}")]]
        )
        await client.send_message(
            chat_id=chat_id,
            text=PAYMENT_FAILED_TEXT,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=support_buttons
        )