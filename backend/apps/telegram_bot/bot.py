"""
Telegram Bot - python-telegram-bot v20+
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, "/app")
django.setup()

import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters,
)
from django.conf import settings

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN


# =============================================================================
# Command Handlers
# =============================================================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_msg = (
        f"سلام {user.first_name}! 👋\n\n"
        f"به ربات سالن فائزه خوش آمدید.\n\n"
        f"🔹 ما در زمینه بافت و اکستنشن مو تخصص داریم.\n"
        f"🔹 ظرافت، دوام بالا، حال خوب، اعتماد به نفس\n\n"
        f"برای استفاده از منو /menu را بزنید."
    )
    await update.message.reply_text(welcome_msg)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📅 نوبت‌های من", callback_data="my_appointments")],
        [InlineKeyboardButton("🗓 رزرو نوبت جدید", callback_data="new_appointment")],
        [InlineKeyboardButton("❌ لغو نوبت", callback_data="cancel_appointment")],
        [InlineKeyboardButton("📞 شماره تماس", callback_data="contact")],
        [InlineKeyboardButton("📍 آدرس سالن", callback_data="address")],
        [InlineKeyboardButton("📱 اینستاگرام", callback_data="instagram")],
        [InlineKeyboardButton("🔗 اتصال به حساب کاربری", callback_data="link_account")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("منوی اصلی:", reply_markup=reply_markup)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🔹 /start - شروع\n"
        "🔹 /menu - منو\n"
        "🔹 /contact - اطلاعات تماس\n"
        "🔹 /help - راهنما\n"
    )
    await update.message.reply_text(help_text)


async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📞 شماره تماس:\n"
        "۰۹۳۹۹۵۴۵۱۱۳\n\n"
        "📍 آدرس:\n"
        "ستارخان کوچه ۱۲/۱\n"
        "عفیف‌آباد کوچه ۲۲\n\n"
        "📱 اینستاگرام:\n"
        "@Baftmofaezeh"
    )
    await update.message.reply_text(msg)


# =============================================================================
# Callback Handlers
# =============================================================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "my_appointments":
        await query.edit_message_text(
            "برای مشاهده نوبت‌ها لطفاً حساب کاربری خود را متصل کنید.\n"
            "از منوی اصلی 'اتصال به حساب کاربری' را بزنید."
        )

    elif data == "new_appointment":
        await query.edit_message_text(
            "برای رزرو نوبت به سایت ما مراجعه کنید:\n"
            "https://faezeh-salon.ir/appointments\n\n"
            "یا با شماره ۰۹۳۹۹۵۴۵۱۱۳ تماس بگیرید."
        )

    elif data == "cancel_appointment":
        await query.edit_message_text(
            "برای لغو نوبت:\n"
            "۱. وارد سایت شوید\n"
            "۲. نوبت خود را پیدا کنید\n"
            "۳. گزینه لغو را بزنید\n\n"
            "یا با ۰۹۳۹۹۵۴۵۱۱۳ تماس بگیرید."
        )

    elif data == "contact":
        await query.edit_message_text(
            "📞 شماره تماس: ۰۹۳۹۹۵۴۵۱۱۳\n"
            "📱 اینستاگرام: @Baftmofaezeh"
        )

    elif data == "address":
        await query.edit_message_text(
            "📍 آدرس:\n"
            "۱. ستارخان کوچه ۱۲/۱\n"
            "۲. عفیف‌آباد کوچه ۲۲"
        )

    elif data == "instagram":
        await query.edit_message_text(
            "📱 پیج اینستاگرام:\n"
            "@Baftmofaezeh\n\n"
            "https://instagram.com/Baftmofaezeh"
        )

    elif data == "link_account":
        await query.edit_message_text(
            "برای اتصال حساب:\n"
            "۱. وارد سایت شوید\n"
            "۲. از پروفایل گزینه 'اتصال به تلگرام' را بزنید\n"
            "۳. کد دریافتی را اینجا وارد کنید."
        )


# =============================================================================
# Main
# =============================================================================

def main():
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("contact", contact))
    application.add_handler(CallbackQueryHandler(button_handler))

    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
