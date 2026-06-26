import os
import asyncio
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_LINK = "https://t.me/projectbuild1"

if not BOT_TOKEN:
    raise Exception("❌ Missing BOT_TOKEN!")

# Flask app (Gunicorn will serve this)
flask_app = Flask(__name__)

@flask_app.route('/')
def health_check():
    return "🤖 Telegram Bot is running!", 200

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("📢 Join Our Channel", url=CHANNEL_LINK)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Welcome to our bot!\n\nClick the button below to join our official channel:\n👇👇👇",
        reply_markup=reply_markup
    )

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("✅ Bot is ready!")
    app.run_polling()

# Start bot thread when Gunicorn loads this module
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()
